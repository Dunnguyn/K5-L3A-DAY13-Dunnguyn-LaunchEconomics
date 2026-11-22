# Báo cáo cá nhân Day 13

## 1. Thông tin sinh viên

- Họ tên: Nguyễn Thị Thùy Dung.
- MSSV: 2A202603552.
- Lớp: L3A.
- Hình thức: Individual Lab.
- Email: chưa cung cấp.

## 2. Phần việc phụ trách

Tôi phụ trách bài cá nhân từ A–E: phân tích, tính toán, tài liệu, kiểm thử và tổng hợp hồ sơ. CP1–CP2 Content Complete; CP3 Content Complete về phân tích, Independent Review Pending; CP4 Design & QA Complete; CP5 Content Complete. Gate 2a: PENDING EXTERNAL REVIEW; Pilot: Planned / Not Approved. Quy trình Individual Lab còn chờ giảng viên xác nhận.

## 3. Kết quả thực hiện

| Phần | Kết quả | Bằng chứng |
| --- | --- | --- |
| CP1 | 978 success; CPS 4.471,968 VND/success (simulated); đủ A1–A4 | `bang_chi_phi.md`, `../../src/lab13.py`, `../../src/test_cp1.py` |
| CP2 | Đủ B1–B4; 2 attempts có system cost thấp nhất 6.901.220,230 VND trên mẫu (simulated) | `bang_chi_phi.md`, `../../src/test_cp2.py` |
| CP3 | 20 Final Labels đã xác nhận; khớp reference 20/20 = 100%; đủ 5 remediation; trùng nhãn 18/20 = 90%, phân tích Case 13 và 17; tính độc lập PENDING | [Báo cáo lỗi](bang_loi.md) |
| CP4 | Design & QA Complete; 20+20 staff, MDE6pp, tổng11960 raw requests, power true5pp≈0,642; lịch có điều kiện | [Pilot plan](pilot_plan.yaml), `../../src/test_cp4.py` |
| CP5 | Content Complete; ba KPI mô tả, hai KPI đề xuất,15 event,4 rủi ro và dossier7 mục; chưa có phê duyệt | [Chỉ số](chi_so.md), [dossier](ho_so_launch_v0.md), `../../src/test_cp5.py` |

Tôi giữ nguyên toàn bộ Final Labels và Root Cause. Năm remediation vẫn phù hợp với năm nhóm lỗi: 01/U, 07/S, 18/C, 19/L và 05/H; mỗi dòng có cách phát hiện đo được và một vai trò chịu trách nhiệm. Các biện pháp vẫn Proposed/Planned, chưa được kiểm chứng hiệu quả trong pilot.

## 4. Bằng chứng và cách kiểm chứng

Tôi cung cấp bảng tổng hợp hai cột nhãn Reviewer 01 và Reviewer 02 trong cuộc trao đổi ngày 22/11/2026. Bảng nguồn được lưu tại [cp3_reviewer_summary.md](cp3_reviewer_summary.md), giữ nguyên 20 cặp nhãn, cột trùng nhãn, nhãn đề xuất và ghi chú phương pháp.

Tôi kiểm tra đủ Case ID 01–20, mỗi ca xuất hiện đúng một lần và cả hai cột chỉ có nhãn U/S/C/L/H. So từng cặp cho kết quả **18 trùng, 2 lệch; 18/20 × 100 = 90%**, cao hơn ngưỡng 80% là 10 điểm phần trăm. Hai ca lệch chính xác là **13 (L/C)** và **17 (H/S)**.

Theo ghi chú nguồn, hai reviewer đã xác nhận bảng nhưng bảng được chuẩn bị trước khi xác nhận. Tôi chưa có bằng chứng hai người tự phân loại riêng trước khi xem bảng tổng hợp. Vì vậy, kết quả 90% đã được tính lại từ bảng, còn điều kiện đánh giá độc lập vẫn **PENDING**; tôi không gọi đây là inter-rater agreement độc lập đã nghiệm thu.

Phiếu `cp3_self_review.md` hiện có đủ20/20 nhãn, giải thích và confidence; đối chiếu khớp Final Labels20/20. Chưa xác minh người điền, thời điểm làm review thực tế và mức tiếp xúc với reference. Đây là một bộ self-review, không phải bằng chứng hai reviewer độc lập; tôi không tự gán nguồn tác giả hoặc thời gian cho phiếu. Các phiếu nhãn lịch sử ở commit `ed89502` không còn trong HEAD hiện tại sau commit `f33bac6`.


## 5. Công cụ AI đã dùng

Sử dụng ChatGPT/Codex để hỗ trợ lập trình, rà soát phép tính và soạn kế hoạch CP4 theo `RULES.md`. 

## Tự đánh giá

Hoàn thành bài LAB 
