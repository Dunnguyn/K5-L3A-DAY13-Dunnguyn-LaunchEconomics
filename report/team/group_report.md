# Tổng quan bài Individual Lab Day 13

## 1. Thông tin và phạm vi

Nguyễn Thị Thùy Dung · MSSV 2A202603552 · L3A · Individual Lab. Tên `group_report.md` được giữ theo cấu trúc nộp của đề; đây là báo cáo tổng hợp bài cá nhân. Phạm vi đóng góp tại [TEAM.md](../../TEAM.md), công cụ và kiểm chứng tại [báo cáo cá nhân](2A202603552_NguyenThiThuyDung.md).

Tôi dùng hai CSV giả lập của lab để phân tích chi phí và xây dựng kế hoạch pilot có đối chứng. Không có kết quả RCT, quyết định hội đồng hoặc phê duyệt pilot thực tế.

## 2. Tổng kết hiện tại CP1–CP5

| Checkpoint | Trạng thái | Bằng chứng |
| --- | --- | --- |
| CP1 | Content Complete | A1–A4, [bảng chi phí](bang_chi_phi.md), [code](../../src/lab13.py), [tests CP1](../../src/test_cp1.py) |
| CP2 | Content Complete | B1–B4, [bảng chi phí](bang_chi_phi.md), [tests CP2](../../src/test_cp2.py) |
| CP3 | Content Complete về phân tích — Independent Review Pending (PARTIAL về quy trình) | 20 ca, 5 nhóm, Root Cause, 5 remediation, [bảng lỗi](bang_loi.md), [nguồn tổng hợp](cp3_reviewer_summary.md) |
| CP4 | Design & QA Complete | D1/D2, [pilot_plan.yaml](pilot_plan.yaml), [tests CP4](../../src/test_cp4.py) |
| CP5 | Content Complete | [KPI/event/rủi ro](chi_so.md), [Launch Dossier](ho_so_launch_v0.md), [tests CP5](../../src/test_cp5.py) |

**Gate 2a: PENDING EXTERNAL REVIEW. Pilot: Planned / Not Approved.** Hoàn thành nội dung không đồng nghĩa đã được hội đồng duyệt hoặc được phép kích hoạt pilot.

## 3. Kết quả quan trọng

- CP1: 1.200 requests, 1.624 runs, 978 success; tổng 4.373.585,132 VND, CPS 4.471,968 VND/success (**simulated**).
- CP2: rework×2 làm CPS tăng 51,765%; review×2 tăng 40,699%; wage+25% tăng 23,116%. Retry cap2 có system cost 5.751,017 VND/request trên toàn mẫu; B4 review100%/rework15,3 phút có CPS 12.414,793 >12.000 VND/success, break-even review khoảng4,8 phút (**simulated**). Fixed/fallback phải được báo riêng, tránh chồng rework.
- CP3: bảng hai cột trùng 18/20 =90%, lệch ca13 L/C và17 H/S; nhãn đề xuất L/H khớp Final Labels đã xác nhận. [Self-review](cp3_self_review.md) đã có đủ20 nhãn, lý do và confidence, khớp nhãn cuối20/20; người điền và thời điểm đánh giá thực tế chưa được xác minh. Một bộ self-review và bảng xác nhận không chứng minh hai lượt reviewer độc lập.
- CP4: scope noi_dia + hang_nang tại6 depot dự kiến; staff20+20, MDE6pp,859 effective/arm,5980 raw/arm,11960 tổng và299 requests/staff. Power khi true effect chỉ5pp khoảng0,642; không hứa power80% cho5pp.
- Lịch CP4 giữ nguyên: main11/01–07/02/2027; quyết định sớm nhất18/02/2027 sau follow-up/QA. Gia hạn theo enrollment block7 ngày, tối đa42 ngày, quyết định sớm nhất04/03 nếu bắt đầu đúng lịch. 28 ngày coverage/capture80% ước tính13748; chỉ20 ngày9820, thiếu2140. Đây là giả định lưu lượng chia đều, không phải số đo thật.
- CP5: primary994/1200=82,83%; sửa/bỏ48/177=27,12%; reopen51/1200=4,25%, scope39/982=3,9715%. Số mô tả trace lab, không phải causal lift từ baseline thiết kế70%. Có15 event, mapping5 KPI và4 rủi ro; adoption/audit sai hoàn vẫn Proposed — Not Yet Measured.

## 4. Bằng chứng kiểm thử hiện tại

| Suite | Tests | PASS | FAIL |
| --- | --- | --- | --- |
| CP1 | 14 | 14 | 0 |
| CP2 | 16 | 16 | 0 |
| CP4 | 25 | 25 | 0 |
| CP5 | 15 | 15 | 0 |
| Tổng | 70 | 70 | 0 |

**70/70 PASS** là kết quả regression và QA nội dung local. Các lệnh kiểm tra từ `src/`: `python lab13.py`, `python -m unittest discover -s . -p "test_*.py" -v`, `python -m py_compile lab13.py test_cp1.py test_cp2.py test_cp4.py test_cp5.py`; từ root chạy `git diff --check`. Tests không thay thế fault-injection giao dịch thật, instrumentation, diễn tập rollback hoặc đánh giá hội đồng.

## 5. Lịch sử và nguồn

CP1–CP2 được kiểm chứng trước với30 tests; CP4 bổ sung25, CP5 bổ sung15 thành70 tests. Các ghi nhận trước đây không còn là trạng thái tổng kết hiện tại. Phiếu cá nhân/snapshot lịch sử được lưu trong commit `ed89502`, không còn ở HEAD hiện tại sau commit `f33bac6`; xem chỉ dẫn nguồn trong [README hồ sơ](README.md). Mẫu `MSSV_HoTen.md` được khôi phục đúng nội dung từ lịch sử; không dùng làm báo cáo cá nhân.

## 6. Giới hạn và khuyến nghị Gate 2a

**Khuyến nghị: Go có điều kiện**, chỉ xem xét kế hoạch noi_dia + hang_nang. Tất cả gate trong [chi_so.md](chi_so.md) còn Chưa: giao dịch/idempotency/ledger, duyệt thiết kế,40 staff/6 depot và coverage, events đo thật, stop rules/rollback, human review và bằng chứng CP3 độc lập.

Đề gốc yêu cầu nhóm4 người; chấp thuận Individual Lab, cách đáp ứng hai reviewer CP3 và hình thức duyệt Gate 2a đang chờ giảng viên. [Phiếu chấm](phieu_cham.md) giữ nguyên, không tự chấm; không có văn bản miễn/thay thế đã xác minh. Roster40 staff, capture/coverage, mẫu từng staff, kill switch và phút review/rework đo thật chưa xác nhận. Nếu không đáp ứng an toàn/nguồn lực trước hạn thì No-go cho lịch đề xuất, hoãn và trình lại; không tự thay điều kiện thống kê theo outcome.

Commit/push và LMS do người thực hiện quyết định sau review; chưa ghi nhận đã nộp LMS hoặc đúng deadline. Không tự tạo người, kết quả pilot hoặc phê duyệt để hoàn tất hồ sơ.
