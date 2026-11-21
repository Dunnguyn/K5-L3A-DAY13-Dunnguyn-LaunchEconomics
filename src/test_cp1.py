"""CP1 QA: chạy python -m unittest -v test_cp1 từ src/. Không sửa dữ liệu."""
import contextlib
import csv
from decimal import Decimal
import io
import math
from pathlib import Path
import subprocess
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

import lab13 as lab


class CP1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = pd.read_csv('logix_runs.csv')
        cls.q = pd.read_csv('logix_requests.csv', keep_default_na=False)

    def test_qa01_known_answers(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            lab.kiem_tra_dap_an_biet_truoc()
        self.assertIn('Ba phép thử đáp án biết trước: ĐẠT', output.getvalue())

    def test_qa01_boundaries(self):
        for k in (1, 2, 3, None):
            self.assertEqual(lab.so_lan_chay_ky_vong(1, k), 1)
            self.assertEqual(lab.ti_le_thanh_cong(1, k), 1)
            self.assertEqual(lab.he_so_chi_phi_moi_viec_thanh_cong(1, k), 1)
            self.assertEqual(lab.ti_le_thanh_cong(0, k), 0)
            self.assertTrue(math.isinf(lab.he_so_chi_phi_moi_viec_thanh_cong(0, k)))
        self.assertEqual(lab.so_lan_chay_ky_vong(0, 3), 3)
        self.assertTrue(math.isinf(lab.so_lan_chay_ky_vong(0)))
        self.assertEqual(lab.so_lan_chay_ky_vong(0.2, 1), 1)
        self.assertAlmostEqual(lab.so_lan_chay_ky_vong(1e-16, 3), 3)
        self.assertAlmostEqual(lab.ti_le_thanh_cong(0.8, 3), 0.992)

    def test_qa01_invalid_parameters(self):
        for f in (lab.so_lan_chay_ky_vong, lab.ti_le_thanh_cong, lab.he_so_chi_phi_moi_viec_thanh_cong):
            for p in (-0.1, 1.1, math.nan, math.inf, '0.8', True, None):
                with self.subTest(f=f.__name__, p=p), self.assertRaises(ValueError):
                    f(p)
            for k in (0, -1, 1.5, '2', True, math.nan):
                with self.subTest(f=f.__name__, k=k), self.assertRaises(ValueError):
                    f(0.8, k)

    def test_qa02_integrity(self):
        self.assertEqual(self.r.shape, (1624, 8))
        self.assertEqual(self.q.shape, (1200, 13))
        self.assertFalse(self.r.run_id.duplicated().any())
        self.assertFalse(self.r.duplicated(['request_id', 'attempt']).any())
        self.assertFalse(self.q.request_id.duplicated().any())
        self.assertEqual(set(self.r.request_id), set(self.q.request_id))
        self.assertFalse(self.r.isna().any().any())
        self.assertFalse(self.q.isna().any().any())
        self.assertGreater(self.q.quyet_dinh_xem_lai.eq('').sum(), 0)
        counts = self.r.groupby('request_id').size().sort_index()
        self.assertEqual(counts.tolist(), self.q.set_index('request_id').sort_index().so_lan_chay.tolist())
        for col in ('attempt', 'tokens_in', 'tokens_out', 'tool_calls'):
            self.assertTrue(pd.api.types.is_integer_dtype(self.r[col]))

    def test_qa02_original_files_unchanged(self):
        for name in ('logix_runs.csv', 'logix_requests.csv', 'lab13_starter.py'):
            original = subprocess.check_output(['git', 'show', f'HEAD:src/{name}'])
            self.assertEqual(Path(name).read_bytes().replace(b'\r\n', b'\n'), original.replace(b'\r\n', b'\n'))

    def independent_cost(self, request_ids=None, limit=None):
        """Đối chiếu bằng csv + Decimal, không dùng phép tổng pandas của mo_hinh."""
        with open('logix_requests.csv', encoding='utf-8', newline='') as f:
            qs = [x for x in csv.DictReader(f) if request_ids is None or x['request_id'] in request_ids]
        ids = {x['request_id'] for x in qs}
        token = tool = retry = Decimal(0)
        with open('logix_runs.csv', encoding='utf-8', newline='') as f:
            for x in csv.DictReader(f):
                if x['request_id'] not in ids or (limit is not None and int(x['attempt']) > limit):
                    continue
                t = (Decimal(x['tokens_in']) * 26 + Decimal(x['tokens_out']) * 130) / 1000
                u = Decimal(x['tool_calls']) * 15
                token += t
                tool += u
                if int(x['attempt']) > 1:
                    retry += t + u
        review = rework = Decimal(0)
        success = 0
        for x in qs:
            if limit is not None and int(x['so_lan_chay']) > limit:
                continue
            review += Decimal(x['phut_xem_lai_simulated']) * 2000
            rework += Decimal(x['phut_lam_lai_simulated']) * 2000
            success += x['ket_qua'] == 'thanh_cong'
        total = token + tool + review + rework
        return dict(token=token, tool=tool, chay_lai=retry, xem_lai=review, lam_lai=rework,
                    tong=total, thanh_cong=success, cps=total / success if success else math.inf,
                    hoa_don_moi_yc=(token + tool) / len(qs) if qs else 0)

    def test_qa03_independent_costs_and_totals(self):
        result = lab.mo_hinh(self.r, self.q)
        for key, value in self.independent_cost().items():
            self.assertAlmostEqual(result[key], float(value), places=7, msg=key)
        self.assertEqual(self.r[['tokens_in', 'tokens_out', 'tool_calls']].sum().tolist(), [5771712, 734774, 5600])
        self.assertEqual(self.q[['phut_xem_lai_simulated', 'phut_lam_lai_simulated']].sum().tolist(), [890, 1132])
        self.assertEqual(result['thanh_cong'], 978)
        self.assertAlmostEqual(result['tong'], sum(result[k] for k in ['token', 'tool', 'xem_lai', 'lam_lai']))

    def test_qa03_failed_runs_still_charged(self):
        q = self.q.loc[self.q.ket_qua == 'chuyen_nhan_vien']
        m = lab.mo_hinh(self.r, q)
        self.assertGreater(m['token'] + m['tool'], 0)
        self.assertEqual(m['thanh_cong'], 0)
        self.assertTrue(math.isinf(m['cps']))
        self.assertTrue(all(not math.isnan(x) for x in m.values()))

    def test_qa03_empty_selection(self):
        m = lab.mo_hinh(self.r, self.q.iloc[:0])
        self.assertEqual(m['tong'], 0)
        self.assertEqual(m['hoa_don_moi_yc'], 0)
        self.assertTrue(math.isinf(m['cps']))

    def test_qa04_segmentation(self):
        a = lab.phan_tich_theo_loai(self.r, self.q)
        m = lab.mo_hinh(self.r, self.q)
        self.assertEqual(a.so_yc.sum(), len(self.q))
        self.assertEqual(a.thanh_cong.sum(), m['thanh_cong'])
        self.assertAlmostEqual(a.tong.sum(), m['tong'])
        for row in a.to_dict('records'):
            q = self.q.loc[self.q.loai == row['loai']]
            expected = self.independent_cost(set(q.request_id))
            self.assertAlmostEqual(row['cps'], float(expected['cps']))
            for k in (1, 2, 3):
                r = self.r.loc[self.r.request_id.isin(q.request_id) & self.r.attempt.eq(k)]
                self.assertEqual(row[f'n_{k}'], len(r))
                self.assertAlmostEqual(row[f'phan_tram_ok_{k}'], 100 * r.status.eq('ok').mean())

    def test_qa05_fixed_cost(self):
        a = lab.phan_tich_co_dinh(self.r, self.q)
        self.assertEqual(a.thanh_cong.tolist(), [33750, 16875])
        self.assertAlmostEqual(a.co_dinh.iloc[1], 2 * a.co_dinh.iloc[0])
        self.assertEqual(a.bien_doi.iloc[0], a.bien_doi.iloc[1])
        for row in a.to_dict('records'):
            self.assertAlmostEqual(row['co_dinh'], 40000000 / row['thanh_cong'])
            self.assertAlmostEqual(row['tong'], row['co_dinh'] + row['bien_doi'])
            self.assertAlmostEqual(row['so_baseline'], row['tong'] / 12000)

    def test_qa06_retry_limits_and_no_mutation(self):
        r, q = self.r.copy(deep=True), self.q.copy(deep=True)
        for k in (1, 2, 3):
            m = lab.mo_hinh(r, q, max_lan_chay=k)
            for key, value in self.independent_cost(limit=k).items():
                self.assertAlmostEqual(m[key], float(value), places=7, msg=f'{k}/{key}')
        assert_frame_equal(r, self.r)
        assert_frame_equal(q, self.q)

    def test_qa06_price_parameters(self):
        base = lab.mo_hinh(self.r, self.q)
        m = lab.mo_hinh(self.r, self.q, gia_vao=52, gia_ra=260, gia_tool=30,
                        luong_phut=4000, he_so_xem_lai=0.5, he_so_lam_lai=0)
        self.assertAlmostEqual(m['token'], 2 * base['token'])
        self.assertAlmostEqual(m['tool'], 2 * base['tool'])
        self.assertEqual(m['xem_lai'], base['xem_lai'])
        self.assertEqual(m['lam_lai'], 0)

    def test_qa06_bad_inputs(self):
        for kw in ({'gia_vao': -1}, {'gia_ra': math.nan}, {'he_so_xem_lai': '1'}, {'max_lan_chay': True}, {'max_lan_chay': 0}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                lab.mo_hinh(self.r, self.q, **kw)
        cases = [(self.r, pd.concat([self.q, self.q.iloc[:1]])),
                 (pd.concat([self.r, self.r.iloc[:1]]), self.q),
                 (self.r.iloc[1:], self.q), (self.r.drop(columns='tokens_in'), self.q)]
        bad = self.r.copy()
        bad.loc[0, 'tokens_in'] = -1
        cases.append((bad, self.q))
        bad = self.q.copy()
        bad.loc[0, 'phut_lam_lai_simulated'] = math.nan
        cases.append((self.r, bad))
        for r, q in cases:
            with self.assertRaises(ValueError):
                lab.mo_hinh(r, q)

    def test_qa06_instructor_comparison(self):
        m = lab.mo_hinh(self.r, self.q)
        for key, reference in dict(token=245585, tool=84000, chay_lai=93804,
                                   xem_lai=1780000, lam_lai=2264000, tong=4373585,
                                   thanh_cong=978, cps=4472, hoa_don_moi_yc=274.7).items():
            self.assertLess(abs(m[key] / reference - 1), 0.02)
        a = lab.phan_tich_theo_loai(self.r, self.q)
        for actual, ref in zip(a.cps, [2696, 8221, 22515, 10215]):
            self.assertLess(abs(actual / ref - 1), 0.02)
        f = lab.phan_tich_co_dinh(self.r, self.q)
        for actual, ref in zip(f.tong, [4599, 5784]):
            self.assertLess(abs(actual / ref - 1), 0.02)


if __name__ == '__main__':
    unittest.main()
