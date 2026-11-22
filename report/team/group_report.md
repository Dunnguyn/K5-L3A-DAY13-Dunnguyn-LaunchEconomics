# Tổng quan bài Individual Lab Day 13

## 1. Thông tin

Nguyễn Thị Thùy Dung · MSSV 2A202603552 · L3A · Individual Lab. Tên `group_report.md` được giữ theo cấu trúc nộp bài của đề.

## 2. Mục tiêu và cách tiếp cận

Tôi sử dụng hai CSV giả lập để phân tích chi phí giải quyết thành công, đánh giá độ nhạy và so sánh với phương án nhân viên tự xử lý. Với 20 tình huống lỗi, báo cáo phân tích nguyên nhân gốc và đề xuất kiểm soát phù hợp LogiX-VN.

## 3. Nội dung thực hiện

CP1–CP2 có code, bảng kết quả và 30 tests; chi tiết tại [bảng chi phí](bang_chi_phi.md). CP3 có taxonomy, 20 nhãn, 5 remediation và đánh giá rủi ro tại [bảng lỗi](bang_loi.md). CP4–CP5 và duyệt chéo vẫn chưa thực hiện.

## 4. Kết quả chính

- CPS A2: 4.471,968 VND/success; 978 success trên 1.200 requests (chi phí simulated).
- Chính sách 2 attempts có system cost thấp nhất trên mẫu: 6.901.220,230 VND, tương đương 5.751,017 VND/request (simulated).
- CP3: Người học đã tự rà soát và xác nhận 20/20 Final Labels; giữ nguyên nhãn và Root Cause. Ngày xác nhận: 22/11/2026; tính lại mức khớp reference 20/20 = 100%. Bảng tổng hợp bổ sung đã được tái tính: 18/20 = 90%, bất đồng tại 13 (L/C) và 17 (H/S); nhãn đề xuất L và H khớp Final Labels CONFIRMED. Chưa có bằng chứng phân loại riêng trước khi xem bảng nên tính độc lập PENDING, CP3 PARTIAL. Chưa có quyết định hội đồng hoặc kết luận launch.

## 5. Khó khăn và cách xử lý

Tôi sử dụng môi trường `.venv` hiện có để chạy chương trình. Regression hiện đạt 30/30 PASS; `git diff --check` không báo lỗi. Với CP3, tôi tách kết quả khớp reference khỏi agreement giữa hai reviewer; không dùng phiếu self-review trống làm bộ nhãn reviewer. Các file lịch sử đang bị xóa từ trước lượt cập nhật này không được khôi phục hoặc sửa.

## 6. Phạm vi trách nhiệm

Tôi phụ trách bài cá nhân; chi tiết phạm vi và bằng chứng tại [báo cáo cá nhân](2A202603552_NguyenThiThuyDung.md). Tôi dùng bảng tổng hợp hai cột nhãn được cung cấp, giữ nguyên nguồn và không suy diễn tính độc lập từ việc xác nhận bảng.

## 7. Giới hạn và hướng tiếp tục

Chi phí có sử dụng phút simulated và giả định fallback 12.000 VND/unresolved, có thể chồng với rework. CP3 đã tính lại tỷ lệ trùng nhãn và phân tích hai ca bất đồng; cần hai phiếu nhãn gốc hoặc bằng chứng phân loại riêng để nghiệm thu tính độc lập; năm remediation giữ nguyên, hiệu quả chưa được kiểm chứng trong pilot. Cần hoàn tất phần bằng chứng này và CP4–CP5 trước khi nghiệm thu toàn bộ hồ sơ.

## 8. Tài liệu tham khảo

[Đề DOCX](../../docs/Ngay13_Lab13_De_bai_hoc_vien.docx), [dữ liệu và công thức](../../docs/du_lieu_va_cong_thuc.md), [hướng dẫn chi tiết](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md), [RULES](../../RULES.md), [RUBRIC](../../RUBRIC.md).
