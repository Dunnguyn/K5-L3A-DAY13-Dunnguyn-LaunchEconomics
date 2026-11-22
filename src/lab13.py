"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
from numbers import Integral, Real
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def _kiem_tra_k(k):
    if k is not None and (isinstance(k, bool) or not isinstance(k, Integral) or k < 1):
        raise ValueError('k/max_lan_chay phải là số nguyên dương hoặc None')


def _kiem_tra_p_k(p, k):
    if isinstance(p, bool) or not isinstance(p, Real) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('p phải là số hữu hạn trong [0, 1]')
    _kiem_tra_k(k)


def so_lan_chay_ky_vong(p, k=None):
    """Trả E[N] (lần/yêu cầu), với xác suất p độc lập, không đổi mỗi lần.

    p thuộc [0, 1]; k nguyên dương hoặc None (thử đến khi thành công).
    p=0 cho E[N]=k nếu hữu hạn, ngược lại là math.inf.
    """
    _kiem_tra_p_k(p, k)
    if k == 1:
        return 1.0
    if p == 0:
        return math.inf if k is None else float(k)
    return 1 / p if k is None else ti_le_thanh_cong(p, k) / p


def ti_le_thanh_cong(p, k=None):
    """Trả xác suất thành công [0, 1] với các lần thử độc lập có cùng p.

    p thuộc [0, 1]; k nguyên dương hoặc None. Không giới hạn: xác suất
    bằng 1 nếu p>0, bằng 0 nếu p=0. Dùng log1p/expm1 tránh mất độ chính xác.
    """
    _kiem_tra_p_k(p, k)
    if k == 1:
        return float(p)
    if p == 0:
        return 0.0
    if k is None or p == 1:
        return 1.0
    return -math.expm1(k * math.log1p(-p))


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Trả E[N]/P(success), bội số giá một lần chạy (chi phí mỗi lần bằng nhau).

    p thuộc [0, 1], k nguyên dương hoặc None; giả định các lần thử độc lập.
    p=0 không có thành công nên trả math.inf, không chia cho 0.
    """
    _kiem_tra_p_k(p, k)
    if p == 0:
        return math.inf
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả chi phí VND và CPS VND/việc thành công; không sửa DataFrame đầu vào.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    - Giới hạn k: giữ attempt <= k; yêu cầu có so_lan_chay > k chuyển nhân viên,
      xoá phút xem lại/làm lại theo quy ước đề (không suy đoán kết quả mới).
    - chay_lai là phần đã nằm trong token + tool, không cộng thêm vào tong.
    - Không thành công: cps=math.inf; không có yêu cầu: hoa_don_moi_yc=0.
      Giá/hệ số phải hữu hạn, không âm; dữ liệu sai/thiếu/trùng báo ValueError.
    """
    _kiem_tra_k(max_lan_chay)
    for ten, gia in dict(gia_vao=gia_vao, gia_ra=gia_ra, gia_tool=gia_tool,
                         luong_phut=luong_phut, he_so_xem_lai=he_so_xem_lai,
                         he_so_lam_lai=he_so_lam_lai).items():
        if isinstance(gia, bool) or not isinstance(gia, Real) or not math.isfinite(gia) or gia < 0:
            raise ValueError(f'{ten} phải là số hữu hạn, không âm')
    cot_runs = ['run_id', 'request_id', 'attempt', 'tokens_in', 'tokens_out', 'tool_calls', 'status']
    cot_reqs = ['request_id', 'so_lan_chay', 'ket_qua',
                'phut_xem_lai_simulated', 'phut_lam_lai_simulated']
    for ten, df, cot in [('runs', runs, cot_runs), ('reqs', reqs, cot_reqs)]:
        if not isinstance(df, pd.DataFrame) or not set(cot).issubset(df.columns):
            raise ValueError(f'{ten} phải là DataFrame có các cột {cot}')
    reqs = reqs.copy(deep=True)
    runs = runs.loc[runs['request_id'].isin(reqs['request_id'])].copy(deep=True)
    for ten, df, cot in [('runs', runs, cot_runs), ('reqs', reqs, cot_reqs)]:
        if df[cot].isna().any().any() or df['request_id'].eq('').any():
            raise ValueError(f'{ten}: dữ liệu bắt buộc bị thiếu')
    if reqs['request_id'].duplicated().any() or runs['run_id'].duplicated().any() or runs.duplicated(['request_id', 'attempt']).any():
        raise ValueError('request_id, run_id hoặc (request_id, attempt) bị trùng')
    for df, cot in [(runs, ['attempt', 'tokens_in', 'tokens_out', 'tool_calls']),
                    (reqs, ['so_lan_chay', 'phut_xem_lai_simulated', 'phut_lam_lai_simulated'])]:
        for ten in cot:
            if not all(isinstance(x, Real) and not isinstance(x, bool) and math.isfinite(x) and x >= 0
                       for x in df[ten]):
                raise ValueError(f'{ten} phải là số hữu hạn, không âm')
            if ten in ['attempt', 'so_lan_chay'] and not ((df[ten] >= 1) & (df[ten] % 1 == 0)).all():
                raise ValueError(f'{ten} phải là số nguyên dương')
    if not runs['status'].isin(['ok', 'loi']).all() or not reqs['ket_qua'].isin(['thanh_cong', 'lam_lai', 'chuyen_nhan_vien']).all():
        raise ValueError('status hoặc ket_qua không hợp lệ')
    counts = runs.groupby('request_id')['attempt'].agg(['size', 'min', 'max'])
    aligned = counts.reindex(reqs['request_id'])
    if (aligned.isna().any().any() or
            not (aligned['size'].to_numpy() == reqs['so_lan_chay'].to_numpy()).all() or
            not (aligned['min'] == 1).all() or not (aligned['max'] == aligned['size']).all()):
        raise ValueError('Trace phải đủ attempt 1..so_lan_chay cho mỗi yêu cầu được chọn')
    if max_lan_chay is not None:
        runs = runs.loc[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    token, tool = float(tien_token.sum()), float(tien_tool.sum())
    xem_lai = float(reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai)
    lam_lai = float(reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai)
    tong = token + tool + xem_lai + lam_lai
    thanh_cong = int(reqs['ket_qua'].eq('thanh_cong').sum())
    return dict(token=token, tool=tool,
                chay_lai=float((tien_token + tien_tool)[runs['attempt'] > 1].sum()),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong, thanh_cong=thanh_cong,
                cps=tong / thanh_cong if thanh_cong else math.inf,
                hoa_don_moi_yc=(token + tool) / len(reqs) if len(reqs) else 0.0)


def phan_tich_theo_loai(runs, reqs):
    """Bảng A3; tỷ lệ ok mỗi attempt có mẫu số là số run đến attempt đó."""
    rows = []
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        q = reqs.loc[reqs['loai'] == loai]
        r = runs.loc[runs['request_id'].isin(q['request_id'])]
        m = mo_hinh(runs, q)
        row = dict(loai=loai, so_yc=len(q), thanh_cong=m['thanh_cong'],
                   ti_le=100 * m['thanh_cong'] / len(q) if len(q) else 0.0,
                   lan_chay=len(r) / len(q) if len(q) else 0.0,
                   cps=m['cps'], so_baseline=m['cps'] / BASELINE, tong=m['tong'])
        for k in (1, 2, 3):
            attempt = r.loc[r['attempt'] == k]
            ok = int(attempt['status'].eq('ok').sum())
            row[f'ok_{k}'] = ok
            row[f'n_{k}'] = len(attempt)
            row[f'phan_tram_ok_{k}'] = 100 * ok / len(attempt) if len(attempt) else 0.0
            row[f'thanh_cong_den_{k}'] = int(q.loc[q['so_lan_chay'] <= k, 'ket_qua'].eq('thanh_cong').sum())
        rows.append(row)
    return pd.DataFrame(rows)


def phan_tich_co_dinh(runs, reqs):
    """Bảng A4: nhu cầu toàn doanh nghiệp × số thành công trong phạm vi / toàn mẫu.

    Giữ cơ cấu loại yêu cầu, kết quả và CPS biến đổi của mẫu ở cả hai khối lượng.
    Không cộng chi phí fallback vào CPS; không thay đổi A2.
    """
    q = reqs.loc[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    m = mo_hinh(runs, q)
    ty_le = m['thanh_cong'] / len(reqs) if len(reqs) else 0.0
    rows = []
    for volume in (45000, 22500):
        success = volume * ty_le
        fixed = 40000000 / success if success else math.inf
        rows.append(dict(nhu_cau=volume, thanh_cong=success, co_dinh=fixed,
                         bien_doi=m['cps'], tong=m['cps'] + fixed,
                         so_baseline=(m['cps'] + fixed) / BASELINE))
    return pd.DataFrame(rows)


# ---------- CP2 · Nhiệm vụ B · Phân tích độ nhạy ----------
def phan_tich_do_nhay(runs, reqs):
    """B1: baseline và 9 cú sốc, tính lại qua mo_hinh; không làm tròn số.

    tong: VND; cps/delta_vnd: VND/success; delta_pct: %. Các chỉ số chi phí
    có phần simulated. Hệ số phút thay đổi chi phí, không mô phỏng lại chất lượng.
    """
    kich_ban = [
        ('B1-01', 'Token ×2', dict(gia_vao=52, gia_ra=260)),
        ('B1-02', 'Token ×0,5', dict(gia_vao=13, gia_ra=65)),
        ('B1-03', 'Review ×2', dict(he_so_xem_lai=2.0)),
        ('B1-04', 'Review ×0,5', dict(he_so_xem_lai=0.5)),
        ('B1-05', 'Rework ×2', dict(he_so_lam_lai=2.0)),
        ('B1-06', 'Rework ×0,5', dict(he_so_lam_lai=0.5)),
        ('B1-07', 'Lương +25%', dict(luong_phut=2500)),
        ('B1-08', 'Tối đa 2 lần', dict(max_lan_chay=2)),
        ('B1-09', 'Tối đa 1 lần', dict(max_lan_chay=1)),
    ]
    goc = mo_hinh(runs, reqs)
    if not math.isfinite(goc['cps']) or goc['cps'] <= 0:
        raise ValueError('Độ nhạy cần baseline CPS hữu hạn, dương')
    rows = []
    for ma, ten, kw in [('B1-00', 'Baseline', {})] + kich_ban:
        m = mo_hinh(runs, reqs, **kw)
        rows.append(dict(id=ma, kich_ban=ten, tham_so=str(kw), tong=m['tong'],
                         thanh_cong=m['thanh_cong'], cps=m['cps'],
                         delta_vnd=m['cps'] - goc['cps'],
                         delta_pct=(m['cps'] / goc['cps'] - 1) * 100))
    return pd.DataFrame(rows)


def phan_tich_ket_hop(runs, reqs):
    """B2: cộng tác động trên CPS; ranking các cú sốc bất lợi đã chỉ định.

    interaction (VND/success) xấp xỉ 0 khi mẫu số không đổi; không phải
    hệ số nhạy chuẩn hóa vì lương +25% khác quy mô token/review/rework +100%.
    """
    b1 = phan_tich_do_nhay(runs, reqs).set_index('id')
    m = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2.0)
    delta = float(m['cps'] - b1.loc['B1-00', 'cps'])
    rieng = b1.loc[['B1-01', 'B1-03'], 'delta_vnd'].sum()
    ranking = b1.loc[['B1-01', 'B1-03', 'B1-05', 'B1-07']].sort_values(
        'delta_pct', ascending=False).head(3).reset_index()
    return dict(tong=m['tong'], thanh_cong=m['thanh_cong'], cps=m['cps'],
                delta_vnd=delta, delta_pct=float(delta / b1.loc['B1-00', 'cps'] * 100),
                tong_tac_dong_rieng=float(rieng), interaction=float(delta - rieng),
                ranking=ranking)


def phan_tich_gioi_han_chay(runs, reqs):
    """B3: agent CPS khác system/request; fallback giả định 12.000 VND/unresolved.

    Giữ nguyên rework của mo_hinh dù có thể chồng fallback; không gồm fixed cost.
    Quy ước cắt trace và xóa phút của yêu cầu vượt giới hạn nằm trong mo_hinh.
    """
    rows = []
    for k in (1, 2, 3):
        m = mo_hinh(runs, reqs, max_lan_chay=k)
        unresolved = len(reqs) - m['thanh_cong']
        fallback = unresolved * BASELINE
        system = m['tong'] + fallback
        rows.append(dict(max_attempts=k, agent_cost=m['tong'], successes=m['thanh_cong'],
                         unresolved=unresolved, fallback=fallback, system_cost=system,
                         system_per_request=system / len(reqs) if len(reqs) else 0.0,
                         agent_cps=m['cps']))
    return pd.DataFrame(rows)


def phan_tich_xem_lai_100(runs, reqs):
    """B4: review 100% yêu cầu có >=1 run ok trong noi_dia + hang_nang.

    Thay thế hoàn toàn phút simulated cũ bằng 5 phút/review, 9 phút/rework
    hoặc mean simulated của các ca ket_qua=lam_lai TOÀN MẪU (đúng đề).
    Báo thêm mean/median riêng phạm vi; giữ token/tool của mọi run và success
    gốc. CPS không gồm fallback/fixed; break-even = ngân sách còn lại / n_review/lương.
    """
    q = reqs.loc[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    m = mo_hinh(runs, q)
    r = runs.loc[runs['request_id'].isin(q['request_id'])]
    n_review = int(r.loc[r['status'].eq('ok'), 'request_id'].nunique())
    n_rework = int(q['ket_qua'].eq('lam_lai').sum())
    all_minutes = reqs.loc[reqs['ket_qua'].eq('lam_lai'), 'phut_lam_lai_simulated']
    scope_minutes = q.loc[q['ket_qua'].eq('lam_lai'), 'phut_lam_lai_simulated']
    if not m['thanh_cong'] or not n_review or all_minutes.empty or scope_minutes.empty:
        raise ValueError('B4 cần success, yêu cầu có run ok và ca lam_lai để ước lượng phút')
    mean = float(all_minutes.mean())
    technical = m['token'] + m['tool']
    rows = []
    for ten, minutes in [('9 phút theo đề', 9.0), ('Mean toàn mẫu làm tròn 1 số lẻ', round(mean, 1)),
                         ('Mean toàn mẫu đầy đủ', mean)]:
        review = n_review * 5 * LUONG_PHUT
        rework = n_rework * minutes * LUONG_PHUT
        total = technical + review + rework
        cps = total / m['thanh_cong']
        threshold = (BASELINE * m['thanh_cong'] - technical - rework) / (n_review * LUONG_PHUT)
        rows.append(dict(kich_ban=ten, phut_review=5.0, phut_rework=minutes,
                         technical=technical, review=review, rework=rework, tong=total,
                         cps=cps, so_baseline=cps / BASELINE, hoa_von_phut_review=threshold))
    return dict(so_yc=len(q), thanh_cong=m['thanh_cong'], n_review=n_review, n_rework=n_rework,
                n_rework_toan_mau=len(all_minutes), mean_toan_mau=mean,
                median_toan_mau=float(all_minutes.median()), mean_pham_vi=float(scope_minutes.mean()),
                median_pham_vi=float(scope_minutes.median()), bang=pd.DataFrame(rows))


# ---------- CP4 · Nhiệm vụ D · Thiết kế pilot, chưa triển khai ----------
def _cp4_real(value, name, lower, upper, closed=False):
    if (isinstance(value, bool) or not isinstance(value, Real)
            or not math.isfinite(value)
            or not (lower <= value <= upper if closed else lower < value < upper)):
        raise ValueError(f'{name}: giá trị hữu hạn ngoài miền cho phép')


def _cp4_positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 1:
        raise ValueError(f'{name} phải là số nguyên dương')


def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Mẫu mỗi arm, hai tỷ lệ độc lập, hai phía, phân bổ 1:1; ceil cuối cùng.

    Đây là xấp xỉ chuẩn cho thiết kế, không phải kết quả phân tích cluster.
    """
    from statistics import NormalDist
    for name, value in [('p1', p1), ('p2', p2)]:
        _cp4_real(value, name, 0, 1, closed=True)
    _cp4_real(alpha, 'alpha', 0, 1)
    _cp4_real(power, 'power', 0.5, 1)
    if p1 == p2:
        raise ValueError('Hai tỷ lệ phải khác nhau')
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
                     / (p2 - p1) ** 2)


def design_effect(m, icc=0.02):
    """Cụm bằng nhau: DE = 1 + (m-1) ICC, 0 <= ICC < 1."""
    _cp4_positive_int(m, 'm')
    _cp4_real(icc, 'ICC', 0, 1, closed=True)
    if icc == 1:
        raise ValueError('ICC phải nhỏ hơn 1')
    return 1 + (m - 1) * icc


def effective_sample_size(c, m, icc=0.02):
    """Raw c*m khác effective c*m/DE; trần c/ICC nếu ICC > 0."""
    _cp4_positive_int(c, 'c')
    return c * m / design_effect(m, icc)


def minimum_requests_per_cluster(n_effective, c, icc=0.02):
    """m nguyên tối thiểu; trả inf khi c/ICC không thể đạt yêu cầu."""
    _cp4_positive_int(c, 'c')
    _cp4_real(n_effective, 'n_effective', 0, math.inf)
    design_effect(1, icc)
    if icc > 0 and n_effective >= c / icc:
        return math.inf
    m = max(1, math.ceil(n_effective * (1 - icc) / (c - n_effective * icc)))
    # Kiểm tra hai phía tránh sai số float ngay tại biên nguyên.
    while effective_sample_size(c, m, icc) < n_effective:
        m += 1
    while m > 1 and effective_sample_size(c, m - 1, icc) >= n_effective:
        m -= 1
    return m


def approximate_power(p1, p2, n_effective, alpha=0.05):
    """Power xấp xỉ theo Cohen h; không thay suy luận cluster-aware hữu hạn."""
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize
    for name, value in [('p1', p1), ('p2', p2)]:
        _cp4_real(value, name, 0, 1, closed=True)
    _cp4_real(n_effective, 'n_effective', 0, math.inf)
    _cp4_real(alpha, 'alpha', 0, 1)
    return float(NormalIndPower().power(abs(proportion_effectsize(p1, p2)),
                                       nobs1=n_effective, alpha=alpha,
                                       ratio=1, alternative='two-sided'))


def safety_baseline(reqs):
    """D3: số đếm reopening từ trace lab giả lập; không sửa DataFrame.

    Không loại âm thầm các dòng thiếu outcome; dữ liệu không hợp lệ báo lỗi.
    """
    columns = {'request_id', 'loai', 'mo_lai_trong_7_ngay'}
    if not isinstance(reqs, pd.DataFrame) or not columns.issubset(reqs.columns):
        raise ValueError('Thiếu cột D3 bắt buộc')
    if (reqs.empty or reqs[list(columns)].isna().any().any()
            or reqs['request_id'].eq('').any() or reqs['request_id'].duplicated().any()
            or not reqs['mo_lai_trong_7_ngay'].isin([0, 1]).all()
            or not reqs['loai'].isin(['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']).all()):
        raise ValueError('D3 cần ID duy nhất, loại hợp lệ và outcome nhị phân đầy đủ')
    eligible = reqs.loc[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    if eligible.empty:
        raise ValueError('Không có yêu cầu trong phạm vi pilot')
    return {name: dict(n=len(q), reopened=int(q['mo_lai_trong_7_ngay'].sum()),
                       rate=float(q['mo_lai_trong_7_ngay'].mean()))
            for name, q in [('overall', reqs), ('pilot', eligible)]}


def phan_tich_cp4(reqs):
    """D1 a-e và D3; mọi số thiết kế được tính, không lấy observed làm effect."""
    n5, n6 = co_mau(0.70, 0.75), co_mau(0.70, 0.76)
    icc, c, m_staff = 0.02, 20, 75
    de_staff = design_effect(m_staff, icc)
    raw5 = math.ceil(n5 * de_staff)
    staff = math.ceil(raw5 / m_staff)
    m6 = minimum_requests_per_cluster(n6, c, icc)
    de6 = design_effect(m6, icc)
    ne6 = effective_sample_size(c, m6, icc)
    rows = [
        ['a', 'request', None, 1.0, n5, n5, 'Có nếu độc lập; spillover cần kiểm soát'],
        ['b', 'staff (m=75)', staff, de_staff, raw5, raw5 / de_staff,
         'Không: cần ' + str(2 * staff) + ' staff > 40'],
        ['c', 'staff (giới hạn)', c, None, None, c / icc, 'Không: effective < trần 1000'],
        ['d', 'depot (giới hạn)', 6, None, None, 6 / icc, 'Không: effective < trần 300'],
        ['e', 'staff (m=' + str(m6) + ')', c, de6, c * m6, ne6,
         'Có điều kiện: roster, lưu lượng, cụm bằng nhau'],
    ]
    table = pd.DataFrame(rows, columns=['Question', 'Randomization unit', 'Clusters/arm',
                                      'DE', 'Raw N/arm', 'Effective N/arm', 'Feasible?'])
    return dict(d1=table, n_5pp=n5, n_6pp=n6, raw_required_5pp=raw5,
                staff_per_arm_5pp=staff, staff_total_5pp=2 * staff,
                staff_allocated_raw_5pp=staff * m_staff,
                m_6pp=m6, de_6pp=de6, raw_per_arm_6pp=c * m6,
                raw_total_6pp=2 * c * m6, effective_6pp=ne6,
                power_true_5pp=approximate_power(0.70, 0.75, ne6),
                power_true_6pp=approximate_power(0.70, 0.76, ne6),
                safety=safety_baseline(reqs))


def in_ket_qua_cp4(reqs):
    """In bảng D1 và câu trả lời a-e, D3; chỉ thiết kế, không chạy RCT."""
    d = phan_tich_cp4(reqs)
    print('D1: giả định thiết kế; c/d là trần tiệm cận không đạt ở m hữu hạn')
    print(d['d1'].to_string(index=False, na_rep='—', float_format=lambda x: f'{x:,.3f}'))
    print(f"a) {d['n_5pp']} request/arm nếu độc lập; không bảo đảm khi spillover.")
    print(f"b) DE={design_effect(75):.2f}; required raw={d['raw_required_5pp']}/arm; "
          f"{d['staff_per_arm_5pp']} staff/arm => {d['staff_allocated_raw_5pp']} raw/arm; "
          f"tổng {d['staff_total_5pp']} > 40: không khả thi.")
    print('c) effective < 20/0.02 = 1000 < yêu cầu; thêm request không đủ.')
    print('d) effective < 6/0.02 = 300; 6 depot/arm dưới 20 cụm.')
    print(f"e) required effective={d['n_6pp']}; m_min={d['m_6pp']}; DE={d['de_6pp']}; "
          f"raw={d['raw_per_arm_6pp']}/arm, {d['raw_total_6pp']} tổng; "
          f"effective thực theo DE={d['effective_6pp']:.6f}.")
    print(f"Power xấp xỉ: true +5pp={d['power_true_5pp']:.6f}; "
          f"true +6pp={d['power_true_6pp']:.6f}; cần suy luận điều chỉnh theo staff.")
    print('D3: trace lab giả lập, không phải baseline doanh nghiệp được đo thật:', d['safety'])


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    print('A1:', so_lan_chay_ky_vong(0.8, 2), so_lan_chay_ky_vong(0.8),
          he_so_chi_phi_moi_viec_thanh_cong(0.8, 3))
    ket_qua = mo_hinh(runs, reqs)
    print('A2: VND; xem_lai, lam_lai, tong, cps: simulated')
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:16s} {gia_tri:>16,.3f}')
    fallback = (len(reqs) - ket_qua['thanh_cong']) * BASELINE
    print(f'Cả hệ thống (simulated): {ket_qua["tong"] + fallback:,.3f} VND; '
          f'{(ket_qua["tong"] + fallback) / len(reqs):,.3f} VND/yêu cầu')
    print('A3: cps, so_baseline, tong có phần simulated; status ok là từ trace')
    print(phan_tich_theo_loai(runs, reqs).to_string(index=False, float_format=lambda x: f'{x:,.3f}'))
    print('A4: CPS gồm fixed 40 triệu VND/tháng (simulated)')
    print(phan_tich_co_dinh(runs, reqs).to_string(index=False, float_format=lambda x: f'{x:,.3f}'))
    print('B1: tong VND; cps/delta_vnd VND/success; delta_pct % (simulated)')
    print(phan_tich_do_nhay(runs, reqs).to_string(index=False, float_format=lambda x: f'{x:,.6f}'))
    b2 = phan_tich_ket_hop(runs, reqs)
    print('B2: combined và interaction VND/success (simulated)')
    print({k: v for k, v in b2.items() if k != 'ranking'})
    print(b2['ranking'].to_string(index=False, float_format=lambda x: f'{x:,.6f}'))
    print('B3: chi phí VND; system_per_request VND/request; agent_cps VND/success (simulated)')
    print(phan_tich_gioi_han_chay(runs, reqs).to_string(index=False, float_format=lambda x: f'{x:,.6f}'))
    b4 = phan_tich_xem_lai_100(runs, reqs)
    print('B4: chi phí VND; cps VND/success; thời gian phút (simulated)')
    print({k: v for k, v in b4.items() if k != 'bang'})
    print(b4['bang'].to_string(index=False, float_format=lambda x: f'{x:,.6f}'))
    in_ket_qua_cp4(reqs)
