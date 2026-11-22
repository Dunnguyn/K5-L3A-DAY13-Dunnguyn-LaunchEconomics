# Bảng lỗi và biện pháp khắc phục

## 1. Thông tin và phương pháp

**Người thực hiện:** Nguyễn Thị Thùy Dung · **MSSV:** 2A202603552 · **Lớp:** L3A · **Hình thức:** Individual Lab.

**CP3: PARTIAL. Tỷ lệ trùng nhãn trong bảng tổng hợp: 18/20 = 90%, đã tính lại. Final Labels: CONFIRMED — 20/20. Bằng chứng đánh giá độc lập: PENDING.**

Tôi tổng hợp hai cột nhãn trong [bảng reviewer được cung cấp](cp3_reviewer_summary.md). Bảng có đủ Case ID 01–20, mỗi cột có 20 nhãn hợp lệ U/S/C/L/H. Tôi đã so từng cặp nhãn, xác định bất đồng tại Case 13 và 17, rồi đối chiếu nhãn đề xuất với bộ Final Labels đã xác nhận.

Nguồn tình huống: [đề DOCX](../../docs/Ngay13_Lab13_De_bai_hoc_vien.docx), mục “Hai mươi ca lỗi”, bảng 9. Taxonomy và nhãn tham khảo theo [hướng dẫn Nhiệm vụ C](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md). Điều kiện nghiệm thu theo [RUBRIC](../../RUBRIC.md), [CHECKPOINTS](../../CHECKPOINTS.md) và [RULES](../../RULES.md): hai bộ nhãn độc lập, agreement ≥80%, khớp reference ≥16/20 và 5 remediation đủ năm loại.

Theo ghi chú phương pháp trong nguồn bổ sung, hai reviewer đã xác nhận bảng nhưng bảng được chuẩn bị trước khi xác nhận. Tỷ lệ trùng nhãn 90% tính được từ bảng này chưa chứng minh hai người đã tự phân loại riêng trước khi xem bảng tổng hợp. Tôi giữ điều kiện đánh giá độc lập ở trạng thái PENDING cho tới khi có hai phiếu nhãn gốc hoặc bằng chứng về quá trình phân loại riêng biệt.

Phiếu đánh giá cá nhân và các snapshot lịch sử không còn trong HEAD/filesystem hiện tại sau commit `f33bac6`; nguồn trước đó được lưu tại `ed89502`, không phải file đang chờ xóa chưa commit. [Phiếu self-review hiện có](cp3_self_review.md) đã điền đủ 20/20 nhãn, giải thích và confidence; nhãn khớp Final Labels 20/20. Chưa có xác nhận người điền hoặc thời điểm đánh giá thực tế. Tôi không coi một bộ self-review, phiếu do trợ lý soạn hoặc bảng xác nhận là hai lượt reviewer độc lập.

## 2. Định nghĩa năm nhóm lỗi


| Error Type | Definition | Recognition Rule | Boundary With Other Types |
| --- | --- | --- | --- |
| Do người dùng | Đầu vào hoặc thao tác người dùng sai | Định vị dữ liệu/chọn mục/bấm nhầm khởi phát sự cố | Thiếu validation là điểm cải thiện, không tự đổi root cause thành Hệ thống |
| Hệ thống | Trả lời hoặc thực thi sai thiết kế/chính sách | Sai tính tiền, tham số tool, trích dẫn hoặc xác nhận không có căn cứ | Không gọi Ngầm chỉ vì chưa có khách phàn nàn; cần chứng cứ sai âm thầm không được nhận biết |
| Ngữ cảnh | Thực hiện đúng nhưng không phù hợp hoàn cảnh/kỳ vọng | Đối chiếu kết quả đúng với kênh, giờ, thông điệp hoặc giải thích khách cần | Thiếu diễn giải khác thiếu dữ liệu/khả năng để trả lời |
| Giới hạn hệ thống | Không đủ dữ liệu, phạm vi hay khả năng xử lý | Xác định giới hạn thực sự ở dữ liệu/định dạng/sản phẩm | Handoff kém là vấn đề phụ; không xóa nguyên nhân ngoài phạm vi |
| Ngầm | Sai nội dung/tiền/chi phí không được phát hiện khi vận hành | Nguồn nêu audit, thiếu cảnh báo hoặc sai kéo dài không ai nhận ra | Sai bị review/khách bắt không phải ngầm; chi phí bất thường vẫn là sai dù đáp án đúng |


Mỗi ca chỉ có 1 primary label; nếu có nhiều yếu tố, ghi rõ nguyên nhân ưu tiên và yếu tố phụ. Không cân bằng số ca theo đáp án, không chọn theo từ khóa. Khi đề thiếu dữ kiện về khả năng/phát hiện, ghi điểm chưa chắc thay vì bổ sung sự kiện.

## 3. Phân loại 20 tình huống

Người học đã tự rà soát và xác nhận 20/20 Final Labels; giữ nguyên nhãn và Root Cause. Ngày xác nhận: 22/11/2026. Trạng thái bộ nhãn cuối: **CONFIRMED — 20/20**.

**Phạm vi xác nhận:** đây là xác nhận bộ nhãn cuối của tôi, không thay thế hai bộ nhãn reviewer gốc hoặc biên bản phân xử bất đồng.

| Case ID | Error Type | Root Cause | Evidence |
| --- | --- | --- | --- |
| 01 | U — User Error | Ngân hàng từ chối lệnh → đầu vào thiếu hai chữ số theo đề → Do người dùng | DOCX bảng 9, ca 01: “thiếu hai chữ số” |
| 02 | S — System Error | Khách mở lại sau 2 ngày vì hoàn thiếu → tham số tool dùng hàng thường cho kiện 28 kg → Hệ thống | DOCX bảng 9, ca 02: “hàng thường thay vì hàng nặng” |
| 03 | C — Context Error | Luồng hoàn vào ví đúng thiết kế nhưng khách đợi tài khoản ngân hàng → kỳ vọng về nơi nhận không khớp → Ngữ cảnh | DOCX bảng 9, ca 03: “Khách chờ tiền về tài khoản ngân hàng” |
| 04 | L — System Limitation | Không xác định được trạng thái và chuyển nhân viên → LogiX không có dữ liệu chặng nước ngoài → Giới hạn hệ thống | DOCX bảng 9, ca 04: “LogiX không có dữ liệu chặng này” |
| 05 | H — Hidden Error | Audit cuối tuần thấy hoàn thừa trung bình 12.000 VND ở 14 đơn → tính theo giá trước giảm và không có báo lỗi/cảnh báo → Ngầm | DOCX bảng 9, ca 05: “Không khách nào báo, không cảnh báo nào kích” |
| 06 | U — User Error | Đơn đúng hạn bị từ chối trong luồng giao trễ → khách chọn sai mục so với nội dung hàng vỡ → Do người dùng | DOCX bảng 9, ca 06: “Khách chọn mục “Hoàn phí giao trễ”” |
| 07 | S — System Error | Thông báo hoàn thành sau ba lần ghi sổ lỗi 503 → trạng thái thông báo không được ràng buộc với kết quả ghi sổ → Hệ thống | DOCX bảng 9, ca 07: “vẫn báo khách “đã hoàn tiền thành công”” |
| 08 | S — System Error | Câu trả lời dẫn điều không có trong chính sách hiện hành dù số tiền đúng → căn cứ trả lời không được xác minh; đề không nêu người phát hiện cụ thể. → Hệ thống | DOCX bảng 9, ca 08: “Bản chính sách hiện hành không có điều 7.2” |
| 09 | U — User Error | Mã bị từ chối rồi dừng → khách nhập mã sàn thay mã vận đơn; thiếu gợi ý là vấn đề xử lý tiếp theo. → Do người dùng | DOCX bảng 9, ca 09: “thay vì mã vận đơn” |
| 10 | C — Context Error | Khách phản đối dù từ chối đúng điều khoản bất khả kháng → cam kết hiển thị không phản ánh hoàn cảnh bão → Ngữ cảnh | DOCX bảng 9, ca 10: “đúng chính sách” |
| 11 | L — System Limitation | Trợ lý yêu cầu nhập chữ → không có khả năng xử lý âm thanh trong đề → Giới hạn hệ thống | DOCX bảng 9, ca 11: “không xử lý được âm thanh” |
| 12 | H — Hidden Error | Token D05 gấp ba suốt ba tuần dù kết quả đúng → thiếu trường khiến gọi tool nhiều lần và không có phát hiện chi phí → Ngầm | DOCX bảng 9, ca 12: “suốt 3 tuần mà không ai thấy” |
| 13 | L — System Limitation | Trả lời chung về phí vận chuyển cho câu hỏi bảo hiểm đối tác → yêu cầu nằm ngoài phạm vi trợ lý; thông báo giới hạn còn thiếu → Giới hạn hệ thống | DOCX bảng 9, ca 13: “ngoài phạm vi trợ lý” |
| 14 | U — User Error | Yêu cầu đóng dù chưa nhận tiền → khách bấm nhầm xác nhận đã nhận; chưa đủ dữ kiện kết luận giao dịch ngân hàng lỗi. → Do người dùng | DOCX bảng 9, ca 14: “Khách bấm nhầm” |
| 15 | S — System Error | Nhân viên chặn mức hoàn 100% trước gửi → tính sai chính sách 50% cho trễ 26 giờ → Hệ thống | DOCX bảng 9, ca 15: “Nhân viên xem lại bắt được trước khi gửi” |
| 16 | C — Context Error | Thông báo đúng thiết kế gửi ngay nhưng làm phiền lúc 2:14 sáng → thiết kế chưa xét giờ yên tĩnh của khách → Ngữ cảnh | DOCX bảng 9, ca 16: “Theo thiết kế “gửi ngay khi xong”” |
| 17 | H — Hidden Error | Đơn dưới 2 kg lệch 1.000–2.000 VND suốt 9 ngày → cache không cập nhật bảng giá từ 01/11, 212 đơn không ai mở lại → Ngầm | DOCX bảng 9, ca 17: “212 đơn trong 9 ngày, không ai mở lại” |
| 18 | C — Context Error | Khách mở lại vì nghĩ hoàn thiếu → thông báo không giải thích mức 50% của phí 30.000 VND → Ngữ cảnh | DOCX bảng 9, ca 18: “không kèm cách tính” |
| 19 | L — System Limitation | Không tra được và chuyển nhân viên kèm tóm tắt → đơn 14 tháng vượt cửa sổ truy cập 12 tháng → Giới hạn hệ thống | DOCX bảng 9, ca 19: “chỉ truy cập được dữ liệu 12 tháng” |
| 20 | S — System Error | Cùng đơn được hoàn hai lần → lệnh thứ hai không có khóa chống trùng; đề chưa nói thời điểm/người phát hiện, không tự bổ sung. → Hệ thống | DOCX bảng 9, ca 20: “lệnh thứ hai không có khoá chống trùng” |

| Loại | Mã | Case IDs | Số ca |
| --- | --- | --- | --- |
| Do người dùng | U | 01, 06, 09, 14 | 4 |
| Hệ thống | S | 02, 07, 08, 15, 20 | 5 |
| Ngữ cảnh | C | 03, 10, 16, 18 | 4 |
| Giới hạn hệ thống | L | 04, 11, 13, 19 | 4 |
| Ngầm | H | 05, 12, 17 | 3 |

Tổng 20/20; phân bố U/S/C/L/H = 4/5/4/4/3. Số ca trong đề không dùng để ước lượng tần suất lỗi của pilot.

## 4. Tỷ lệ trùng nhãn và đối chiếu reference

Tôi đọc từng dòng trong [bảng nguồn](cp3_reviewer_summary.md), kiểm tra đủ 20 Case ID duy nhất 01–20 và nhãn hợp lệ ở cả hai cột. Tỷ lệ trùng nhãn được tính trên hai cột trước phân xử, không tính trên nhãn cuối đã thống nhất.

| Chỉ số | Cách kiểm tra | Kết quả | Trạng thái |
| --- | --- | --- | --- |
| Số cặp nhãn hợp lệ | Mỗi Case ID có nhãn Reviewer 01 và Reviewer 02 | 20/20 | PASS |
| Số cặp trùng / không trùng | So nhãn từng dòng | 18 trùng / 2 không trùng | VERIFIED — theo bảng tổng hợp |
| Tỷ lệ trùng nhãn | 18 / 20 × 100 | 90%; cao hơn ngưỡng 80% là 10 điểm phần trăm | PASS về tỷ lệ trong bảng |
| Case ID bất đồng | L/C ở Case 13; H/S ở Case 17 | Chính xác 13 và 17 | VERIFIED — theo bảng tổng hợp |
| Tính độc lập của hai lượt đánh giá | Cần bằng chứng tự phân loại riêng trước khi xem bảng | Chưa được chứng minh bởi bảng xác nhận | PENDING |
| Nhãn đề xuất so Final Labels đã xác nhận | So cột đề xuất trong bảng nguồn với mục 3 | 20/20 trùng; không cần đổi nhãn | CONFIRMED — bộ nhãn hiện tại |
| Final Labels so reference | So mục 3 với bảng “Nhãn tham khảo cho 20 ca” trong hướng dẫn | 20 trùng / 0 lệch = 100%; đạt ≥16/20 | PASS |

**Agreement trong bảng = 18/20 × 100 = 90%.** Đây là kết quả tính lại từ dữ liệu tổng hợp được cung cấp; chưa gọi là inter-rater agreement độc lập đã được nghiệm thu. Kết quả khớp reference 100% và phiếu self-review không thay thế bằng chứng hai người phân loại độc lập.

## 5. Bảng phân xử bất đồng

Hai ca bất đồng được xác định trực tiếp từ bảng nguồn: Case 13 và Case 17. Tôi giữ nguyên hai nhãn reviewer trong nguồn và phân tích theo tình huống của đề. Nhãn phân xử đề xuất L và H đều trùng bộ Final Labels tôi đã xác nhận; không có thay đổi cần xác nhận lại.

| Case ID | Reviewer 01 | Reviewer 02 | Phân tích Root Cause | Quy tắc phân biệt | Nhãn phân xử đề xuất | Đối chiếu Final Label |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | L — System Limitation | C — Context Error | Yêu cầu hoàn phí bảo hiểm đối tác nằm ngoài phạm vi chức năng của trợ lý. Trả lời chung chung và không nói rõ giới hạn là yếu tố giao tiếp phụ, không thay đổi nguyên nhân ngoài phạm vi. | Ngoài phạm vi chức năng → L. Có đủ khả năng xử lý nhưng kết quả đúng không phù hợp hoàn cảnh/kỳ vọng → C. | L — System Limitation | Trùng L đã CONFIRMED; giữ nguyên Root Cause |
| 17 | H — Hidden Error | S — System Error | Cache vẫn dùng bảng giá cũ từ 01/11 khiến đơn dưới 2 kg lệch 1.000–2.000 VND, kéo dài 212 đơn trong 9 ngày mà không ai mở lại. Lỗi kỹ thuật nằm ở cache; theo taxonomy bài lab, H phản ánh tính âm thầm kéo dài. Đề không nêu cơ chế hoặc thời điểm phát hiện cuối cùng. | Sai đã lộ ra trong xử lý thông thường → S; sai tồn tại âm thầm không được nhận biết qua kiểm soát thông thường → H. Không tự thêm sự kiện audit/người phát hiện. | H — Hidden Error | Trùng H đã CONFIRMED; giữ nguyên Root Cause |

Trạng thái: **đã phân tích và đối chiếu với bộ Final Labels CONFIRMED**. Bảng nguồn vẫn ghi nhãn phân xử là đề xuất; tôi không suy diễn rằng hai reviewer đã cùng chấp thuận phân xử hoặc rằng quá trình gắn nhãn đã độc lập. Xác nhận bộ nhãn cuối của tôi đã có từ ngày 22/11/2026 và không thay thế bằng chứng về quy trình reviewer.

Các quy tắc ranh giới tham chiếu khác:

- 01/06/09/14: root cause ở nhập/chọn/bấm sai; thiếu validation là vấn đề khắc phục, không tự đổi primary label.
- 05 so với 15: audit mới thấy 14 đơn hoàn thừa là Ngầm; nhân viên bắt mức 100% thay 50% trước gửi là Hệ thống.
- 08: trích Điều 7.2 không tồn tại là lỗi hệ thống hiển hiện trong căn cứ phản hồi, dù tiền hoàn đúng; không bịa audit để gắn Ngầm.
- 12: D05 token gấp 3 suốt 3 tuần không ai thấy là lỗi ngầm về chi phí; kết quả đúng không loại trừ tổn thất kinh tế.
- 13/19 so với 18: ngoài phạm vi/cửa sổ truy cập là Giới hạn; số tiền 15.000 VND đúng nhưng không giải thích là Ngữ cảnh.
- 20: gửi lại sau 10 phút không thay thế trách nhiệm idempotency; thiếu khóa làm hoàn hai lần là Hệ thống.

## 6. Biện pháp khắc phục

Tôi đề xuất 5 biện pháp, mỗi loại một ca: 01/U, 07/S, 18/C, 19/L, 05/H. Các loại lỗi khớp initial và nhãn tham khảo. Biện pháp chưa được triển khai; tiêu chí nghiệm thu trong bảng là yêu cầu kiểm chứng, không phải kết quả đã đạt.

Tất cả event, threshold, frequency và acceptance dưới đây là **đề xuất**, chưa tồn tại trong CSV. Mỗi event phải mang `trace_id`, `request_id`, thời điểm, phiên bản policy và mã giao dịch khi có; nội dung tài khoản phải che/mã hóa, không log số tài khoản đầy đủ.


| Case ID | Error Type | Detection Mechanism | Trigger / Threshold đề xuất | Monitoring Frequency đề xuất | Remediation Action đề xuất | Responsible Role đề xuất | Acceptance Criteria chưa kiểm chứng | Trạng thái kiểm chứng |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Do người dùng | `refund_input_validated`: đối chiếu schema và quy tắc tài khoản của ngân hàng được chọn | invalid_required_fields ≥1 hoặc bank_validation_failed = true | Mỗi lần submit, trước tạo lệnh hoàn | Chặn lệnh, đánh dấu trường sai và yêu cầu nhập lại; không cố định một độ dài cho mọi ngân hàng. Nếu vẫn không xác minh được thì handoff có mã lỗi | Product Manager | Test tài khoản thiếu 2 chữ số không tạo lệnh; dữ liệu hợp lệ theo từng ngân hàng được đi tiếp; mọi lần chặn có trace_id | Proposed/Planned |
| 07 | Hệ thống | `refund_ledger_write` nối `refund_customer_notification` và ledger/read-back theo transaction_id | success_notification = true nhưng ledger_committed != true: count ≥1; lỗi 503 còn tồn tại sau retry | Mỗi giao dịch trước gửi; đối soát lại mỗi 5 phút | Chỉ gửi xác nhận thành công sau commit/read-back; giữ pending khi lỗi, không gửi lại lệnh thiếu idempotency; chuyển đối soát cho nhân viên khi hết retry | AI Engineering Lead | Fault injection 503 ở cả 3 lượt tạo 0 thông báo thành công; commit có bằng chứng mới xác nhận, retry không hoàn trùng | Proposed/Planned |
| 18 | Ngữ cảnh | `refund_explanation_checked`: đối chiếu thông báo với fee, refund_rate, refund_amount, policy_version | Thiếu ≥1 trường bắt buộc/cách tính hoặc amount != fee × rate | Mỗi thông báo trước gửi; rà các yêu cầu mở lại hằng ngày | Dùng mẫu nêu phí 30.000, tỷ lệ 50%, hoàn 15.000 và căn cứ; nếu dữ liệu không khớp thì giữ thông báo để nhân viên kiểm tra | CSKH Lead | Test ca 18 chứa đủ 30.000 × 50% = 15.000 và nguồn policy; test thiếu trường bị chặn. Tác động lên hiểu đúng/mở lại phải đo trong pilot | Proposed/Planned |
| 19 | Giới hạn hệ thống | `request_scope_checked` và `handoff_created`: so tuổi đơn với cửa sổ truy cập | Tuổi đơn >12 tháng thì phải handoff; thiếu ≥1 trường summary hoặc không có handoff_id là cảnh báo | Mỗi yêu cầu trước truy xuất; rà hàng chờ mỗi giờ | Nói rõ không truy cập đơn 14 tháng, không suy đoán trạng thái; tạo handoff kèm mã đơn, tuổi đơn, lý do giới hạn và thông tin đã thu thập | Operations Manager | Test đơn 14 tháng tạo đúng 1 handoff có summary và trace_id; 0 kết luận bịa trạng thái; kiểm thử thêm ranh giới 12 tháng theo múi giờ thống nhất | Proposed/Planned |
| 05 | Ngầm | `refund_audit_checked`: tính lại số phải hoàn từ giá sau giảm, so với ledger và phiên bản policy | refund_amount − expected_post_discount_amount >0 VND: ≥1 ca xác minh | Đối soát tự động mọi hoàn có mã giảm giá mỗi ngày; audit độc lập 20 giao dịch/tuần hoặc toàn bộ nếu ít hơn 20 | Cách ly luồng tính giá khuyến mãi khi có lệch xác minh; sửa căn cứ giá sau giảm, rà lại các giao dịch bị ảnh hưởng và chuyển điều chỉnh cho kế toán | Finance Lead | Bộ test 14 đơn mô phỏng có lỗi như đề được phát hiện trong ≤24 giờ; sau sửa không còn lệch trên cùng bộ test và mỗi điều chỉnh truy xuất tới ledger | Proposed/Planned |

## 7. Ưu tiên xử lý rủi ro

Đây là đánh giá định tính và ưu tiên đề xuất, không phải số liệu đo. **Likelihood = Unknown cho cả 5 ca** vì 20 tình huống không cung cấp mẫu số hay tần suất; số 14 đơn của ca 05 chỉ là dữ kiện tình huống. Detectability mô tả khả năng nhận biết bằng quy trình thông thường trước khi thêm remediation.


| Case ID | Impact | Likelihood | Detectability | Operational Priority | Cơ sở và lớp kiểm soát đề xuất |
| --- | --- | --- | --- | --- | --- |
| 01 | Medium | Unknown | Easy | P2 | Ngân hàng trả lỗi thấy được, làm chậm hoàn; chặn input trước tạo lệnh và handoff khi không xác minh |
| 07 | High | Unknown | Moderate | P1 | Báo đã hoàn dù 503 gây mất tin cậy và tranh chấp; chặn xác nhận trước gửi, đối soát ledger và handoff |
| 18 | Medium | Unknown | Moderate | P2 | 15.000 VND đúng nhưng thiếu cách tính gây mở lại; kiểm tra giải thích trước gửi và theo dõi mở lại định kỳ |
| 19 | Medium | Unknown | Easy | P2 | Cửa sổ 12 tháng rõ ràng, đơn 14 tháng phải handoff; kiểm tra đủ tóm tắt và hàng chờ định kỳ |
| 05 | High | Unknown | Difficult | P1 | Hoàn thừa không ai báo; hậu kiểm ledger/giá sau giảm hằng ngày, điều chỉnh sau xác minh và chặn luồng sai |


Ưu tiên P1 cho ca 07 và 05 vì giao dịch/thông báo sai có thể không tự lộ qua chỉ số sử dụng. Ca 15/17/20 cũng là safety risks cần mang sang CP4 để xem xét, nhưng không thêm vào 5 dòng remediation bắt buộc và không tuyên bố đã đặt luật dừng.

## 8. Kiểm chứng và giới hạn

Lượt nghiệm thu ngày 22/11/2026 kiểm tra file hiện có, lịch sử Git, nhãn cuối so reference, tính đầy đủ của remediation và regression CP1–CP2.

| QA ID | Nội dung | Bằng chứng hiện tại | Trạng thái |
| --- | --- | --- | --- |
| QA-C01 | Đủ 20 Case ID và Root Cause | 01–20, mỗi ca một nhãn U/S/C/L/H và evidence; bảng giữ nguyên | PASS |
| QA-C02 | Hai bộ nhãn reviewer độc lập | Có bảng tổng hợp 20 cặp nhãn; chưa có bằng chứng hai người tự phân loại riêng trước khi xem bảng | PENDING |
| QA-C03 | Xác nhận nhãn cuối | Xác nhận của tôi ngày 22/11/2026; đủ 20 Final Labels | CONFIRMED |
| QA-C04 | Tỷ lệ trùng nhãn trong bảng ≥80% | Tái tính từ đủ 20 cặp: 18 trùng, 2 lệch, 90% | PASS — theo bảng tổng hợp |
| QA-C05 | Hai ca bất đồng và phân xử | Case 13 L/C → L; Case 17 H/S → H; có Root Cause/quy tắc, khớp Final Labels đã xác nhận | PASS |
| QA-C06 | Final Labels khớp reference ≥16/20 | Tính lại từ bảng hiện tại và hướng dẫn: 20/20 = 100% | PASS |
| QA-C07 | 5 remediation bao phủ 5 nhóm | 01/U, 07/S, 18/C, 19/L, 05/H | PASS |
| QA-C08 | Cách phát hiện đo được | 5/5 có event/source, threshold và frequency | PASS |
| QA-C09 | Một vai trò chịu trách nhiệm mỗi dòng | 5/5 có đúng một owner; giữ nguyên biện pháp | PASS |
| QA-C10 | Bảo toàn dữ liệu | Giữ nguyên code/test CP1–CP2, CSV, reviewer labels và nội dung self-review; không ghi đè nguồn nhãn lịch sử | PASS |
| QA-C11 | Regression CP1–CP2 | Chạy thực tế 30 tests: 30 PASS, 0 FAIL | PASS |
| QA-C12 | Kiểm tra diff | `git diff --check` không báo lỗi | PASS |

Lệnh regression từ thư mục gốc repository:

```powershell
Push-Location src
.\.venv\Scripts\python.exe -m unittest -v test_cp1 test_cp2
Pop-Location
git diff --check
```

Lượt chạy đầu có 29/30 PASS: test bảo toàn báo cáo CP1 phát hiện câu mở đầu `bang_chi_phi.md` bị sửa ở lượt trước. Tôi khôi phục đúng câu gốc theo `HEAD`, không thay code hoặc tests; lượt chạy lại đạt **30/30 PASS**. Đây là khôi phục nội dung CP1 để đáp ứng kiểm tra bảo toàn, không phải thay đổi mô hình chi phí.

Các test này xác minh CP1–CP2, không kiểm chứng nhãn reviewer hoặc hiệu quả remediation. Các event và remediation vẫn Proposed/Planned; likelihood của cả 5 ca là Unknown vì không có mẫu số để ước lượng tần suất.

## 9. Checklist nghiệm thu cuối cùng

**CP3: PARTIAL.** Tôi đã tái tính đủ 20 cặp nhãn: 18/20 = 90%; đã phân tích Case 13 và 17, đối chiếu khớp bộ Final Labels CONFIRMED 20/20. Năm remediation đáp ứng cấu trúc yêu cầu. Điều kiện còn PENDING là bằng chứng hai reviewer tự phân loại riêng trước khi xem bảng tổng hợp.

| Điều kiện | Kết quả | Trạng thái |
| --- | --- | --- |
| Taxonomy, 20 tình huống, Root Cause và evidence | Đủ; giữ nguyên nội dung | DONE |
| Hai bộ nhãn reviewer độc lập | Có bảng tổng hợp; chưa có phiếu gốc hoặc bằng chứng phân loại riêng trước khi xem bảng | PENDING |
| Tỷ lệ trùng nhãn ≥16/20 = 80% | Tái tính 18/20 = 90% từ bảng tổng hợp; tính độc lập xét riêng | DONE — theo bảng tổng hợp |
| Xác định và phân tích hai ca bất đồng | Case 13 L/C → L; Case 17 H/S → H; khớp nhãn cuối đã xác nhận | DONE |
| Final Labels được người học xác nhận | 20/20 đã xác nhận ngày 22/11/2026; không thay đổi | CONFIRMED |
| Final Labels khớp reference ≥16/20 | Tính lại 20/20 = 100% | DONE |
| 5 remediation đủ năm loại và phát hiện đo được | Giữ nguyên 5/5, có event, ngưỡng, tần suất và một owner | DONE — Proposed/Planned |
| Regression CP1–CP2 | 30/30 PASS, 0 FAIL | DONE |
| `git diff --check` | Không có lỗi | DONE |
| Code CP1–CP2, CSV, dữ liệu reviewer gốc | Không sửa; không tự commit/push | DONE |

Một bộ self-review đã điền không phải bằng chứng hai reviewer độc lập và không thay thế điều kiện agreement. Người điền và thời điểm đánh giá của phiếu hiện có vẫn chưa được xác minh. Kiểm chứng hiệu quả remediation trong pilot là bước vận hành sau, không được mô tả như đã thực hiện. Tôi cần hai phiếu nhãn gốc hoặc bằng chứng về quá trình phân loại riêng trước khi xem bảng để nghiệm thu điều kiện độc lập; bộ Final Labels hiện tại đã được xác nhận và không thay đổi.

Các safety risks cần xem xét ở CP4–CP5: ca 07/20 về thông báo chưa commit hoặc hoàn trùng; ca 05/15/17 về sai tiền/phiên bản giá; ca 12 về chi phí âm thầm. Theo dõi ledger, notification, audit, validation, handoff và explanation với trace_id/request_id/transaction_id/policy_version. Ngưỡng ≥1 sai tiền hoặc giao dịch bất nhất được xác minh là đề xuất để đối soát luồng liên quan, chưa phải luật dừng đã áp dụng.

## 10. Lịch sử bằng chứng

Các phiếu và snapshot nhãn lịch sử không còn trong HEAD hiện tại sau commit `f33bac6`; có thể đọc bản trước tại commit `ed89502`. Phiếu cá nhân lịch sử có một bộ initial và Phase 2 PENDING, không mô tả hiện trạng của `cp3_self_review.md` đã điền đủ20 dòng. Các snapshot lịch sử không tạo thành hai lượt phân loại của hai người. Tôi giữ nguyên nguồn nhãn và không dùng xác nhận hash/liên kết cũ làm bằng chứng đánh giá độc lập. Mẫu báo cáo `MSSV_HoTen.md` được khôi phục riêng từ `ed89502` để đáp ứng yêu cầu nộp, không phải phiếu reviewer.

Nguồn bổ sung là bảng tổng hợp do tôi cung cấp trong cuộc trao đổi ngày 22/11/2026, được chép tại `cp3_reviewer_summary.md`. Hai cột nhãn được giữ nguyên và tính lại ra 18/20 = 90%, bất đồng tại 13 và 17. Bảng này không được mô tả thành hai phiếu gốc đã chứng minh tính độc lập. Bộ Final Labels tại mục 3, tài liệu trong `docs/`, xác nhận nhãn cuối trước đó và kết quả regression tiếp tục được dùng để đối chiếu.
