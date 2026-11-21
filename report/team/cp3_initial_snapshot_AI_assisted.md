# CP3 — Error Taxonomy: AI-Assisted Classification

**Người thực hiện:** Nguyễn Thị Thùy Dung
**MSSV:** 2A202603552
**Lớp:** L3A
**Hình thức:** Individual Lab
**Phương pháp:** Phân tích nguyên nhân gốc có AI hỗ trợ, đối chiếu tài liệu hướng dẫn.

## Bảng phân loại 20 tình huống

| ID | Nhãn | Root Cause Explanation | AI Confidence |
| --- | --- | --- | --- |
| 01 | U — User Error | Khách hàng nhập số tài khoản ngân hàng thiếu hai chữ số, khiến dữ liệu đầu vào không hợp lệ. Nguyên nhân trực tiếp xuất phát từ thao tác nhập liệu của người dùng. | High |
| 02 | S — System Error | Kiện hàng nặng 28 kg nhưng agent gọi công cụ xử lý hàng thường. Agent chọn sai công cụ so với quy tắc phân loại trọng lượng. | High |
| 03 | C — Context Error | Agent hoàn tiền về ví điện tử đúng thiết kế, nhưng khách hàng kỳ vọng nhận tiền vào tài khoản ngân hàng. Kết quả đúng về kỹ thuật nhưng không phù hợp với kỳ vọng của khách. | High |
| 04 | L — System Limitation | Agent không có dữ liệu về chặng vận chuyển quốc tế cần thiết để xử lý yêu cầu. Nguyên nhân là thiếu dữ liệu trong phạm vi hệ thống hỗ trợ. | High |
| 05 | H — Hidden Error | Hệ thống tính tiền hoàn theo giá trước giảm thay vì giá thực trả. Sai lệch không được nhận ra trong quy trình thông thường mà chỉ được phát hiện khi kiểm toán. | High |
| 06 | U — User Error | Khách hàng chọn lý do giao hàng trễ trong khi nội dung phản ánh hàng bị vỡ. Nguyên nhân gốc là chọn sai loại yêu cầu, không phải lỗi xử lý của agent. | High |
| 07 | S — System Error | Công cụ ghi sổ giao dịch trả lỗi HTTP 503 nhưng agent vẫn thông báo hoàn tiền thành công. Agent không kiểm tra xác nhận giao dịch trước khi gửi thông báo. | High |
| 08 | S — System Error | Agent viện dẫn một điều khoản chính sách không tồn tại, dù số tiền hoàn đúng. Đây là hành vi tạo thông tin sai có thể nhận diện được từ nội dung phản hồi. | High |
| 09 | U — User Error | Khách hàng nhập mã đơn hàng trên sàn thương mại điện tử thay vì mã vận đơn. Dữ liệu đầu vào không đúng định dạng định danh mà hệ thống yêu cầu. | High |
| 10 | C — Context Error | Agent từ chối hoàn phí đúng chính sách liên quan đến bão, nhưng khách kỳ vọng được giải quyết theo cam kết dịch vụ. Vấn đề nằm ở sự khác biệt giữa quy tắc áp dụng và kỳ vọng thực tế. | High |
| 11 | L — System Limitation | Agent không thể xử lý thông tin khách cung cấp bằng tin nhắn thoại. Khả năng tiếp nhận và phân tích định dạng âm thanh chưa được hỗ trợ. | High |
| 12 | H — Hidden Error | Một trường dữ liệu bị thiếu khiến số token tăng bất thường trong thời gian dài mà không được phát hiện. Đây là lỗi ngầm về hiệu quả chi phí, dù kết quả phản hồi vẫn có thể đúng. | High |
| 13 | L — System Limitation | Yêu cầu bảo hiểm của đối tác nằm ngoài phạm vi hỗ trợ của agent. Việc giải thích giới hạn chưa tốt là điểm cần cải thiện nhưng không thay đổi nguyên nhân gốc. | High |
| 14 | U — User Error | Người dùng vô tình chọn trạng thái đã nhận tiền, khiến yêu cầu bị đóng. Nguyên nhân trực tiếp là thao tác xác nhận nhầm của người dùng. | High |
| 15 | S — System Error | Agent tính mức hoàn 100% thay vì 50% theo chính sách. Sai sót được nhân viên phát hiện trước khi gửi kết quả nên thuộc lỗi hệ thống đã lộ ra. | High |
| 16 | C — Context Error | Agent gửi thông báo đúng quy trình nhưng vào lúc 02:14 sáng. Hành vi hợp lệ về kỹ thuật nhưng không phù hợp với thời điểm và trải nghiệm của khách hàng. | High |
| 17 | H — Hidden Error | Bộ nhớ đệm sử dụng bảng giá cũ khiến 212 đơn bị tính sai. Sai lệch tồn tại trên nhiều giao dịch trước khi được phát hiện qua kiểm tra. | High |
| 18 | C — Context Error | Số tiền hoàn được tính đúng chính sách nhưng agent không giải thích cách tính, khiến khách khó hiểu kết quả. Hệ thống đã giả định khách có đủ thông tin để tự diễn giải. | High |
| 19 | L — System Limitation | Đơn hàng đã 14 tháng tuổi, vượt giới hạn truy xuất dữ liệu 12 tháng của hệ thống. Agent không thể xử lý đầy đủ vì giới hạn thời gian lưu trữ/truy cập. | High |
| 20 | S — System Error | Hệ thống thực hiện hoàn tiền hai lần vì thiếu cơ chế chống xử lý trùng giao dịch. Đây là lỗi kiểm soát nghiệp vụ và tính toàn vẹn giao dịch của hệ thống. | High |

## Tổng hợp kết quả phân loại

| Loại lỗi | Mã | Các tình huống | Số lượng |
| --- | --- | --- | ---: |
| User Error | U | 01, 06, 09, 14 | 4 |
| System Error | S | 02, 07, 08, 15, 20 | 5 |
| Context Error | C | 03, 10, 16, 18 | 4 |
| System Limitation | L | 04, 11, 13, 19 | 4 |
| Hidden Error | H | 05, 12, 17 | 3 |
| **Tổng** | | | **20** |

## Những trường hợp dễ nhầm

**Ca 05 và 15:** Cả hai đều tính sai tiền hoàn, nhưng ca 05 chỉ lộ ra khi audit nên là Hidden Error. Ca 15 được nhân viên phát hiện trước khi gửi nên là System Error.

**Ca 08:** Điều khoản không tồn tại là thông tin sai do agent tạo ra và có thể phát hiện trong phản hồi, nên thuộc System Error.

**Ca 12:** Kết quả vẫn có thể đúng nhưng token tăng bất thường mà không ai phát hiện. Hidden Error bao gồm cả lỗi chi phí.

**Ca 13:** Yêu cầu nằm ngoài phạm vi chức năng nên thuộc System Limitation, dù thông báo từ chối chưa phù hợp.

**Ca 18:** Agent hoàn đúng số tiền nhưng thiếu giải thích phù hợp với khách hàng, nên thuộc Context Error.

## Kết luận

Bộ phân loại gồm 20 tình huống, bao phủ đầy đủ năm nhóm lỗi. Hai nhóm cần ưu tiên kiểm soát trong pilot là System Error và Hidden Error, đặc biệt các trường hợp hoàn tiền sai, hoàn trùng, xác nhận giao dịch không thành công và sai lệch chi phí không được phát hiện.
