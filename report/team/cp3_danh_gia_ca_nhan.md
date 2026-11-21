# CP3 Phiếu đánh giá cá nhân

**Nguyễn Thị Thùy Dung · 2A202603552 · L3A · Individual Lab.** Phương pháp và nguồn bộ nhãn được trình bày tại [báo cáo lỗi, mục 1](bang_loi.md#1-thông-tin-và-phương-pháp); không xem bộ nhãn này là đánh giá độc lập.

## Phase 1 Initial classification

Nhãn và giải thích dưới đây giữ nguyên từ [snapshot nguồn](cp3_initial_snapshot_AI_assisted.md), SHA-256 `3d0822a1e19bded7f806b058c1db838a7f9cc849564426858ba9c358bab0e417`. Các giá trị confidence gốc được bảo toàn trong snapshot, không đưa vào bảng chính vì không phải tự đánh giá của người học. Evidence là trích đoạn đối chiếu đề DOCX khi rà soát tài liệu.

| Case ID | Tình huống nguyên văn DOCX | Initial label | Root Cause Explanation gốc | Evidence |
| --- | --- | --- | --- | --- |
| 01 | Khách nhập số tài khoản nhận hoàn tiền thiếu hai chữ số. Trợ lý tạo lệnh hoàn, ngân hàng trả về lỗi. | U — User Error | Khách hàng nhập số tài khoản ngân hàng thiếu hai chữ số, khiến dữ liệu đầu vào không hợp lệ. Nguyên nhân trực tiếp xuất phát từ thao tác nhập liệu của người dùng. | DOCX bảng 9, ca 01: “thiếu hai chữ số” |
| 02 | Kiện nội địa 28 kg. Trợ lý gọi tool tra bảng giá với tham số hàng thường thay vì hàng nặng, hoàn thiếu 45.000 đ. Khách mở lại sau 2 ngày. | S — System Error | Kiện hàng nặng 28 kg nhưng agent gọi công cụ xử lý hàng thường. Agent chọn sai công cụ so với quy tắc phân loại trọng lượng. | DOCX bảng 9, ca 02: “hàng thường thay vì hàng nặng” |
| 03 | Theo thiết kế, trợ lý hoàn tiền về ví LogiX trong 5 phút. Khách chờ tiền về tài khoản ngân hàng và báo “chưa được hoàn”. | C — Context Error | Agent hoàn tiền về ví điện tử đúng thiết kế, nhưng khách hàng kỳ vọng nhận tiền vào tài khoản ngân hàng. Kết quả đúng về kỹ thuật nhưng không phù hợp với kỳ vọng của khách. | DOCX bảng 9, ca 03: “Khách chờ tiền về tài khoản ngân hàng” |
| 04 | Khách yêu cầu hoàn phí cho chặng do hãng nước ngoài giao. LogiX không có dữ liệu chặng này. Trợ lý nói không xác định được trạng thái và chuyển cho nhân viên. | L — System Limitation | Agent không có dữ liệu về chặng vận chuyển quốc tế cần thiết để xử lý yêu cầu. Nguyên nhân là thiếu dữ liệu trong phạm vi hệ thống hỗ trợ. | DOCX bảng 9, ca 04: “LogiX không có dữ liệu chặng này” |
| 05 | Kiểm tra mẫu cuối tuần thấy 14 đơn có mã giảm giá bị hoàn theo giá trước giảm, thừa trung bình 12.000 đ mỗi đơn. Không khách nào báo, không cảnh báo nào kích. | H — Hidden Error | Hệ thống tính tiền hoàn theo giá trước giảm thay vì giá thực trả. Sai lệch không được nhận ra trong quy trình thông thường mà chỉ được phát hiện khi kiểm toán. | DOCX bảng 9, ca 05: “Không khách nào báo, không cảnh báo nào kích” |
| 06 | Khách chọn mục “Hoàn phí giao trễ” nhưng nội dung mô tả hàng bị vỡ. Trợ lý xử lý theo luồng giao trễ và từ chối vì đơn giao đúng hạn. | U — User Error | Khách hàng chọn lý do giao hàng trễ trong khi nội dung phản ánh hàng bị vỡ. Nguyên nhân gốc là chọn sai loại yêu cầu, không phải lỗi xử lý của agent. | DOCX bảng 9, ca 06: “Khách chọn mục “Hoàn phí giao trễ”” |
| 07 | API sổ cái trả lỗi 503 ở bước ghi hoàn tiền. Trợ lý thử lại 3 lần rồi vẫn báo khách “đã hoàn tiền thành công”. | S — System Error | Công cụ ghi sổ giao dịch trả lỗi HTTP 503 nhưng agent vẫn thông báo hoàn tiền thành công. Agent không kiểm tra xác nhận giao dịch trước khi gửi thông báo. | DOCX bảng 9, ca 07: “vẫn báo khách “đã hoàn tiền thành công”” |
| 08 | Trợ lý dẫn “Điều 7.2 chính sách hoàn phí” làm căn cứ. Bản chính sách hiện hành không có điều 7.2. Số tiền hoàn vẫn đúng. | S — System Error | Agent viện dẫn một điều khoản chính sách không tồn tại, dù số tiền hoàn đúng. Đây là hành vi tạo thông tin sai có thể nhận diện được từ nội dung phản hồi. | DOCX bảng 9, ca 08: “Bản chính sách hiện hành không có điều 7.2” |
| 09 | Khách nhập mã đơn của sàn thương mại điện tử thay vì mã vận đơn. Trợ lý báo “mã không hợp lệ” rồi dừng, không gợi ý gì. | U — User Error | Khách hàng nhập mã đơn hàng trên sàn thương mại điện tử thay vì mã vận đơn. Dữ liệu đầu vào không đúng định dạng định danh mà hệ thống yêu cầu. | DOCX bảng 9, ca 09: “thay vì mã vận đơn” |
| 10 | Đơn giao trễ do bão. Trợ lý từ chối hoàn theo điều khoản bất khả kháng, đúng chính sách. Khách thấy vô lý vì ứng dụng vẫn hiện “cam kết giao 24 giờ”. | C — Context Error | Agent từ chối hoàn phí đúng chính sách liên quan đến bão, nhưng khách kỳ vọng được giải quyết theo cam kết dịch vụ. Vấn đề nằm ở sự khác biệt giữa quy tắc áp dụng và kỳ vọng thực tế. | DOCX bảng 9, ca 10: “đúng chính sách” |
| 11 | Khách gửi tin nhắn thoại 40 giây. Trợ lý không xử lý được âm thanh, trả lời “vui lòng nhập bằng chữ”. | L — System Limitation | Agent không thể xử lý thông tin khách cung cấp bằng tin nhắn thoại. Khả năng tiếp nhận và phân tích định dạng âm thanh chưa được hỗ trợ. | DOCX bảng 9, ca 11: “không xử lý được âm thanh” |
| 12 | Tool tra đơn của depot D05 trả thiếu một trường. Trợ lý vẫn ra kết quả đúng sau nhiều lần gọi, nên tiền token của D05 gấp 3 lần depot khác suốt 3 tuần mà không ai thấy. | H — Hidden Error | Một trường dữ liệu bị thiếu khiến số token tăng bất thường trong thời gian dài mà không được phát hiện. Đây là lỗi ngầm về hiệu quả chi phí, dù kết quả phản hồi vẫn có thể đúng. | DOCX bảng 9, ca 12: “suốt 3 tuần mà không ai thấy” |
| 13 | Khách hỏi hoàn phí bảo hiểm hàng hoá, sản phẩm của công ty bảo hiểm đối tác, ngoài phạm vi trợ lý. Trợ lý trả lời chung chung về phí vận chuyển, không nói rõ là mình không xử lý được. | L — System Limitation | Yêu cầu bảo hiểm của đối tác nằm ngoài phạm vi hỗ trợ của agent. Việc giải thích giới hạn chưa tốt là điểm cần cải thiện nhưng không thay đổi nguyên nhân gốc. | DOCX bảng 9, ca 13: “ngoài phạm vi trợ lý” |
| 14 | Khách bấm nhầm “Xác nhận đã nhận tiền” khi chưa nhận. Yêu cầu bị đóng. | U — User Error | Người dùng vô tình chọn trạng thái đã nhận tiền, khiến yêu cầu bị đóng. Nguyên nhân trực tiếp là thao tác xác nhận nhầm của người dùng. | DOCX bảng 9, ca 14: “Khách bấm nhầm” |
| 15 | Đơn trễ 26 giờ. Chính sách: trễ 24–48 giờ hoàn 50%. Trợ lý tính hoàn 100%. Nhân viên xem lại bắt được trước khi gửi. | S — System Error | Agent tính mức hoàn 100% thay vì 50% theo chính sách. Sai sót được nhân viên phát hiện trước khi gửi kết quả nên thuộc lỗi hệ thống đã lộ ra. | DOCX bảng 9, ca 15: “Nhân viên xem lại bắt được trước khi gửi” |
| 16 | Theo thiết kế “gửi ngay khi xong”, trợ lý gửi thông báo hoàn tiền qua Zalo lúc 2:14 sáng. Khách phản ánh bị làm phiền. | C — Context Error | Agent gửi thông báo đúng quy trình nhưng vào lúc 02:14 sáng. Hành vi hợp lệ về kỹ thuật nhưng không phù hợp với thời điểm và trải nghiệm của khách hàng. | DOCX bảng 9, ca 16: “Theo thiết kế “gửi ngay khi xong”” |
| 17 | Bảng giá đổi từ ngày 01/11 nhưng trợ lý vẫn dùng bản cũ trong bộ nhớ đệm cho đơn dưới 2 kg. Lệch 1.000–2.000 đ mỗi đơn, 212 đơn trong 9 ngày, không ai mở lại. | H — Hidden Error | Bộ nhớ đệm sử dụng bảng giá cũ khiến 212 đơn bị tính sai. Sai lệch tồn tại trên nhiều giao dịch trước khi được phát hiện qua kiểm tra. | DOCX bảng 9, ca 17: “212 đơn trong 9 ngày, không ai mở lại” |
| 18 | Trợ lý tính đúng: phí giao 30.000 đ, hoàn 50%. Tin nhắn chỉ ghi “Đã hoàn 15.000 đ”, không kèm cách tính. Khách cho là hoàn thiếu và mở lại yêu cầu. | C — Context Error | Số tiền hoàn được tính đúng chính sách nhưng agent không giải thích cách tính, khiến khách khó hiểu kết quả. Hệ thống đã giả định khách có đủ thông tin để tự diễn giải. | DOCX bảng 9, ca 18: “không kèm cách tính” |
| 19 | Khách yêu cầu hoàn phí cho đơn từ 14 tháng trước. Trợ lý chỉ truy cập được dữ liệu 12 tháng. Trợ lý nói rõ không tra được và chuyển cho nhân viên kèm tóm tắt. | L — System Limitation | Đơn hàng đã 14 tháng tuổi, vượt giới hạn truy xuất dữ liệu 12 tháng của hệ thống. Agent không thể xử lý đầy đủ vì giới hạn thời gian lưu trữ/truy cập. | DOCX bảng 9, ca 19: “chỉ truy cập được dữ liệu 12 tháng” |
| 20 | Khách gửi lại yêu cầu sau 10 phút vì chưa thấy phản hồi. Trợ lý hoàn hai lần cho cùng một đơn vì lệnh thứ hai không có khoá chống trùng. | S — System Error | Hệ thống thực hiện hoàn tiền hai lần vì thiếu cơ chế chống xử lý trùng giao dịch. Đây là lỗi kiểm soát nghiệp vụ và tính toàn vẹn giao dịch của hệ thống. | DOCX bảng 9, ca 20: “lệnh thứ hai không có khoá chống trùng” |

## Phase 2 Self-review: PENDING

Chưa có lượt self-review thực tế. Dùng [phiếu self-review riêng](cp3_self_review.md) để tự điền; nếu đã xem reference trước review, cần ghi nhận mức tiếp xúc. Các trường Review/Match dưới đây giữ nguyên; không gọi đây là hai lượt gắn nhãn độc lập.

| Case ID | Initial label từ snapshot | Review label | Match? | Reason for change | Review evidence |
| --- | --- | --- | --- | --- | --- |
| 01 | U — User Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 02 | S — System Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 03 | C — Context Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 04 | L — System Limitation | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 05 | H — Hidden Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 06 | U — User Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 07 | S — System Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 08 | S — System Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 09 | U — User Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 10 | C — Context Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 11 | L — System Limitation | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 12 | H — Hidden Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 13 | L — System Limitation | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 14 | U — User Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 15 | S — System Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 16 | C — Context Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 17 | H — Hidden Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 18 | C — Context Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 19 | L — System Limitation | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |
| 20 | S — System Error | PENDING | Not evaluated | PENDING — chưa có lượt review thật | PENDING |

## Nhãn kết luận đề xuất

Các nhãn đề xuất giữ nguyên initial và khớp tham khảo; chưa phải kết quả adjudication của hai lượt đánh giá. Cần người học xác nhận nhãn cuối.

| Case ID | Initial | Reference | Final đề xuất |
| --- | --- | --- | --- |
| 01 | U — User Error | Do người dùng | Do người dùng |
| 02 | S — System Error | Hệ thống | Hệ thống |
| 03 | C — Context Error | Ngữ cảnh | Ngữ cảnh |
| 04 | L — System Limitation | Giới hạn hệ thống | Giới hạn hệ thống |
| 05 | H — Hidden Error | Ngầm | Ngầm |
| 06 | U — User Error | Do người dùng | Do người dùng |
| 07 | S — System Error | Hệ thống | Hệ thống |
| 08 | S — System Error | Hệ thống | Hệ thống |
| 09 | U — User Error | Do người dùng | Do người dùng |
| 10 | C — Context Error | Ngữ cảnh | Ngữ cảnh |
| 11 | L — System Limitation | Giới hạn hệ thống | Giới hạn hệ thống |
| 12 | H — Hidden Error | Ngầm | Ngầm |
| 13 | L — System Limitation | Giới hạn hệ thống | Giới hạn hệ thống |
| 14 | U — User Error | Do người dùng | Do người dùng |
| 15 | S — System Error | Hệ thống | Hệ thống |
| 16 | C — Context Error | Ngữ cảnh | Ngữ cảnh |
| 17 | H — Hidden Error | Ngầm | Ngầm |
| 18 | C — Context Error | Ngữ cảnh | Ngữ cảnh |
| 19 | L — System Limitation | Giới hạn hệ thống | Giới hạn hệ thống |
| 20 | S — System Error | Hệ thống | Hệ thống |

## Kết quả và giới hạn

Reference accuracy initial = 20/20 × 100 = **100%**. Self-review consistency: **Not evaluated — PENDING**. Inter-rater agreement: **NOT MET — Individual Lab**; chưa có miễn trừ hoặc reviewer thứ hai. Công thức và giới hạn diễn giải được ghi tại [báo cáo lỗi](bang_loi.md#4-kết-quả-đối-chiếu-và-mức-độ-nhất-quán).

Snapshot [PENDING trước đó](cp3_initial_snapshot_PENDING_bcfb8102e793.md) giữ nguyên để truy xuất lịch sử; không dùng làm một lượt đánh giá.
