# Báo cáo cá nhân Day 13

## 1. Thông tin sinh viên

- Họ tên: Nguyễn Thị Thùy Dung.
- MSSV: 2A202603552.
- Lớp: L3A.
- Hình thức: Individual Lab.
- Email: chưa cung cấp.

## 2. Phần việc phụ trách

Tôi phụ trách bài cá nhân từ A–E. Phạm vi đã có kết quả là CP1–CP2 và nội dung phân tích CP3; CP4–CP5 hiện còn ở dạng biểu mẫu. CP3 chưa đủ điều kiện nghiệm thu quy trình đánh giá.

## 3. Kết quả thực hiện

| Phần | Kết quả | Bằng chứng |
| --- | --- | --- |
| CP1 | 978 success; CPS 4.471,968 VND/success (simulated); đủ A1–A4 | `bang_chi_phi.md`, `../../src/lab13.py`, `../../src/test_cp1.py` |
| CP2 | Đủ B1–B4; 2 attempts có system cost thấp nhất 6.901.220,230 VND trên mẫu (simulated) | `bang_chi_phi.md`, `../../src/test_cp2.py` |
| CP3 | 20 nhãn, 5 nhóm, 5 remediation; khớp reference 20/20 = 100% | `bang_loi.md`, phiếu cá nhân và snapshot |

Từ kết quả chi phí, tôi đề xuất xem xét pilot trong phạm vi noi_dia + hang_nang và theo dõi công sức xem lại/làm lại. Các đề xuất ở CP3 cần kiểm chứng bằng event thực tế; chưa được coi là cơ chế đã triển khai.

## 4. Bằng chứng và cách kiểm chứng

Các phép tính được đối chiếu bằng `lab13.py`, kiểm thử độc lập `csv`/`Decimal` và invariant tests. Lệnh `python -m unittest -v test_cp1 test_cp2` chạy 30 tests, 30 PASS, 0 FAIL; `python lab13.py` và `py_compile` chạy thành công.

Bộ initial CP3 được lưu trước lượt đối chiếu của trợ lý, không chỉnh theo reference. Snapshot nhãn có SHA-256 `3d0822a1e19bded7f806b058c1db838a7f9cc849564426858ba9c358bab0e417`; snapshot PENDING lịch sử có SHA-256 `bcfb8102e7931e7b0479e64ff1708ece9ea16a14617c3cbb188ece3241f34758`. Bảng QA-C01–C12 ghi trong báo cáo lỗi; phiếu self-review vẫn trống.

Không có commit/push mới được tạo trong quá trình chuẩn hóa; kết quả kiểm thử không phải chứng cứ remediation đã hiệu quả hoặc có reviewer thứ hai.

## 5. Công cụ hỗ trợ và kiểm chứng

Tôi sử dụng ChatGPT và Codex để hỗ trợ phân tích yêu cầu, phát triển mã nguồn, rà soát tài liệu và phân loại lỗi. Các phép tính được kiểm tra bằng chương trình và kiểm thử tự động. Bộ nhãn lỗi CP3 có sử dụng hỗ trợ AI và đã được đối chiếu với tài liệu tham khảo; chưa có bằng chứng đánh giá độc lập của hai người.

Các giá trị AI Confidence trong snapshot là dữ liệu nguồn, không phải confidence tự đánh giá của tôi hay xác suất đã hiệu chuẩn. Kết quả khớp reference 100% không thay thế self-review consistency hoặc inter-rater agreement. Không gọi model thật/API trong chương trình lab.

## 6. Tự đánh giá và phần còn thiếu

CP1–CP2 đã có kết quả thực thi và kiểm thử. CP3: **Self-review PENDING; inter-rater agreement NOT MET — Individual Lab**; nhãn kết luận đề xuất chờ xác nhận. Nếu tiếp tục tự review sau khi đã xem reference, cần ghi rõ mức tiếp xúc; không mô tả là gắn nhãn mù hay hai người độc lập.

CP4–CP5 và duyệt chéo chưa thực hiện. Cần xác nhận với giảng viên cách nghiệm thu Individual Lab khi không có reviewer thứ hai, thay phút simulated bằng đo thật và kiểm chứng các remediation trong pilot trước khi kết luận hiệu quả.
