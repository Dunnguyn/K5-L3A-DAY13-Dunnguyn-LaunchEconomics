"""CP2: invariant, tính độc lập csv/Decimal, synthetic retry và regression CP1."""
import ast
import csv
from decimal import Decimal as D
import hashlib
from pathlib import Path
import statistics
import subprocess
import unittest
from unittest.mock import patch

import pandas as pd
from pandas.testing import assert_frame_equal

import lab13 as lab


class CP2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = pd.read_csv('logix_runs.csv')
        cls.q = pd.read_csv('logix_requests.csv', keep_default_na=False)
        with open('logix_runs.csv', encoding='utf-8', newline='') as f:
            cls.raw_runs = list(csv.DictReader(f))
        with open('logix_requests.csv', encoding='utf-8', newline='') as f:
            cls.raw_reqs = list(csv.DictReader(f))
        cls.b1 = lab.phan_tich_do_nhay(cls.r, cls.q).set_index('id')
        cls.base = lab.mo_hinh(cls.r, cls.q)

    def independent(self, limit=None, gia_vao=26, gia_ra=130, review=1, rework=1, wage=2000):
        """Tính độc lập bằng từng dòng CSV và Decimal, không gọi mo_hinh."""
        token = tool = xem = lam = D(0)
        success = 0
        for row in self.raw_runs:
            if limit is None or int(row['attempt']) <= limit:
                token += (D(row['tokens_in']) * D(gia_vao) + D(row['tokens_out']) * D(gia_ra)) / 1000
                tool += D(row['tool_calls']) * 15
        for row in self.raw_reqs:
            if limit is not None and int(row['so_lan_chay']) > limit:
                continue
            xem += D(row['phut_xem_lai_simulated']) * D(wage) * D(str(review))
            lam += D(row['phut_lam_lai_simulated']) * D(wage) * D(str(rework))
            success += row['ket_qua'] == 'thanh_cong'
        total = token + tool + xem + lam
        return float(total), success, float(total / success)

    def check_scenario(self, scenario, **kw):
        total, success, cps = self.independent(**kw)
        row = self.b1.loc[scenario]
        self.assertAlmostEqual(row.tong, total, places=7)
        self.assertEqual(row.thanh_cong, success)
        self.assertAlmostEqual(row.cps, cps, places=8)
        self.assertAlmostEqual(row.delta_vnd, cps - self.base['cps'])
        self.assertAlmostEqual(row.delta_pct, 100 * (cps / self.base['cps'] - 1))

    def test_b01_baseline_preservation(self):
        total, success, cps = self.independent()
        self.assertAlmostEqual(self.base['tong'], total, places=7)
        self.assertEqual(self.base['thanh_cong'], success)
        self.assertAlmostEqual(self.base['cps'], cps)
        self.assertAlmostEqual(cps, 4471.968438, places=6)
        self.assertEqual(success, 978)

    def test_b02_nine_scenarios_call_model(self):
        expected = [dict(gia_vao=52, gia_ra=260), dict(gia_vao=13, gia_ra=65),
                    dict(he_so_xem_lai=2.0), dict(he_so_xem_lai=0.5),
                    dict(he_so_lam_lai=2.0), dict(he_so_lam_lai=0.5),
                    dict(luong_phut=2500), dict(max_lan_chay=2), dict(max_lan_chay=1)]
        with patch.object(lab, 'mo_hinh', wraps=lab.mo_hinh) as spy:
            result = lab.phan_tich_do_nhay(self.r, self.q)
        self.assertEqual(result.id.tolist(), [f'B1-{i:02d}' for i in range(10)])
        calls = [c.kwargs for c in spy.call_args_list if c.kwargs]
        self.assertEqual(calls, expected)
        self.assertFalse(result.select_dtypes('number').isna().any().any())

    def test_b03_token_and_linearity(self):
        self.check_scenario('B1-01', gia_vao=52, gia_ra=260)
        self.check_scenario('B1-02', gia_vao=13, gia_ra=65)
        self.assertAlmostEqual(self.b1.loc['B1-02', 'delta_vnd'], -0.5 * self.b1.loc['B1-01', 'delta_vnd'])

    def test_b04_review_and_linearity(self):
        self.check_scenario('B1-03', review=2)
        self.check_scenario('B1-04', review=0.5)
        self.assertAlmostEqual(self.b1.loc['B1-04', 'delta_vnd'], -0.5 * self.b1.loc['B1-03', 'delta_vnd'])

    def test_b05_rework_and_linearity(self):
        self.check_scenario('B1-05', rework=2)
        self.check_scenario('B1-06', rework=0.5)
        self.assertAlmostEqual(self.b1.loc['B1-06', 'delta_vnd'], -0.5 * self.b1.loc['B1-05', 'delta_vnd'])

    def test_b06_wage(self):
        self.check_scenario('B1-07', wage=2500)
        expected_delta = 0.25 * (self.base['xem_lai'] + self.base['lam_lai']) / self.base['thanh_cong']
        self.assertAlmostEqual(self.b1.loc['B1-07', 'delta_vnd'], expected_delta)

    def test_b07_combined_and_ranking(self):
        b = lab.phan_tich_ket_hop(self.r, self.q)
        total, success, cps = self.independent(gia_vao=52, gia_ra=260, review=2)
        self.assertAlmostEqual(b['tong'], total)
        self.assertEqual(b['thanh_cong'], success)
        self.assertAlmostEqual(b['cps'], cps)
        self.assertAlmostEqual(b['interaction'], 0, delta=1e-9)
        self.assertAlmostEqual(b['delta_vnd'], b['tong_tac_dong_rieng'])
        self.assertEqual(b['ranking'].id.tolist(), ['B1-05', 'B1-03', 'B1-07'])

    def test_b08_retry_cap_synthetic(self):
        # Yêu cầu thứ 2 cuối cùng thành công ở attempt 2; cắt ở 1 phải mất success
        # và mọi phút review/rework của yêu cầu đó, nhưng vẫn tính run lỗi đầu.
        r = pd.DataFrame([
            dict(run_id='a', request_id='one', attempt=1, tokens_in=1000, tokens_out=0, tool_calls=1, status='ok'),
            dict(run_id='b', request_id='two', attempt=1, tokens_in=2000, tokens_out=0, tool_calls=2, status='loi'),
            dict(run_id='c', request_id='two', attempt=2, tokens_in=100000, tokens_out=10000, tool_calls=100, status='ok')])
        q = pd.DataFrame([
            dict(request_id='one', so_lan_chay=1, ket_qua='thanh_cong', phut_xem_lai_simulated=1, phut_lam_lai_simulated=0),
            dict(request_id='two', so_lan_chay=2, ket_qua='thanh_cong', phut_xem_lai_simulated=9, phut_lam_lai_simulated=7)])
        m = lab.mo_hinh(r, q, max_lan_chay=1)
        self.assertEqual(m['token'], 78)
        self.assertEqual(m['tool'], 45)
        self.assertEqual(m['chay_lai'], 0)
        self.assertEqual(m['xem_lai'], 2000)
        self.assertEqual(m['lam_lai'], 0)
        self.assertEqual(m['thanh_cong'], 1)
        self.assertEqual(m['tong'], 2123)
        self.assertEqual(lab.mo_hinh(r, q, max_lan_chay=2)['thanh_cong'], 2)

    def test_b09_retry_accounting_independent(self):
        table = lab.phan_tich_gioi_han_chay(self.r, self.q)
        for row in table.to_dict('records'):
            total, success, cps = self.independent(limit=row['max_attempts'])
            self.assertAlmostEqual(row['agent_cost'], total, places=7)
            self.assertAlmostEqual(row['agent_cps'], cps)
            self.assertEqual(row['fallback'], (len(self.raw_reqs) - success) * 12000)
            self.assertAlmostEqual(row['system_cost'], total + row['fallback'])
            self.assertAlmostEqual(row['system_per_request'], row['system_cost'] / len(self.raw_reqs))

    def test_b10_retry_reconciliation_and_policy(self):
        b = lab.phan_tich_gioi_han_chay(self.r, self.q)
        self.assertTrue((b.successes + b.unresolved == len(self.q)).all())
        self.assertEqual(b.loc[b.agent_cps.idxmin(), 'max_attempts'], 1)
        self.assertEqual(b.loc[b.system_cost.idxmin(), 'max_attempts'], 2)
        self.assertEqual(b.unresolved.iloc[0] - b.unresolved.iloc[1], 85)
        self.check_scenario('B1-08', limit=2)
        self.check_scenario('B1-09', limit=1)

    def b4_inputs(self):
        scope = [q for q in self.raw_reqs if q['loai'] in {'noi_dia', 'hang_nang'}]
        ids = {q['request_id'] for q in scope}
        runs = [r for r in self.raw_runs if r['request_id'] in ids]
        ok = {r['request_id'] for r in runs if r['status'] == 'ok'}
        tech = sum((D(r['tokens_in']) * 26 + D(r['tokens_out']) * 130) / 1000 + D(r['tool_calls']) * 15 for r in runs)
        return scope, ok, float(tech)

    def test_b11_b4_scope_and_unique_reviews(self):
        b = lab.phan_tich_xem_lai_100(self.r, self.q)
        scope, ok, _ = self.b4_inputs()
        self.assertEqual(b['so_yc'], len(scope))
        self.assertEqual(b['n_review'], len(ok))
        self.assertEqual(b['n_rework'], sum(q['ket_qua'] == 'lam_lai' for q in scope))
        self.assertEqual(b['thanh_cong'], sum(q['ket_qua'] == 'thanh_cong' for q in scope))
        self.assertEqual((b['so_yc'], b['thanh_cong'], b['n_review'], b['n_rework']), (982, 900, 948, 48))
        # B4 dùng token/tool từ scope: run ngoài scope không ảnh hưởng technical.
        changed = self.r.copy()
        changed.loc[~changed.request_id.isin({q['request_id'] for q in scope}), 'tokens_in'] *= 100
        self.assertEqual(lab.phan_tich_xem_lai_100(changed, self.q)['bang'].technical.tolist(), b['bang'].technical.tolist())

    def test_b12_b4_mean_median_and_costs(self):
        b = lab.phan_tich_xem_lai_100(self.r, self.q)
        scope, ok, technical = self.b4_inputs()
        all_minutes = [int(q['phut_lam_lai_simulated']) for q in self.raw_reqs if q['ket_qua'] == 'lam_lai']
        scope_minutes = [int(q['phut_lam_lai_simulated']) for q in scope if q['ket_qua'] == 'lam_lai']
        self.assertEqual(b['n_rework_toan_mau'], len(all_minutes))
        self.assertEqual(b['mean_toan_mau'], statistics.mean(all_minutes))
        self.assertEqual(b['median_toan_mau'], statistics.median(all_minutes))
        self.assertEqual(b['mean_pham_vi'], statistics.mean(scope_minutes))
        self.assertEqual(b['median_pham_vi'], statistics.median(scope_minutes))
        for row, minutes in zip(b['bang'].to_dict('records'), [9, round(statistics.mean(all_minutes), 1), statistics.mean(all_minutes)]):
            review = len(ok) * 5 * 2000
            rework = len(scope_minutes) * minutes * 2000
            total = technical + review + rework
            self.assertEqual(row['phut_rework'], minutes)
            self.assertAlmostEqual(row['technical'], technical)
            self.assertEqual(row['review'], review)
            self.assertAlmostEqual(row['rework'], rework)
            self.assertAlmostEqual(row['tong'], total)
            self.assertAlmostEqual(row['cps'], total / b['thanh_cong'])
            self.assertAlmostEqual(row['so_baseline'], total / b['thanh_cong'] / 12000)

    def test_b13_break_even_direct_substitution(self):
        b = lab.phan_tich_xem_lai_100(self.r, self.q)
        for row in b['bang'].to_dict('records'):
            t = row['hoa_von_phut_review']
            direct_cps = (row['technical'] + b['n_review'] * t * 2000 + row['rework']) / b['thanh_cong']
            self.assertAlmostEqual(direct_cps, 12000, places=8)
            self.assertGreater((row['technical'] + b['n_review'] * (t + 0.01) * 2000 + row['rework']) / b['thanh_cong'], 12000)
        self.assertEqual([round(t, 1) for t in b['bang'].hoa_von_phut_review[:2]], [5.1, 4.8])

    def test_b14_immutability_and_determinism(self):
        names = ['logix_runs.csv', 'logix_requests.csv', 'lab13_starter.py']
        hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
        r, q = self.r.copy(deep=True), self.q.copy(deep=True)
        for f in [lab.phan_tich_do_nhay, lab.phan_tich_ket_hop, lab.phan_tich_gioi_han_chay, lab.phan_tich_xem_lai_100]:
            first, second = f(r, q), f(r, q)
            if isinstance(first, pd.DataFrame):
                assert_frame_equal(first, second)
            else:
                for key in first:
                    if isinstance(first[key], pd.DataFrame):
                        assert_frame_equal(first[key], second[key])
                    else:
                        self.assertEqual(first[key], second[key])
        assert_frame_equal(r, self.r)
        assert_frame_equal(q, self.q)
        self.assertEqual(hashes, {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names})

    def test_b15_cp1_functions_report_and_tests_unchanged(self):
        original = subprocess.check_output(['git', 'show', 'HEAD:src/lab13.py']).decode('utf-8')
        before = {n.name: ast.dump(n) for n in ast.parse(original).body if isinstance(n, ast.FunctionDef)}
        after = {n.name: ast.dump(n) for n in ast.parse(Path('lab13.py').read_text(encoding='utf-8')).body if isinstance(n, ast.FunctionDef)}
        for name, function in before.items():
            self.assertEqual(after[name], function, name)
        report = subprocess.check_output(['git', 'show', 'HEAD:report/team/bang_chi_phi.md']).decode('utf-8')
        actual = Path('../report/team/bang_chi_phi.md').read_text(encoding='utf-8')
        self.assertEqual(report.split('## B1', 1)[0], actual.split('## B1', 1)[0])
        old_test = subprocess.check_output(['git', 'show', 'HEAD:src/test_cp1.py']).decode('utf-8')
        self.assertEqual(old_test, Path('test_cp1.py').read_text(encoding='utf-8'))

    def test_b16_instructor_comparison(self):
        refs = [4723, 4346, 6292, 3562, 6787, 3315, 5506, 4237, 4111]
        for actual, ref in zip(self.b1.cps.iloc[1:], refs):
            self.assertLess(abs(actual / ref - 1), 0.02)
        for actual, ref in zip(self.b1.delta_pct.iloc[1:], [5.6, -2.8, 40.7, -20.3, 51.8, -25.9, 23.1, -5.2, -8.1]):
            self.assertLess(abs(actual / ref - 1), 0.02)
        b3 = lab.phan_tich_gioi_han_chay(self.r, self.q)
        self.assertEqual(b3.unresolved.tolist(), [319, 234, 222])
        for actual, ref in zip(b3.system_cost, [7449781, 6901220, 7037585]):
            self.assertLess(abs(actual / ref - 1), 0.02)
        self.assertLess(abs(lab.phan_tich_ket_hop(self.r, self.q)['cps'] / 6543 - 1), 0.02)
        b4 = lab.phan_tich_xem_lai_100(self.r, self.q)['bang']
        for actual, ref in zip(b4.cps, [11743, 12414, 12414]):
            self.assertLess(abs(actual / ref - 1), 0.02)


if __name__ == '__main__':
    unittest.main()
