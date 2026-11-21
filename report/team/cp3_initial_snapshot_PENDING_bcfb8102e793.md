# CP3 Phiếu đánh giá cá nhân

Người thực hiện dự kiến: Nguyễn Thị Thùy Dung · 2A202603552 · L3A. Đây là **phiếu chưa được thực hiện**, không phải bằng chứng một lượt đánh giá. AI chỉ trích xuất nguyên văn 20 ca và tạo ô chờ; không điền nhãn, lý do hay confidence thay người học.

Năm nhãn hợp lệ: **Do người dùng; Hệ thống; Ngữ cảnh; Giới hạn hệ thống; Ngầm**. Confidence chỉ nhận High / Medium / Low khi người học thực sự đánh giá. “Chờ người học” và “Not evaluated” là trạng thái thiếu bằng chứng, không phải nhãn lỗi.

## Phase 1 Initial classification chưa khóa

Tự đọc đề và điền 20 dòng dưới đây trước khi đối chiếu đáp án. Bằng chứng cá nhân cần chỉ rõ chi tiết trong ca và lý do chọn root cause, không chỉ lặp nhãn. Người học tự xác nhận đã/chưa xem phần phân tích AI hoặc đáp án; không ghi “blind/độc lập” nếu đã xem. Chưa có xác nhận nào được cung cấp.

Sau khi điền đầy đủ, gửi/lưu nguyên bản thành một snapshot riêng hoặc phiên bản có thể truy xuất trước khi review/reference; ghi người thực hiện và thời điểm thật khi có. Hiện **chưa có snapshot nhãn khóa**, chưa có thời gian đánh giá, không tạo timestamp giả.


| Case ID | Tình huống nguyên văn DOCX | Initial label | Root-cause explanation cá nhân | Evidence cá nhân | Confidence |
| --- | --- | --- | --- | --- | --- |
| 01 | Khách nhập số tài khoản nhận hoàn tiền thiếu hai chữ số. Trợ lý tạo lệnh hoàn, ngân hàng trả về lỗi. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 02 | Kiện nội địa 28 kg. Trợ lý gọi tool tra bảng giá với tham số hàng thường thay vì hàng nặng, hoàn thiếu 45.000 đ. Khách mở lại sau 2 ngày. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 03 | Theo thiết kế, trợ lý hoàn tiền về ví LogiX trong 5 phút. Khách chờ tiền về tài khoản ngân hàng và báo “chưa được hoàn”. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 04 | Khách yêu cầu hoàn phí cho chặng do hãng nước ngoài giao. LogiX không có dữ liệu chặng này. Trợ lý nói không xác định được trạng thái và chuyển cho nhân viên. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 05 | Kiểm tra mẫu cuối tuần thấy 14 đơn có mã giảm giá bị hoàn theo giá trước giảm, thừa trung bình 12.000 đ mỗi đơn. Không khách nào báo, không cảnh báo nào kích. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 06 | Khách chọn mục “Hoàn phí giao trễ” nhưng nội dung mô tả hàng bị vỡ. Trợ lý xử lý theo luồng giao trễ và từ chối vì đơn giao đúng hạn. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 07 | API sổ cái trả lỗi 503 ở bước ghi hoàn tiền. Trợ lý thử lại 3 lần rồi vẫn báo khách “đã hoàn tiền thành công”. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 08 | Trợ lý dẫn “Điều 7.2 chính sách hoàn phí” làm căn cứ. Bản chính sách hiện hành không có điều 7.2. Số tiền hoàn vẫn đúng. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 09 | Khách nhập mã đơn của sàn thương mại điện tử thay vì mã vận đơn. Trợ lý báo “mã không hợp lệ” rồi dừng, không gợi ý gì. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 10 | Đơn giao trễ do bão. Trợ lý từ chối hoàn theo điều khoản bất khả kháng, đúng chính sách. Khách thấy vô lý vì ứng dụng vẫn hiện “cam kết giao 24 giờ”. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 11 | Khách gửi tin nhắn thoại 40 giây. Trợ lý không xử lý được âm thanh, trả lời “vui lòng nhập bằng chữ”. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 12 | Tool tra đơn của depot D05 trả thiếu một trường. Trợ lý vẫn ra kết quả đúng sau nhiều lần gọi, nên tiền token của D05 gấp 3 lần depot khác suốt 3 tuần mà không ai thấy. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 13 | Khách hỏi hoàn phí bảo hiểm hàng hoá, sản phẩm của công ty bảo hiểm đối tác, ngoài phạm vi trợ lý. Trợ lý trả lời chung chung về phí vận chuyển, không nói rõ là mình không xử lý được. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 14 | Khách bấm nhầm “Xác nhận đã nhận tiền” khi chưa nhận. Yêu cầu bị đóng. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 15 | Đơn trễ 26 giờ. Chính sách: trễ 24–48 giờ hoàn 50%. Trợ lý tính hoàn 100%. Nhân viên xem lại bắt được trước khi gửi. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 16 | Theo thiết kế “gửi ngay khi xong”, trợ lý gửi thông báo hoàn tiền qua Zalo lúc 2:14 sáng. Khách phản ánh bị làm phiền. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 17 | Bảng giá đổi từ ngày 01/11 nhưng trợ lý vẫn dùng bản cũ trong bộ nhớ đệm cho đơn dưới 2 kg. Lệch 1.000–2.000 đ mỗi đơn, 212 đơn trong 9 ngày, không ai mở lại. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 18 | Trợ lý tính đúng: phí giao 30.000 đ, hoàn 50%. Tin nhắn chỉ ghi “Đã hoàn 15.000 đ”, không kèm cách tính. Khách cho là hoàn thiếu và mở lại yêu cầu. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 19 | Khách yêu cầu hoàn phí cho đơn từ 14 tháng trước. Trợ lý chỉ truy cập được dữ liệu 12 tháng. Trợ lý nói rõ không tra được và chuyển cho nhân viên kèm tóm tắt. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |
| 20 | Khách gửi lại yêu cầu sau 10 phút vì chưa thấy phản hồi. Trợ lý hoàn hai lần cho cùng một đơn vì lệnh thứ hai không có khoá chống trùng. | Chờ người học | Chờ người học | Chờ người học | Chờ người học |


## Phase 2 Self-review chưa thực hiện

Chỉ điền sau khi Phase 1 đã lưu/khóa; ghi một lượt rà soát thực sự của chính người học. Giữ nguyên initial label, không chép đáp án rồi gọi là tự rà soát; nếu đã xem đáp án phải khai báo mức tiếp xúc. Đây là intra-rater consistency, không phải inter-rater agreement.


| Case ID | Initial label (từ snapshot) | Review label | Match? | Reason for change | Review evidence |
| --- | --- | --- | --- | --- | --- |
| 01 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 02 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 03 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 04 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 05 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 06 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 07 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 08 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 09 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 10 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 11 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 12 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 13 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 14 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 15 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 16 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 17 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 18 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 19 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |
| 20 | Chờ snapshot | Chờ người học | Not evaluated | Chờ lượt review thực tế | Chờ người học |


## Phase 3 đến Phase 5 Chờ dữ liệu

Agreement = số nhãn initial/review trùng / 20 × 100, chỉ tính khi đủ 20 cặp hợp lệ; không dùng số dòng đã điền làm mẫu số thay thế. Số trùng, số không trùng, danh sách bất đồng và tỷ lệ hiện **Not evaluated**. Ngưỡng tham khảo 16/20 = 80% chưa được đánh giá.

Khi có bất đồng: lưu case, hai nhãn gốc, chi tiết quyết định, quy tắc ranh giới và final label; không chỉnh snapshot để tăng agreement. Chỉ sau khi initial đã khóa mới mở bảng nhãn tham khảo và tính reference accuracy = số khớp / 20 × 100, ghi rõ so initial hay final. Hiện chưa đối chiếu cả hai; không lấy đáp án làm initial.

Reviewer thứ hai: chưa có; inter-rater agreement **Not evaluated**, tiêu chí **NOT MET — Individual Lab**; chưa có văn bản miễn trừ. Không dùng hai lượt của một người hay AI làm hai reviewer.
