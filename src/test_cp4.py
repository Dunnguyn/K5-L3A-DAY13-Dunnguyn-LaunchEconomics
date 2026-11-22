"""CP4 QA: phép tính độc lập, biên, CSV lab, YAML và bảo toàn CP1–CP3.

Chạy từ src: python -m unittest -v test_cp1 test_cp2 test_cp4.
Không chạy randomization hoặc ghi dữ liệu pilot.
"""
import ast
import contextlib
import csv
from datetime import date, timedelta
import hashlib
import io
import math
from pathlib import Path
import re
import subprocess
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal
from scipy.stats import norm
import yaml

import lab13 as lab


class CP4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
        cls.result = lab.phan_tich_cp4(cls.reqs)
        cls.plan_path = Path('../report/team/pilot_plan.yaml')
        cls.plan_text = cls.plan_path.read_text(encoding='utf-8')
        cls.plan = yaml.safe_load(cls.plan_text)['pilot']

    def test_d01_sample_size_independent_formula(self):
        for p1, p2, alpha, power in [(.70, .75, .05, .8), (.2, .3, .01, .9),
                                     (.1, .15, .1, .85), (.8, .7, .05, .8)]:
            pb = (p1 + p2) / 2
            continuous = ((norm.isf(alpha / 2) * math.sqrt(2 * pb * (1 - pb))
                           + norm.ppf(power) * math.sqrt(p1*(1-p1)+p2*(1-p2)))
                          / abs(p2-p1)) ** 2
            actual = lab.co_mau(p1, p2, alpha, power)
            self.assertEqual(actual, math.ceil(continuous))
            self.assertGreaterEqual(actual, continuous)
            self.assertLess(actual - continuous, 1)
        self.assertLess(abs(lab.co_mau(.7, .75) / 1251 - 1), .02)

    def test_d02_staff_design_effect(self):
        self.assertAlmostEqual(lab.design_effect(75), 2.48)
        for m in [1, 2, 75, 299, 10000]:
            self.assertEqual(lab.design_effect(m, 0), 1)
            self.assertAlmostEqual(lab.design_effect(m, .03), .97 + .03*m)

    def test_d03_required_staff_and_raw_ceil(self):
        d = self.result
        raw = d['raw_required_5pp']
        n = lab.co_mau(.7, .75)
        self.assertGreaterEqual(raw / lab.design_effect(75), n)
        self.assertLess((raw - 1) / lab.design_effect(75), n)
        staff = d['staff_per_arm_5pp']
        self.assertGreaterEqual(staff * 75, raw)
        self.assertLess((staff - 1) * 75, raw)
        self.assertEqual((raw, staff, d['staff_total_5pp']), (3103, 42, 84))
        self.assertGreater(d['staff_total_5pp'], 40)
        self.assertEqual(d['staff_allocated_raw_5pp'], 3150)

    def test_d04_fixed_clusters_limit(self):
        last = 0
        for m in [1, 75, 299, 1000, 1000000]:
            ne = lab.effective_sample_size(20, m)
            self.assertGreater(ne, last)
            self.assertLess(ne, 20 / .02)
            last = ne
        self.assertTrue(math.isinf(lab.minimum_requests_per_cluster(1000, 20)))
        self.assertTrue(math.isinf(lab.minimum_requests_per_cluster(self.result['n_5pp'], 20)))

    def test_d05_depot_ceiling(self):
        for m in [1, 75, 299, 100000]:
            self.assertLess(lab.effective_sample_size(6, m), 300)
        self.assertTrue(math.isinf(lab.minimum_requests_per_cluster(1251, 6)))

    def test_d06_mde_sample_monotonicity(self):
        n6 = lab.co_mau(.7, .76)
        self.assertLess(abs(n6 / 859 - 1), .02)
        self.assertLess(n6, lab.co_mau(.7, .75))
        self.assertGreater(lab.co_mau(.7, .76, power=.9), n6)
        self.assertGreater(lab.co_mau(.7, .76, alpha=.01), n6)
        self.assertEqual(lab.co_mau(.76, .7), n6)

    def test_d07_minimum_cluster_requests(self):
        n = self.result['n_6pp']
        m = lab.minimum_requests_per_cluster(n, 20)
        self.assertEqual(m, 299)
        self.assertGreaterEqual(lab.effective_sample_size(20, m), n)
        self.assertLess(lab.effective_sample_size(20, m - 1), n)
        self.assertAlmostEqual(lab.design_effect(m), 6.96)
        self.assertEqual(2 * 20 * m, 11960)
        # ICC=0 không có trần; kiểm tra tối thiểu trên nhiều cấu hình.
        for icc in [0, .005, .02, .1]:
            for target in [1, 19, 20, 39, 99]:
                c = 20
                m = lab.minimum_requests_per_cluster(target, c, icc)
                self.assertTrue(math.isfinite(m))
                self.assertGreaterEqual(lab.effective_sample_size(c, m, icc), target)
                if m > 1:
                    self.assertLess(lab.effective_sample_size(c, m - 1, icc), target)

    def test_d08_power_independent_normal_distribution(self):
        ne = self.result['effective_6pp']
        z = norm.isf(.025)
        for target in [.75, .76]:
            h = 2 * (math.asin(math.sqrt(target)) - math.asin(math.sqrt(.7)))
            shift = h * math.sqrt(ne / 2)
            expected = norm.sf(z - shift) + norm.cdf(-z - shift)
            self.assertAlmostEqual(lab.approximate_power(.7, target, ne), expected, places=10)
        self.assertAlmostEqual(self.result['power_true_5pp'], .64, delta=.01)
        self.assertAlmostEqual(self.result['power_true_6pp'], .80, delta=.01)
        self.assertLess(self.result['power_true_5pp'], .8)

    def test_d09_safety_baseline_independent_csv(self):
        with open('logix_requests.csv', encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        for name, subset in [('overall', rows), ('pilot', [r for r in rows
                               if r['loai'] in {'noi_dia', 'hang_nang'}])]:
            actual = self.result['safety'][name]
            count = sum(int(r['mo_lai_trong_7_ngay']) for r in subset)
            self.assertEqual(actual['n'], len(subset))
            self.assertEqual(actual['reopened'], count)
            self.assertEqual(actual['rate'], count / len(subset))
        self.assertEqual(self.result['safety']['overall']['reopened'], 51)
        self.assertEqual(self.result['safety']['overall']['n'], 1200)
        self.assertEqual(self.result['safety']['pilot']['reopened'], 39)
        self.assertEqual(self.result['safety']['pilot']['n'], 982)

    def test_d10_yaml_parse(self):
        self.assertIsInstance(yaml.safe_load(self.plan_text), dict)
        self.assertIsInstance(self.plan, dict)

    def test_d11_template_fields_and_types_preserved(self):
        template = yaml.safe_load(subprocess.check_output(
            ['git', 'show', 'HEAD:report/team/pilot_plan.yaml']).decode('utf-8'))['pilot']
        def check(original, actual):
            if isinstance(original, dict):
                self.assertIsInstance(actual, dict)
                self.assertTrue(set(original).issubset(actual))
                for key in original:
                    check(original[key], actual[key])
            elif isinstance(original, list):
                self.assertIsInstance(actual, list)
            elif original == '?':
                self.assertIsNotNone(actual)
            else:
                self.assertIsInstance(actual, type(original))
        check(template, self.plan)
        self.assertIs(self.plan['assignment']['randomized'], True)
        self.assertIsInstance(self.plan['primary_metric']['n_per_arm'], int)
        self.assertEqual(self.plan['status'], 'Planned')

    def test_d12_no_placeholders_in_yaml_tree(self):
        def check(value):
            self.assertIsNotNone(value)
            if isinstance(value, dict):
                for key, item in value.items():
                    check(key)
                    check(item)
            elif isinstance(value, list):
                self.assertGreater(len(value), 0)
                for item in value:
                    check(item)
            elif isinstance(value, str):
                self.assertTrue(value.strip())
                self.assertNotIn('?', value)
                self.assertNotRegex(value.strip(), r'^(TODO|TBD|\.\.\.)$')
        check(self.plan)

    def test_d13_stop_rules_four_clauses(self):
        rules = self.plan['stop_rules']
        self.assertGreaterEqual(len(rules), 3)
        for i, rule in enumerate(rules, start=1):
            self.assertIn(f'SR-0{i}', rule)
            self.assertRegex(rule, r'NẾU .+ TRONG .+ THÌ .+ KHÔNG THÌ .+')
            self.assertIn('Giám đốc vận hành', rule)
            self.assertRegex(rule, r'\d')
        self.assertIn('khẩn cấp ngay', rules[0])
        self.assertIn('0.02', rules[0])
        self.assertIn('0.06', rules[0])
        self.assertIn('>=200', rules[0])
        self.assertIn('8000', rules[1])
        self.assertIn('hai tuần liên tiếp', rules[1])
        self.assertIn('>=100', rules[1])
        self.assertIn('0.40', rules[2])
        self.assertIn('>=100', rules[2])

    def test_d14_identifiability_and_randomization(self):
        for key in ['concurrent_control', 'spillover_risk', 'predeclared']:
            self.assertGreater(len(self.plan['identifiability'][key]), 100)
        a = self.plan['assignment']
        self.assertEqual(a['unit'], 'staff')
        self.assertEqual(a['control_share'], .5)
        self.assertEqual(a['clusters_per_arm'], 20)
        self.assertIsInstance(a['seed'], int)
        self.assertIn('PCG64', a['stratification'])
        self.assertEqual(a['status'], 'Planned_not_executed')
        self.assertIn('ITT', self.plan['analysis_plan']['population'])
        self.assertIn('CR2', self.plan['analysis_plan']['estimator'])

    def test_d15_primary_metric_math_matches_yaml(self):
        p = self.plan['primary_metric']
        self.assertEqual(p['name'], 'dong_trong_24h_khong_mo_lai_7_ngay')
        self.assertEqual((p['baseline'], p['mde'], p['alpha'], p['power']), (.70, .06, .05, .80))
        self.assertEqual(p['n_per_arm'], lab.co_mau(p['baseline'], p['baseline']+p['mde'],
                                                 p['alpha'], p['power']))
        m, c = p['min_requests_per_staff'], p['clusters_per_arm']
        self.assertEqual(p['design_effect'], lab.design_effect(m))
        self.assertEqual(p['raw_n_per_arm'], c * m)
        self.assertEqual(p['raw_n_total'], 2 * c * m)
        self.assertGreaterEqual(lab.effective_sample_size(c, m), p['n_per_arm'])

    def test_d16_scope_and_source_roster_limitations(self):
        self.assertIn('Chỉ noi_dia và hang_nang', self.plan['scope'])
        self.assertIn('loại quoc_te', self.plan['scope'])
        self.assertIn('doi_tac', self.plan['scope'])
        partner = self.reqs.loc[self.reqs['loai'].eq('doi_tac')]
        success_percent = 100 * partner['ket_qua'].eq('thanh_cong').mean()
        self.assertIn(f'{success_percent:.2f}%', self.plan['scope'])
        self.assertEqual(self.reqs['staff_id'].nunique(), 20)
        self.assertEqual(self.reqs['depot'].nunique(), 6)
        self.assertIs(self.plan['feasibility']['roster_verified'], False)
        self.assertIn('20 staff', self.plan['assignment']['prerequisite'])

    def test_d17_no_input_mutation(self):
        q = self.reqs.copy(deep=True)
        names = ['logix_requests.csv', 'logix_runs.csv', '../report/team/cp3_reviewer_summary.md']
        hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names}
        lab.safety_baseline(q)
        lab.phan_tich_cp4(q)
        assert_frame_equal(q, self.reqs)
        self.assertEqual(hashes, {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names})

    def test_d18_cp1_cp2_functions_and_tests_preserved(self):
        before = ast.parse(subprocess.check_output(['git', 'show', 'HEAD:src/lab13.py']).decode('utf-8'))
        after = ast.parse(Path('lab13.py').read_text(encoding='utf-8'))
        current = {n.name: ast.dump(n) for n in after.body if isinstance(n, ast.FunctionDef)}
        for node in before.body:
            if isinstance(node, ast.FunctionDef):
                self.assertEqual(ast.dump(node), current[node.name])
        for name in ['test_cp1.py', 'test_cp2.py', 'lab13_starter.py']:
            baseline = subprocess.check_output(['git', 'show', 'HEAD:src/' + name]).decode('utf-8')
            self.assertEqual(baseline, Path(name).read_text(encoding='utf-8'))

    def test_d19_invalid_design_parameters(self):
        for bad in [-.1, 1.1, math.nan, math.inf, True, '0.7', None]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                lab.co_mau(bad, .75)
        for kwargs in [dict(alpha=0), dict(alpha=1), dict(alpha=math.nan),
                       dict(power=.5), dict(power=1), dict(power=True)]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                lab.co_mau(.7, .75, **kwargs)
        with self.assertRaises(ValueError):
            lab.co_mau(.7, .7)
        for bad in [0, -1, 1.5, True, math.inf]:
            with self.assertRaises(ValueError):
                lab.design_effect(bad)
            with self.assertRaises(ValueError):
                lab.effective_sample_size(bad, 10)
        for bad in [-.1, 1, math.nan, True]:
            with self.assertRaises(ValueError):
                lab.design_effect(75, bad)
        with self.assertRaises(ValueError):
            lab.minimum_requests_per_cluster(0, 20)
        with self.assertRaises(ValueError):
            lab.approximate_power(.7, .75, 0)

    def test_d20_invalid_safety_data(self):
        for mutate in [lambda q: q.drop(columns='loai'),
                       lambda q: q.iloc[0:0],
                       lambda q: q.assign(mo_lai_trong_7_ngay=2),
                       lambda q: q.assign(mo_lai_trong_7_ngay=float('nan')),
                       lambda q: q.assign(request_id='same'),
                       lambda q: q.assign(loai='invalid'),
                       lambda q: q.assign(loai='quoc_te')]:
            with self.assertRaises(ValueError):
                lab.safety_baseline(mutate(self.reqs.copy(deep=True)))

    def test_d21_schedule_followup_and_capacity(self):
        schedule = self.plan['schedule']
        self.assertEqual(self.plan['rollout'], [.10, .25, .50])
        for stage, count in [('ramp_10', 4), ('ramp_25', 10), ('main_50', 20)]:
            self.assertEqual(schedule[stage]['treatment_staff'], count)
        main = schedule['main_50']
        days = (date.fromisoformat(main['end']) - date.fromisoformat(main['start'])).days + 1
        self.assertEqual(days, self.plan['feasibility']['planned_collection_days'])
        followup = date.fromisoformat(schedule['final_followup_end'])
        self.assertGreaterEqual(followup, date.fromisoformat(main['end']) + timedelta(days=8))
        qa_end = date.fromisoformat(schedule['data_qa_end'])
        self.assertGreater(qa_end, followup)
        self.assertGreater(date.fromisoformat(self.plan['decision_date']), qa_end)
        self.assertGreater(date.fromisoformat(schedule['ramp_10']['start']), date(2026, 11, 22))
        f = self.plan['feasibility']
        self.assertAlmostEqual(f['required_eligible_requests_per_day_total'], 11960 / days, places=5)
        self.assertAlmostEqual(f['estimated_eligible_requests_per_day_lab_assumption'],
                               1500 * len(self.reqs[self.reqs.loai.isin(['noi_dia', 'hang_nang'])]) / len(self.reqs))

    def test_d22_print_and_table_accounting(self):
        table = self.result['d1'].set_index('Question')
        for key in ['a', 'b', 'e']:
            row = table.loc[key]
            self.assertAlmostEqual(row['Raw N/arm'] / row['DE'], row['Effective N/arm'])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            lab.in_ket_qua_cp4(self.reqs)
        for text in ['D1:', 'a)', 'b)', 'c)', 'd)', 'e)', 'D3:', 'Power']:
            self.assertIn(text, output.getvalue())

    def test_d23_six_depot_flow_estimate_and_shortfall(self):
        from fractions import Fraction
        f = self.plan['feasibility']['flow_estimate']
        eligible_share = Fraction(int(self.reqs.loai.isin(['noi_dia', 'hang_nang']).sum()),
                                  len(self.reqs))
        flow = Fraction(f['network_requests_per_day'] * f['pilot_depots'], f['network_depots'])
        eligible_daily = flow * eligible_share
        capture = Fraction(str(f['capture_rate_scenario']))
        self.assertEqual(f['status'], 'assumption_not_observed')
        self.assertEqual(f['total_requests_per_day_six_depots'], float(flow))
        self.assertEqual(f['eligible_requests_per_day_six_depots'], float(eligible_daily))
        target = self.plan['primary_metric']['raw_n_total']
        old_total = 14 * eligible_daily
        self.assertEqual(f['old_14day_expected_raw'], float(old_total))
        self.assertEqual(f['old_14day_shortfall_raw'], float(target - old_total))
        self.assertLess(old_total, target)
        self.assertLess(old_total / 40, self.plan['primary_metric']['min_requests_per_staff'])
        for rate, key in [(Fraction(1), 'minimum_coverage_days_full_capture'),
                          (capture, 'minimum_coverage_days_80pct_capture')]:
            days = f[key]
            self.assertGreaterEqual(days * eligible_daily * rate, target)
            self.assertLess((days - 1) * eligible_daily * rate, target)
        self.assertEqual(f['new_28day_expected_raw_full_capture'], float(28 * eligible_daily))
        self.assertEqual(f['new_28day_expected_raw_80pct_capture'], float(28 * eligible_daily * capture))
        self.assertGreaterEqual(28 * eligible_daily * capture, target)
        self.assertEqual(f['weekday_only_20day_raw_80pct_capture'], float(20 * eligible_daily * capture))
        self.assertLess(20 * eligible_daily * capture, target)

    def test_d24_staffing_is_prerequisite_not_observed(self):
        f = self.plan['feasibility']['flow_estimate']
        uniform_staff = 40 * f['pilot_depots'] / f['network_depots']
        self.assertEqual(f['staff_uniform_estimate_six_depots'], uniform_staff)
        self.assertEqual(f['required_staff_six_depots'],
                         2 * self.plan['primary_metric']['clusters_per_arm'])
        self.assertEqual(f['additional_staff_to_verify'], f['required_staff_six_depots'] - uniform_staff)
        self.assertIs(self.plan['feasibility']['roster_verified'], False)
        self.assertTrue(math.isinf(lab.minimum_requests_per_cluster(self.result['n_6pp'], 10)))
        self.assertLess(10 / .02, self.result['n_6pp'])
        per_staff = f['new_28day_expected_raw_80pct_capture'] / f['required_staff_six_depots']
        self.assertAlmostEqual(f['new_28day_average_per_staff_80pct_capture'], per_staff)
        self.assertGreater(per_staff, self.plan['primary_metric']['min_requests_per_staff'])

    def test_d25_gate_maturity_and_enrollment_extension(self):
        s = self.plan['schedule']
        for previous, following in [('ramp_10', 'ramp_25'), ('ramp_25', 'main_50')]:
            maturity = date.fromisoformat(s[previous]['end']) + timedelta(days=8)
            self.assertGreater(date.fromisoformat(s[following]['start']), maturity)
        start = date.fromisoformat(s['main_50']['start'])
        end = date.fromisoformat(s['main_50']['end'])
        self.assertEqual(start.weekday(), 0)
        self.assertEqual(end.weekday(), 6)
        self.assertEqual((end - start).days + 1, 28)
        # Hai cohort tuần cuối, mỗi cohort đủ 1 ngày đóng + 7 ngày theo dõi.
        for cohort_end in [end - timedelta(days=7), end]:
            self.assertLess(cohort_end + timedelta(days=8), date.fromisoformat(self.plan['decision_date']))
        self.assertGreaterEqual(date.fromisoformat(self.plan['decision_date']), end + timedelta(days=11))
        e = s['extension_policy']
        self.assertEqual(e['planned_main_days'], 28)
        self.assertEqual(e['extension_block_days'], 7)
        maximum = date.fromisoformat(e['maximum_main_end_if_start_unchanged'])
        self.assertEqual((maximum - start).days + 1, e['maximum_main_days'])
        self.assertEqual(e['maximum_main_days'], 42)
        self.assertEqual(date.fromisoformat(e['maximum_followup_end_if_start_unchanged']),
                         maximum + timedelta(days=8))
        self.assertEqual(date.fromisoformat(e['maximum_decision_if_start_unchanged']),
                         maximum + timedelta(days=11))
        for text in ['outcome efficacy', 'không kéo dài vì p-value', 'Inconclusive', 'safety stop']:
            self.assertIn(text, e['rule'])


if __name__ == '__main__':
    unittest.main()
