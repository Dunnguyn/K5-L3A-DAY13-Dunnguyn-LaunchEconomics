"""CP5 QA: KPI từ CSV lab, hợp đồng event, hồ sơ và tính nhất quán CP1–CP4.

Chạy từ src: python -m unittest discover -s . -p "test_*.py" -v.
Các tests này không chứng minh instrumentation, remediation hoặc pilot đã vận hành.
"""
import csv
from datetime import date
import hashlib
from pathlib import Path
import re
import subprocess
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal
import yaml

import lab13 as lab


def summarize_kpis(reqs):
    """Phép tính mô tả có kiểm tra dữ liệu; không gán kết quả cho KPI chưa có event."""
    required = {'request_id', 'loai', 'dong_trong_24h', 'mo_lai_trong_7_ngay',
                'duoc_xem_lai', 'quyet_dinh_xem_lai', 'ket_qua'}
    if not isinstance(reqs, pd.DataFrame) or not required.issubset(reqs.columns):
        raise ValueError('Thiếu cột KPI')
    if (reqs.empty or reqs[list(required)].isna().any().any()
            or reqs.request_id.duplicated().any() or reqs.request_id.eq('').any()):
        raise ValueError('Cần request duy nhất và dữ liệu đầy đủ')
    for name in ['dong_trong_24h', 'mo_lai_trong_7_ngay', 'duoc_xem_lai']:
        if not reqs[name].isin([0, 1]).all():
            raise ValueError('Cờ KPI phải nhị phân')
    if not reqs.loai.isin(['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']).all():
        raise ValueError('Loại request không hợp lệ')
    reviewed = reqs.loc[reqs.duoc_xem_lai.eq(1)]
    if not reviewed.quyet_dinh_xem_lai.isin(['giu', 'sua', 'bo']).all():
        raise ValueError('Request reviewed thiếu quyết định hợp lệ')
    scope = reqs.loc[reqs.loai.isin(['noi_dia', 'hang_nang'])]

    def metric(count, total):
        return dict(numerator=int(count), denominator=int(total),
                    rate=float(count / total) if total else None)

    return {
        'KPI-01': metric((reqs.dong_trong_24h.eq(1) & reqs.mo_lai_trong_7_ngay.eq(0)).sum(), len(reqs)),
        'KPI-02': metric(reviewed.quyet_dinh_xem_lai.isin(['sua', 'bo']).sum(), len(reviewed)),
        'KPI-03 overall': metric(reqs.mo_lai_trong_7_ngay.eq(1).sum(), len(reqs)),
        'KPI-03 pilot scope': metric(scope.mo_lai_trong_7_ngay.eq(1).sum(), len(scope)),
        'Rework baseline pilot': metric(scope.ket_qua.eq('lam_lai').sum(), len(scope)),
    }


def markdown_tables(text):
    """Đọc bảng Markdown để QA chính nội dung giao nộp, không bảng mock riêng."""
    tables, lines = [], text.splitlines()
    for index in range(len(lines) - 1):
        if not lines[index].startswith('|') or not re.fullmatch(r'[\s|:\-]+', lines[index + 1]):
            continue
        header = [v.strip() for v in lines[index].strip('|').split('|')]
        rows = []
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].startswith('|'):
            row = [v.strip() for v in lines[cursor].strip('|').split('|')]
            if len(row) != len(header):
                raise ValueError('Số cột Markdown không nhất quán')
            rows.append(dict(zip(header, row)))
            cursor += 1
        tables.append((header, rows))
    return tables


def table_by_first_column(text, column):
    found = [rows for header, rows in markdown_tables(text) if header[0] == column]
    if len(found) != 1:
        raise ValueError('Không tìm được bảng duy nhất: ' + column)
    return found[0]


def vn(value, places=3):
    return f'{value:,.{places}f}'.replace(',', '#').replace('.', ',').replace('#', '.')


def submission_metadata_issues(team, group, index, personal, review_rows,
                               final_labels, current_files, expected_tests):
    """Kiểm tra hợp đồng nộp bài; cho phép cập nhật metadata hợp lệ trước commit.

    Không suy ra reviewer độc lập hoặc approval từ một tài liệu đã được điền.
    """
    issues = []
    try:
        members = table_by_first_column(team, 'STT')
        if (len(members) != 1 or members[0]['Họ tên'] != 'Nguyễn Thị Thùy Dung'
                or members[0]['MSSV'] != '2A202603552'
                or not members[0]['Vai trò'].strip()):
            issues.append('TEAM phải có đúng một người thực hiện và đúng danh tính')
    except (ValueError, KeyError):
        issues.append('Thiếu bảng thành viên hợp lệ')
    if 'Individual Lab' not in team or 'L3A' not in team:
        issues.append('Thiếu hình thức/lớp')

    expected_status = {'CP1': 'Content Complete', 'CP2': 'Content Complete',
                       'CP3': 'Independent Review Pending',
                       'CP4': 'Design & QA Complete', 'CP5': 'Content Complete'}
    try:
        checkpoints = {r['Checkpoint']: r['Trạng thái']
                       for r in table_by_first_column(group, 'Checkpoint')}
        if set(checkpoints) != set(expected_status):
            issues.append('Thiếu checkpoint trong tổng kết')
        for name, status in expected_status.items():
            if status not in checkpoints.get(name, ''):
                issues.append('Sai trạng thái ' + name)
        suites = {r['Suite']: r for r in table_by_first_column(group, 'Suite')}
        for name, count in {**expected_tests, 'Tổng': sum(expected_tests.values())}.items():
            row = suites[name]
            if (int(row['Tests']), int(row['PASS']), int(row['FAIL'])) != (count, count, 0):
                issues.append('Sai số kiểm thử ' + name)
    except (ValueError, KeyError):
        issues.append('Bảng checkpoint hoặc kiểm thử không hợp lệ')

    for name, text in [('TEAM', team), ('group_report', group),
                       ('README', index), ('personal', personal)]:
        if 'PENDING EXTERNAL REVIEW' not in text or 'Planned / Not Approved' not in text:
            issues.append('Thiếu giới hạn external review/pilot ở ' + name)
        if re.search(r'CP4–CP5 (?:còn ở dạng biểu mẫu|và duyệt chéo vẫn chưa thực hiện)', text):
            issues.append('Trạng thái CP4/CP5 lỗi thời ở ' + name)
        if re.search(r'(?:self-review|cp3_self_review\.md)[^\n]{0,140}'
                     r'(?:vẫn trống|giữ trống|chưa điền|20 dòng đánh giá để trống)', text):
            issues.append('Sai hiện trạng self-review ở ' + name)
    try:
        listed = {r['File'].strip('`') for r in table_by_first_column(index, 'File')}
        if listed != set(current_files):
            issues.append('README không khớp danh mục file hiện có')
    except (ValueError, KeyError):
        issues.append('Thiếu danh mục hồ sơ hợp lệ')
    if len(review_rows) != len(final_labels) or len({r['Case ID'] for r in review_rows}) != len(final_labels):
        issues.append('Self-review thiếu/trùng ca')
    for row in review_rows:
        if (row['Self-review label'] != final_labels.get(row['Case ID'])
                or not row['Root-cause explanation'].strip() or not row['Confidence'].strip()):
            issues.append('Self-review không đầy đủ/không khớp nhãn cuối')
    return issues


class CP5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
        cls.runs = pd.read_csv('logix_runs.csv')
        cls.kpi = summarize_kpis(cls.reqs)
        cls.spec = Path('../report/team/chi_so.md').read_text(encoding='utf-8')
        cls.dossier = Path('../report/team/ho_so_launch_v0.md').read_text(encoding='utf-8')
        cls.plan = yaml.safe_load(Path('../report/team/pilot_plan.yaml').read_text(encoding='utf-8'))['pilot']
        cls.spec_rows = {r['KPI ID']: r for r in table_by_first_column(cls.spec, 'KPI ID')}
        cls.events = {r['Event Name']: r for r in table_by_first_column(cls.spec, 'Event Name')}
        cls.risks = {r['Risk ID']: r for r in table_by_first_column(cls.spec, 'Risk ID')}

    def test_e01_primary_independent_csv_and_document(self):
        with open('logix_requests.csv', encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        count = sum(r['dong_trong_24h'] == '1' and r['mo_lai_trong_7_ngay'] == '0' for r in rows)
        self.assertEqual(self.kpi['KPI-01']['numerator'], count)
        self.assertEqual((count, len(rows)), (994, 1200))
        self.assertNotEqual(count, int(self.reqs.ket_qua.eq('thanh_cong').sum()))
        self.assertIn('giả định thiết kế', self.spec)

    def test_e02_review_denominator_and_independent_csv(self):
        with open('logix_requests.csv', encoding='utf-8', newline='') as handle:
            reviewed = [r for r in csv.DictReader(handle) if r['duoc_xem_lai'] == '1']
        count = sum(r['quyet_dinh_xem_lai'] in {'sua', 'bo'} for r in reviewed)
        m = self.kpi['KPI-02']
        self.assertEqual((m['numerator'], m['denominator']), (count, len(reviewed)))
        self.assertEqual((count, len(reviewed)), (48, 177))
        self.assertNotAlmostEqual(m['rate'], count / len(self.reqs))
        self.assertIn('SR-03', self.spec)
        self.assertIn('suggestion_id', self.spec)

    def test_e03_safety_and_documented_calculations(self):
        baseline = lab.safety_baseline(self.reqs)
        for key, name in [('overall', 'KPI-03 overall'), ('pilot', 'KPI-03 pilot scope')]:
            self.assertEqual(self.kpi[name]['numerator'], baseline[key]['reopened'])
            self.assertEqual(self.kpi[name]['denominator'], baseline[key]['n'])
        self.assertEqual(self.kpi['KPI-03 pilot scope']['numerator'], 39)
        self.assertEqual(self.kpi['KPI-03 pilot scope']['denominator'], 982)
        for row in table_by_first_column(self.spec, 'Calculation'):
            m = self.kpi[row['Calculation']]
            self.assertEqual(int(row['Numerator']), m['numerator'])
            self.assertEqual(int(row['Denominator']), m['denominator'])
            self.assertEqual(row['Result'], vn(100 * m['rate'], 4) + '%')

    def test_e04_proposed_metrics_have_no_fabricated_result(self):
        for key in ['KPI-04', 'KPI-05']:
            self.assertNotIn(key, self.kpi)
            self.assertEqual(self.spec_rows[key]['Status'], 'Proposed — Not Yet Measured')
            self.assertIn('Không có kết quả', self.spec_rows[key]['Baseline/Result'])
        self.assertIn('action_used', self.spec_rows['KPI-04']['Event Sources'])
        self.assertIn('sampling_frame=random', self.spec_rows['KPI-05']['Filter/Window'])
        self.assertIn('audit nhắm đích báo riêng', self.spec_rows['KPI-05']['Filter/Window'])

    def test_e05_event_contracts_and_coverage(self):
        required = {'refund_request_created', 'agent_run_completed', 'agent_suggestion_shown',
                    'staff_review_decision', 'staff_rework_completed', 'refund_ledger_write',
                    'handoff_to_staff', 'ticket_closed', 'ticket_reopened', 'audit_sample_checked'}
        self.assertTrue(required.issubset(self.events))
        self.assertGreaterEqual(len(self.events), 10)
        for row in self.events.values():
            properties = set(row['Required Properties'].split(', '))
            self.assertTrue({'trace_id', 'request_id', 'event_timestamp', 'event_id'}.issubset(properties))
            for column in ['Producer', 'Trigger', 'Data Source', 'KPI Supported']:
                self.assertTrue(row[column].strip())
        self.assertIn('Proposed — Not Instrumented', self.spec)

    def test_e06_mapping_fields_supported_by_events(self):
        mappings = table_by_first_column(self.spec, 'KPI')
        self.assertEqual({r['KPI'] for r in mappings}, set(self.spec_rows))
        for row in mappings:
            names = row['Required Events'].split(', ')
            self.assertTrue(set(names).issubset(self.events))
            available = set()
            for name in names:
                available.update(self.events[name]['Required Properties'].split(', '))
            self.assertTrue(set(row['Required Fields'].split(', ')).issubset(available), row['KPI'])
            self.assertTrue(row['Missing Instrumentation'])
        for key in ['coverage_complete', 'source_watermark', 'assigned_staff_id', 'decision_version']:
            self.assertIn(key, self.spec)

    def test_e07_economic_risks_match_model(self):
        b1 = lab.phan_tich_do_nhay(self.runs, self.reqs).set_index('id')
        r1 = self.risks['RISK-01']['Quantified Impact']
        self.assertIn(vn(b1.loc['B1-05', 'cps']), r1)
        self.assertIn(vn(b1.loc['B1-05', 'delta_pct']) + '%', r1)
        b4 = lab.phan_tich_xem_lai_100(self.runs, self.reqs)['bang']
        r2 = self.risks['RISK-02']['Quantified Impact']
        for index in [0, 1]:
            self.assertIn(vn(b4.iloc[index]['cps']), r2)
        self.assertIn(vn(b4.iloc[1]['hoa_von_phut_review']), r2)
        a4 = lab.phan_tich_co_dinh(self.runs, self.reqs)
        r3 = self.risks['RISK-03']['Quantified Impact']
        for column in ['co_dinh', 'tong']:
            for value in a4[column]:
                self.assertIn(vn(value), r3)
        for row in self.risks.values():
            for column in ['Early Warning Indicator', 'Trigger/Threshold', 'Monitoring Window',
                           'Mitigation', 'Owner', 'Status']:
                self.assertTrue(row[column].strip())
            self.assertRegex(row['Trigger/Threshold'], r'\d')
        self.assertGreaterEqual(len(self.risks), 3)

    def test_e08_seven_item_dossier_and_statuses(self):
        rows = table_by_first_column(self.dossier, 'Mục')
        self.assertEqual(len(rows), 7)
        self.assertEqual([r['Mục'].split(' · ')[0] for r in rows], [str(i) for i in range(1, 8)])
        roles = {'Finance Lead', 'PM trợ lý hoàn phí', 'Product Manager',
                 'AI Engineering Lead', 'Giám đốc vận hành LogiX-VN'}
        for row in rows:
            self.assertIn(row['Trạng thái'], {'Giả lập', 'Chưa', 'Xong, có bằng chứng'})
            self.assertIn(row['Người phụ trách'], roles)
            self.assertRegex(row['Con số chính và giới hạn'], r'\d')
        self.assertLessEqual(len(self.dossier.split()), 700)
        self.assertTrue(self.dossier.strip().splitlines()[-1].startswith('**Đề xuất Gate 2a: Go có điều kiện'))

    def test_e09_dossier_numbers_and_cp4_dates(self):
        rows = table_by_first_column(self.dossier, 'Mục')
        a2 = lab.mo_hinh(self.runs, self.reqs)
        self.assertIn(vn(a2['cps']), rows[0]['Con số chính và giới hạn'])
        self.assertIn(vn(a2['tong']), rows[0]['Con số chính và giới hạn'])
        for rate in lab.phan_tich_ket_hop(self.runs, self.reqs)['ranking']['delta_pct']:
            self.assertIn(vn(rate) + '%', rows[1]['Con số chính và giới hạn'])
        b3 = lab.phan_tich_gioi_han_chay(self.runs, self.reqs)
        for cap in [2, 3]:
            value = b3.loc[b3.max_attempts.eq(cap), 'system_per_request'].iloc[0]
            self.assertIn(vn(value), rows[2]['Con số chính và giới hạn'])
        main = self.plan['schedule']['main_50']
        start, end = date.fromisoformat(main['start']), date.fromisoformat(main['end'])
        self.assertIn(start.strftime('%d/%m') + '–' + end.strftime('%d/%m/%Y'), self.dossier)
        for value in [self.plan['decision_date'], self.plan['schedule']['extension_policy']['maximum_decision_if_start_unchanged']]:
            self.assertIn(date.fromisoformat(value).strftime('%d/%m/%Y'), self.dossier)
        self.assertIn('chưa chứng minh hai lượt độc lập', rows[4]['Con số chính và giới hạn'])

    def test_e10_simulated_labels_and_denominator_limits(self):
        rows = table_by_first_column(self.dossier, 'Mục')
        for index in [0, 1, 2, 6]:
            self.assertEqual(rows[index]['Trạng thái'], 'Giả lập')
            self.assertIn('simulated', rows[index]['Con số chính và giới hạn'])
        for key in ['RISK-01', 'RISK-02', 'RISK-03']:
            self.assertIn('simulated', self.risks[key]['Quantified Impact'])
        self.assertIn('khác mẫu số', rows[2]['Con số chính và giới hạn'])
        self.assertIn('fallback có thể chồng rework', self.dossier)
        self.assertIn('không causal lift', rows[3]['Con số chính và giới hạn'])
        self.assertIn('baseline70% là giả định', self.dossier)

    def test_e11_gate_evidence_owner_and_pre_exposure_deadlines(self):
        gates = table_by_first_column(self.spec, 'Gate ID')
        self.assertTrue({f'GATE-0{i}' for i in range(1, 8)}.issubset({g['Gate ID'] for g in gates}))
        first_exposure = date.fromisoformat(self.plan['schedule']['ramp_10']['start'])
        for row in gates:
            self.assertEqual(row['Status'], 'Chưa')
            self.assertTrue(row['Accountable Owner'])
            self.assertGreater(len(row['Evidence Required']), 40)
            self.assertLess(date.fromisoformat(row['Check Date']), first_exposure)
        self.assertIn('hoãn bắt đầu', self.spec)
        self.assertIn('chưa cho kích hoạt', self.spec)
        self.assertIn('No-go cho lịch đề xuất', self.spec)

    def test_e12_protected_sources_and_submission_metadata(self):
        # Chỉ đóng băng nguồn thực sự bất biến trong remediation này.
        # TEAM/group/bang_loi không bị khóa toàn file theo HEAD khi cần sửa metadata.
        names = ['src/lab13.py', 'src/test_cp1.py', 'src/test_cp2.py', 'src/test_cp4.py',
                 'src/lab13_starter.py', 'src/logix_requests.csv', 'src/logix_runs.csv',
                 'report/team/bang_chi_phi.md', 'report/team/cp3_reviewer_summary.md',
                 'report/team/cp3_self_review.md', 'report/team/pilot_plan.yaml',
                 'report/team/phieu_cham.md']
        for name in names:
            original = subprocess.check_output(['git', 'show', 'HEAD:' + name]).decode('utf-8')
            self.assertEqual(original.replace('\r\n', '\n'),
                             (Path('..') / name).read_text(encoding='utf-8'), name)
        template = subprocess.check_output(
            ['git', 'show', 'ed89502:report/team/MSSV_HoTen.md'])
        self.assertEqual(Path('../report/team/MSSV_HoTen.md').read_bytes(), template)
        error_report = Path('../report/team/bang_loi.md').read_text(encoding='utf-8')
        old_report = subprocess.check_output(
            ['git', 'show', 'HEAD:report/team/bang_loi.md']).decode('utf-8')
        for number in range(2, 8):
            pattern = r'^## ' + str(number) + r'\. .*?(?=^## \d+\.|\Z)'
            self.assertEqual(re.search(pattern, error_report, re.M | re.S).group().strip(),
                             re.search(pattern, old_report, re.M | re.S).group().strip())
        section3 = error_report.split('## 3.', 1)[1].split('## 4.', 1)[0]
        final_labels = dict(re.findall(r'^\| (\d{2}) \| ([USCLH]) — ', section3, re.M))
        self.assertEqual(len(final_labels), 20)
        self.assertIn('CONFIRMED — 20/20', error_report)
        self.assertIn('Bằng chứng đánh giá độc lập: PENDING', error_report)
        self.assertNotIn('20 dòng đánh giá để trống', error_report)
        base = Path('../report/team')
        inputs = dict(
            team=Path('../TEAM.md').read_text(encoding='utf-8'),
            group=(base / 'group_report.md').read_text(encoding='utf-8'),
            index=(base / 'README.md').read_text(encoding='utf-8'),
            personal=(base / '2A202603552_NguyenThiThuyDung.md').read_text(encoding='utf-8'),
            review_rows=table_by_first_column((base / 'cp3_self_review.md').read_text(encoding='utf-8'),
                                             'Case ID'),
            final_labels=final_labels,
            current_files={p.name for p in base.iterdir() if p.is_file()},
            expected_tests={name: unittest.defaultTestLoader.loadTestsFromName(module).countTestCases()
                            for name, module in [('CP1', 'test_cp1'), ('CP2', 'test_cp2'),
                                                 ('CP4', 'test_cp4'), ('CP5', 'test_cp5')]})
        self.assertEqual(submission_metadata_issues(**inputs), [])
        # Kiểm tra âm: validator phải bắt lỗi metadata, không chỉ chấp nhận tài liệu mới.
        mutations = [
            dict(team=inputs['team'].replace('2A202603552', 'WRONG_ID')),
            dict(group=inputs['group'].replace('| CP4 | 25 | 25 | 0 |', '| CP4 | 24 | 24 | 0 |')),
            dict(group=inputs['group'].replace('Independent Review Pending', 'Approved')),
            dict(personal=inputs['personal'].replace('Planned / Not Approved', 'Approved')),
            dict(index=inputs['index'].replace('`MSSV_HoTen.md`', '`missing.md`')),
            dict(review_rows=[{**r, 'Self-review label': ''} for r in inputs['review_rows']]),
        ]
        for mutation in mutations:
            with self.subTest(fields=sorted(mutation)):
                self.assertTrue(submission_metadata_issues(**{**inputs, **mutation}))
        self.assertIn('PENDING EXTERNAL REVIEW', self.spec)
        self.assertIn('Planned / Not Approved', self.dossier)
        self.assertIn('không phải điểm chính thức', self.spec)

    def test_e13_missing_empty_review_and_immutable_input(self):
        q = self.reqs.copy(deep=True)
        before = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                  for name in ['logix_requests.csv', 'logix_runs.csv']}
        summarize_kpis(q)
        assert_frame_equal(q, self.reqs)
        self.assertEqual(before, {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in before})
        no_reviews = q.assign(duoc_xem_lai=0, quyet_dinh_xem_lai='')
        self.assertIsNone(summarize_kpis(no_reviews)['KPI-02']['rate'])
        for bad in [q.iloc[0:0], q.assign(request_id='duplicate'),
                    q.assign(dong_trong_24h=2), q.assign(mo_lai_trong_7_ngay=float('nan')),
                    q.drop(columns='duoc_xem_lai'), q.assign(quyet_dinh_xem_lai='')]:
            with self.assertRaises(ValueError):
                summarize_kpis(bad)

    def test_e14_rework_and_volume_risk_baselines(self):
        value = self.kpi['Rework baseline pilot']
        self.assertEqual((value['numerator'], value['denominator']), (48, 982))
        self.assertLess(value['rate'], .07)
        self.assertIn(vn(value['rate'] * 100, 4) + '%', self.risks['RISK-01']['Early Warning Indicator'])
        flow = self.plan['feasibility']['flow_estimate']
        target = self.plan['primary_metric']['raw_n_total']
        shortfall = target - flow['weekday_only_20day_raw_80pct_capture']
        self.assertIn(str(int(shortfall)), self.risks['RISK-04']['Quantified Impact'])
        self.assertIn(str(flow['new_28day_expected_raw_80pct_capture']), self.risks['RISK-04']['Quantified Impact'])

    def test_e15_markdown_no_placeholder_or_forbidden_term(self):
        for text in [self.spec, self.dossier]:
            for header, rows in markdown_tables(text):
                for value in header + [cell for row in rows for cell in row.values()]:
                    self.assertNotIn(value.strip(), {'...', '?', 'TODO', 'TBD'})
            self.assertNotIn('production', text.lower())
            self.assertNotIn('chúng tôi', text.lower())
            self.assertNotIn('Biểu mẫu chưa hoàn thành', text)
        self.assertEqual(len(self.spec_rows), 5)
        self.assertIn('sampling_frame=targeted', self.spec)
        self.assertIn('không gộp thẳng', self.spec)


if __name__ == '__main__':
    unittest.main()
