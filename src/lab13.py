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
    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    #   from statsmodels.stats.proportion import proportion_effectsize
    #   from statsmodels.stats.power import NormalIndPower
