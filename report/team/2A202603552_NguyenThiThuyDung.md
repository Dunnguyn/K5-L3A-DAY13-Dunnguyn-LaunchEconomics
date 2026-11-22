# Báo cáo cá nhân Day 13

## 1. Thông tin sinh viên

- Họ tên: Nguyễn Thị Thùy Dung.
- MSSV: 2A202603552.
- Lớp: L3A.
- Hình thức: Individual Lab.
- Email: chưa cung cấp.

## 2. Phần việc phụ trách

Tôi phụ trách bài cá nhân từ A–E. CP1–CP2 đã có kết quả thực thi; CP3 có taxonomy, 20 Final Labels và năm remediation. CP4–CP5 còn ở dạng biểu mẫu. Lượt này tôi rà soát nghiệm thu CP3 theo bằng chứng trong repository, không thay đổi code CP1–CP2 hoặc CSV.

## 3. Kết quả thực hiện

| Phần | Kết quả | Bằng chứng |
| --- | --- | --- |
| CP1 | 978 success; CPS 4.471,968 VND/success (simulated); đủ A1–A4 | `bang_chi_phi.md`, `../../src/lab13.py`, `../../src/test_cp1.py` |
| CP2 | Đủ B1–B4; 2 attempts có system cost thấp nhất 6.901.220,230 VND trên mẫu (simulated) | `bang_chi_phi.md`, `../../src/test_cp2.py` |
| CP3 | 20 Final Labels đã xác nhận; khớp reference 20/20 = 100%; đủ 5 remediation; trùng nhãn 18/20 = 90%, phân tích Case 13 và 17; tính độc lập PENDING | [Báo cáo lỗi](bang_loi.md) |

Tôi giữ nguyên toàn bộ Final Labels và Root Cause. Năm remediation vẫn phù hợp với năm nhóm lỗi: 01/U, 07/S, 18/C, 19/L và 05/H; mỗi dòng có cách phát hiện đo được và một vai trò chịu trách nhiệm. Các biện pháp vẫn Proposed/Planned, chưa được kiểm chứng hiệu quả trong pilot.

## 4. Bằng chứng và cách kiểm chứng

Tôi cung cấp bảng tổng hợp hai cột nhãn Reviewer 01 và Reviewer 02 trong cuộc trao đổi ngày 22/11/2026. Bảng nguồn được lưu tại [cp3_reviewer_summary.md](cp3_reviewer_summary.md), giữ nguyên 20 cặp nhãn, cột trùng nhãn, nhãn đề xuất và ghi chú phương pháp.

Tôi kiểm tra đủ Case ID 01–20, mỗi ca xuất hiện đúng một lần và cả hai cột chỉ có nhãn U/S/C/L/H. So từng cặp cho kết quả **18 trùng, 2 lệch; 18/20 × 100 = 90%**, cao hơn ngưỡng 80% là 10 điểm phần trăm. Hai ca lệch chính xác là **13 (L/C)** và **17 (H/S)**.

Theo ghi chú nguồn, hai reviewer đã xác nhận bảng nhưng bảng được chuẩn bị trước khi xác nhận. Tôi chưa có bằng chứng hai người tự phân loại riêng trước khi xem bảng tổng hợp. Vì vậy, kết quả 90% đã được tính lại từ bảng, còn điều kiện đánh giá độc lập vẫn **PENDING**; tôi không gọi đây là inter-rater agreement độc lập đã nghiệm thu.

Phiếu `cp3_self_review.md` vẫn trống ở cả 20 dòng. Tôi không dùng phiếu do trợ lý soạn làm bằng chứng tự đánh giá độc lập hoặc thay cho phiếu reviewer gốc. Các file lịch sử đang bị xóa từ trước lượt nghiệm thu được giữ nguyên trạng thái.

## 5. Xác nhận nhãn cuối và phân xử

Người học đã tự rà soát và xác nhận 20/20 Final Labels; giữ nguyên nhãn và Root Cause. Ngày xác nhận: 22/11/2026. Trạng thái bộ nhãn hiện tại: **CONFIRMED — 20/20**.

Tôi đối chiếu đủ 20 nhãn đề xuất trong bảng nguồn với bộ Final Labels hiện tại: **20/20 trùng**, không cần đổi nhãn. Đối chiếu với hướng dẫn Nhiệm vụ C tiếp tục cho kết quả **20/20 = 100%**.

| Case ID | Hai nhãn reviewer | Phân tích và nhãn phân xử đề xuất | Đối chiếu nhãn cuối |
| --- | --- | --- | --- |
| 13 | L / C | Yêu cầu bảo hiểm đối tác nằm ngoài phạm vi chức năng; phản hồi chung chung là yếu tố giao tiếp phụ. Chọn L — System Limitation. | Trùng L đã CONFIRMED |
| 17 | H / S | Cache dùng bảng giá cũ gây sai lệch ở 212 đơn trong 9 ngày mà không ai mở lại; taxonomy bài lab ưu tiên tính âm thầm kéo dài. Chọn H — Hidden Error; không bổ sung cơ chế phát hiện mà đề chưa nêu. | Trùng H đã CONFIRMED |

Phân tích chi tiết và quy tắc ranh giới nằm tại mục 5 của [báo cáo lỗi](bang_loi.md). Nhãn cuối đã được tôi xác nhận từ trước và không thay đổi. Tôi không suy diễn xác nhận nhãn cuối thành việc hai reviewer đã cùng chấp thuận phân xử hoặc đã phân loại độc lập.

## 6. Regression và bảo toàn dữ liệu

Ngày 22/11/2026, tôi chạy `src/.venv/Scripts/python.exe -m unittest -v test_cp1 test_cp2` từ thư mục `src`. Lượt đầu có 29/30 PASS do câu mở đầu báo cáo CP1 đã bị sửa ở lượt trước. Tôi khôi phục đúng câu gốc trong `bang_chi_phi.md` theo `HEAD` để đáp ứng kiểm tra bảo toàn; lượt chạy lại đạt **30 tests, 30 PASS, 0 FAIL**. Tôi không sửa code, tests hoặc CSV. `git diff --check` không báo lỗi.

Tôi giữ nguyên năm remediation, phiếu self-review và trạng thái các file lịch sử đang bị xóa. Không tự commit/push. Regression CP1–CP2 không phải chứng cứ agreement hoặc hiệu quả remediation.

## 7. Checklist nghiệm thu CP3

| Điều kiện | Trạng thái và bằng chứng |
| --- | --- |
| Taxonomy và 20 ca có Root Cause/evidence | DONE; giữ nguyên |
| Bằng chứng hai reviewer phân loại độc lập | PENDING — có bảng tổng hợp, chưa có bằng chứng phân loại riêng trước khi xem bảng |
| Tỷ lệ trùng nhãn trong bảng ≥80% | DONE — tái tính đủ 20 cặp: 18 trùng, 2 lệch, 90%; tính độc lập xét riêng |
| Xác định và phân tích hai ca bất đồng | DONE — Case 13 L/C → L; Case 17 H/S → H, trùng Final Labels đã xác nhận |
| Người học xác nhận Final Labels | CONFIRMED — 20/20, ngày 22/11/2026 |
| Final Labels khớp reference ≥16/20 | DONE — tính lại 20/20 = 100% |
| 5 remediation đủ loại, ngưỡng, chu kỳ, owner | DONE — giữ nguyên; Proposed/Planned |
| Regression CP1–CP2 và diff check | DONE — 30/30 PASS; không có lỗi diff |

**CP3: PARTIAL.** Tôi đã tính lại 90% từ bảng tổng hợp, phân tích hai ca bất đồng và đối chiếu khớp bộ nhãn cuối CONFIRMED. Điều kiện còn thiếu là hai phiếu nhãn gốc hoặc bằng chứng hai reviewer tự phân loại riêng trước khi xem bảng. CP4–CP5 và nghiệm thu toàn bộ hồ sơ vẫn chưa hoàn thành.

## 8. Cập nhật CP4 và công cụ hỗ trợ

Ngày 22/11/2026, tôi hoàn thiện thiết kế CP4 trong `src/lab13.py`, `src/test_cp4.py` và `pilot_plan.yaml`. Đây là kế hoạch Planned để trình Gate 2a; chưa thực hiện phân nhóm hoặc pilot. Ghi nhận CP4 chưa hoàn thành ở mục trước là trạng thái trước lượt cập nhật này; CP3 và CP5 giữ nguyên trạng thái.

Tôi sử dụng ChatGPT/Codex để hỗ trợ lập trình, rà soát phép tính và soạn kế hoạch CP4 theo `RULES.md`. Cách kiểm chứng: đối chiếu công thức bằng SciPy, kiểm tra bất biến và tính tối thiểu của cỡ mẫu, đếm lại CSV bằng `csv.DictReader`, parse và duyệt cây YAML, chạy 25 tests CP4 cùng 30 regression tests CP1–CP2 sau rà soát tính khả thi, kiểm tra cú pháp và `git diff --check`. Không gọi model/API trong chương trình, không dùng kết quả thiết kế làm bằng chứng hiệu quả thực nghiệm.

### Rà soát tính khả thi trước CP5

Tôi giữ nguyên toàn bộ D1: MDE 6pp cần 859 effective/arm, 20 staff/arm, tối thiểu 299 requests/người, DE 6,96 và tổng 11.960 raw requests. Power khi tác động thật chỉ +5pp vẫn khoảng 0,642; gia hạn để đạt mẫu không thay đổi giới hạn này.

Lịch cũ 28/12/2026–10/01/2027 có 14 ngày. Với giả định chia đều 1.500 requests/ngày trên 12 depot, 6 depot có 750 requests/ngày; áp tỷ trọng eligible 982/1.200 cho khoảng 613,75 eligible/ngày. Trong 14 ngày chỉ có 8.592,5 requests kỳ vọng, thiếu 3.367,5; chia đều 40 staff là 214,8125/người, chưa đạt 299. Đây là phép ước tính từ bối cảnh và trace lab giả lập, không phải số đo thực tế. Con số 1.227,5 eligible/ngày trong kế hoạch trước thuộc toàn bộ 12 depot, không được dùng thay lưu lượng 6 depot.

Nếu staff cũng chia đều 40 người trên 12 depot, 6 depot chỉ khoảng 20 người. Tôi chưa có bằng chứng bố trí đủ 40 staff tại 6 depot; cần xác minh roster/năng lực hoặc điều chuyển thêm khoảng 20 người trước phân nhóm. Vì 40 là toàn bộ nguồn lực giả định của mạng, phương án điều chuyển phải bảo đảm coverage của 6 depot ngoài pilot; tôi không mặc định có thêm người hoặc đã được doanh nghiệp chấp thuận. Chỉ có 20 staff tổng thì 10/arm có trần effective 500 <859, không thể khắc phục bằng kéo dài thời gian. Mở phạm vi sang 12 depot chỉ là phương án khác cần xét và duyệt trước preregistration, không tự thay phạm vi khi đang chạy.

Tôi đổi kỳ chính dự kiến sang 11/01–07/02/2027 (28 ngày), có điều kiện: 40 staff tại 6 depot và đủ coverage. Theo phép chia đều, 28 ngày có 17.185 eligible kỳ vọng; kịch bản capture 80% còn 13.748, bình quân 343,7/người. Capture 80% là giả định hao hụt do exclusion bổ sung, routing và coverage, chưa được đo. Tối thiểu cần 20 ngày có lưu lượng ở capture 100%, hoặc 25 ngày ở capture 80%; nếu 28 ngày lịch chỉ có 20 ngày coverage thì kịch bản 80% chỉ thu 9.820, vẫn thiếu. Tổng đủ cũng không bảo đảm từng staff hoặc từng arm đủ, nhất là khi workload không đều.

Hai bước ramp dự kiến thu một tuần mỗi bước, sau đó chờ tối đa 1 ngày đóng và đủ 7 ngày follow-up, rồi qua gate: ramp 10% từ 30/11–06/12, gate không trước 15/12; ramp 25% từ 21–27/12, gate không trước 05/01. Main bắt đầu 11/01 nếu gate đạt; không gộp dữ liệu ramp vào mẫu efficacy chính. Economic rule dùng hai cohort tuần lịch liên tiếp, không chồng lấn, cùng phiên bản/scope và mỗi tuần đủ 100 success trưởng thành. Hai tuần cuối main có thể đánh giá đầy đủ ngày 16/02; sự cố giao dịch nghiêm trọng vẫn dừng ngay.

Nếu kết thúc thu mẫu ngày 07/02, request cuối có thể đóng ngày 08/02 và cần theo dõi đến hết 15/02; QA 16–17/02, quyết định sớm nhất 18/02/2027. Toàn bộ lịch là đề xuất chưa được LogiX chấp thuận. Khi chưa đủ mẫu, gia hạn đồng thời hai arm theo block 7 ngày, tối đa 42 ngày main; chỉ dùng số enrollment/coverage đã làm mù efficacy để quyết định gia hạn, không dùng p-value hoặc effect. Giữ nguyên arm, roster và eligibility; thu mọi eligible tới hết block, không bỏ request từ staff thu nhanh.

Nếu main bắt đầu đúng 11/01 và gia hạn hết 42 ngày thì kết thúc 21/02, follow-up đến 01/03, QA 02–03/03 và quyết định sớm nhất 04/03. Thiếu mẫu sau giới hạn, thiếu cụm, thiếu hai tuần kinh tế đủ mẫu hoặc dữ liệu chưa đạt QA thì Inconclusive/không mở rộng. Ramp/main bị lùi phải dịch toàn bộ lịch theo ngày thực và lưu audit. Các giới hạn khác còn lại gồm staff chưa xác minh, tải không đều, ICC/CV kích thước cụm, contamination, ngày nghỉ và ngưỡng adoption có thể làm rollout kéo dài.
