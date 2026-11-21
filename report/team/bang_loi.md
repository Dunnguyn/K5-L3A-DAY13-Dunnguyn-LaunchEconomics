# Bảng lỗi và biện pháp khắc phục

## 1. Thông tin và phương pháp

**Người thực hiện:** Nguyễn Thị Thùy Dung · **MSSV:** 2A202603552 · **Lớp:** L3A · **Hình thức:** Individual Lab.

**Trạng thái: CP3 PARTIAL. Self-review: PENDING. Inter-rater agreement: NOT MET — Individual Lab.**

Nguồn tình huống: [đề DOCX](../../docs/Ngay13_Lab13_De_bai_hoc_vien.docx), mục “Hai mươi ca lỗi”, bảng 9 của word/document.xml, đủ 20 ca. Định nghĩa và nhãn tham khảo theo [hướng dẫn Nhiệm vụ C](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md); yêu cầu nghiệm thu theo [RUBRIC](../../RUBRIC.md), [CHECKPOINTS](../../CHECKPOINTS.md) và [RULES](../../RULES.md).

**Nguồn kết quả và giới hạn:** bộ nhãn có hỗ trợ AI và đã đối chiếu tài liệu tham khảo; đây không phải phân loại độc lập của hai người. Nhãn initial, lời giải và giá trị AI Confidence gốc được giữ nguyên trong [snapshot](cp3_initial_snapshot_AI_assisted.md); confidence này không phải tự đánh giá của người học. Bằng chứng DOCX và đề xuất kết luận được bổ sung khi rà soát. Khai báo công cụ và cách kiểm chứng tập trung tại [báo cáo cá nhân](2A202603552_NguyenThiThuyDung.md#5-công-cụ-hỗ-trợ-và-kiểm-chứng).

SHA-256 snapshot: `3d0822a1e19bded7f806b058c1db838a7f9cc849564426858ba9c358bab0e417`. Snapshot được lưu trước lượt đối chiếu của trợ lý; điều này không chứng minh người thực hiện chưa xem tài liệu trước đó. Không có timestamp đánh giá hoặc reviewer bổ sung được tạo.

Lịch sử initial/review và nhãn đề xuất được ghi tại [phiếu đánh giá](cp3_danh_gia_ca_nhan.md). [Phiếu self-review](cp3_self_review.md) còn trống; chưa có cơ sở tính consistency hoặc thay đổi trạng thái đánh giá.


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

Bảng trình bày nhãn và phân tích nguyên nhân gốc hiện có. Bộ nhãn initial được bảo toàn trong snapshot; các nhãn kết luận vẫn là đề xuất chờ xác nhận, không phải kết quả của một lượt self-review mới.

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


## 4. Kết quả đối chiếu và mức độ nhất quán

Self-review consistency = số initial/review trùng / 20 × 100, chỉ tính khi đủ 20 cặp đánh giá thực tế. Inter-rater agreement cần hai người thật. Reference accuracy = số initial khớp tham khảo / 20 × 100.

| Metric | Bằng chứng | Số khớp / số không khớp | Kết quả | Nghiệm thu |
| --- | --- | --- | --- | --- |
| Self-review consistency | Chỉ có 1 bộ nhãn; Phase 2 PENDING | Not evaluated | Not evaluated | Chưa đủ điều kiện tính |
| Inter-rater agreement | Không có reviewer thứ hai thật | Not evaluated | Not evaluated | NOT MET — Individual Lab |
| Reference accuracy initial | Snapshot lưu trước lượt đối chiếu; 20 nhãn hợp lệ | 20 / 0 | 100% | Đạt mốc ≥16/20 về khớp nhãn |
| Reference match của nhãn kết luận đề xuất | 20 đề xuất giữ nguyên nhãn initial phù hợp tham khảo | 20 / 0 | 100% | Không phải lượt đánh giá độc lập mới |

Kết quả đối chiếu là **20/20 = 100%**, đạt mốc khớp nhãn ≥16/20. Kết quả này không thay thế self-review consistency hoặc inter-rater agreement; hai chỉ số chưa thực hiện giữ **Not evaluated**.


## 5. Phân tích khác biệt và quy tắc ranh giới

**Initial so reference:** không có bất đồng nhãn trong 20/20 ca; danh sách lệch reference rỗng, không cần sửa nhãn initial. **Initial so self-review:** Not evaluated, không được diễn đạt là “không có bất đồng” vì chưa có lượt review thứ hai.

Các nhãn kết luận đề xuất giữ nguyên cả 20 nhãn initial. Bên dưới là góp ý về độ chính xác của diễn đạt, **không phải bất đồng nhãn hoặc thay đổi bản gốc**:

| Ca | Diễn đạt trong initial gốc | Đối chiếu nguồn | Nhãn đề xuất |
| --- | --- | --- | --- |
| 02 | “chọn sai công cụ” | Đề nói gọi tool tra bảng giá với tham số hàng thường thay vì hàng nặng; nên nêu sai tham số/phân loại, không suy ra đã chọn tool khác | Hệ thống |
| 17 | “trước khi được phát hiện qua kiểm tra” | Đề nêu cache cũ, 212 đơn/9 ngày và không ai mở lại; không nêu audit/người/thời điểm phát hiện. Chỉ dựa vào sai âm thầm, không thêm sự kiện audit | Ngầm |
| 19 | “giới hạn thời gian lưu trữ/truy cập” | Đề chỉ xác nhận truy cập 12 tháng; không khẳng định dữ liệu cũ đã bị xóa hay giới hạn lưu trữ vật lý | Giới hạn hệ thống |

Quy tắc ranh giới cho các ca dễ nhầm:

- 01/06/09/14: root cause ở nhập/chọn/bấm sai; thiếu validation là vấn đề khắc phục, không tự đổi primary label.
- 05 so với 15: audit mới thấy 14 đơn hoàn thừa là Ngầm; nhân viên bắt mức 100% thay 50% trước gửi là Hệ thống.
- 08: trích Điều 7.2 không tồn tại là lỗi hệ thống hiển hiện trong căn cứ phản hồi, dù tiền hoàn đúng; không bịa audit để gắn Ngầm.
- 12: D05 token gấp 3 suốt 3 tuần không ai thấy là lỗi ngầm về chi phí; kết quả đúng không loại trừ tổn thất kinh tế.
- 13/19 so với 18: ngoài phạm vi/cửa sổ truy cập là Giới hạn; số tiền 15.000 VND đúng nhưng không giải thích là Ngữ cảnh.
- 20: gửi lại sau 10 phút không thay thế trách nhiệm idempotency; thiếu khóa làm hoàn hai lần là Hệ thống.

## 6. Biện pháp khắc phục

Tôi đề xuất 5 biện pháp, mỗi loại một ca: 01/U, 07/S, 18/C, 19/L, 05/H. Các loại lỗi khớp initial và nhãn tham khảo. Biện pháp chưa được triển khai; tiêu chí nghiệm thu trong bảng là yêu cầu kiểm chứng, không phải kết quả đã đạt.

Tất cả event, threshold, frequency và acceptance dưới đây là **đề xuất**, chưa tồn tại trong CSV. Mỗi event phải mang `trace_id`, `request_id`, thời điểm, phiên bản policy và mã giao dịch khi có; nội dung tài khoản phải che/mã hóa, không log số tài khoản đầy đủ.


| Case ID | Error Type | Detection Mechanism | Trigger / Threshold đề xuất | Monitoring Frequency đề xuất | Remediation Action đề xuất | Responsible Role đề xuất | Acceptance Criteria chưa kiểm chứng |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Do người dùng | `refund_input_validated`: đối chiếu schema và quy tắc tài khoản của ngân hàng được chọn | invalid_required_fields ≥1 hoặc bank_validation_failed = true | Mỗi lần submit, trước tạo lệnh hoàn | Chặn lệnh, đánh dấu trường sai và yêu cầu nhập lại; không cố định một độ dài cho mọi ngân hàng. Nếu vẫn không xác minh được thì handoff có mã lỗi | Product Manager | Test tài khoản thiếu 2 chữ số không tạo lệnh; dữ liệu hợp lệ theo từng ngân hàng được đi tiếp; mọi lần chặn có trace_id |
| 07 | Hệ thống | `refund_ledger_write` nối `refund_customer_notification` và ledger/read-back theo transaction_id | success_notification = true nhưng ledger_committed != true: count ≥1; lỗi 503 còn tồn tại sau retry | Mỗi giao dịch trước gửi; đối soát lại mỗi 5 phút | Chỉ gửi xác nhận thành công sau commit/read-back; giữ pending khi lỗi, không gửi lại lệnh thiếu idempotency; chuyển đối soát cho nhân viên khi hết retry | AI Engineering Lead | Fault injection 503 ở cả 3 lượt tạo 0 thông báo thành công; commit có bằng chứng mới xác nhận, retry không hoàn trùng |
| 18 | Ngữ cảnh | `refund_explanation_checked`: đối chiếu thông báo với fee, refund_rate, refund_amount, policy_version | Thiếu ≥1 trường bắt buộc/cách tính hoặc amount != fee × rate | Mỗi thông báo trước gửi; rà các yêu cầu mở lại hằng ngày | Dùng mẫu nêu phí 30.000, tỷ lệ 50%, hoàn 15.000 và căn cứ; nếu dữ liệu không khớp thì giữ thông báo để nhân viên kiểm tra | CSKH Lead | Test ca 18 chứa đủ 30.000 × 50% = 15.000 và nguồn policy; test thiếu trường bị chặn. Tác động lên hiểu đúng/mở lại phải đo trong pilot |
| 19 | Giới hạn hệ thống | `request_scope_checked` và `handoff_created`: so tuổi đơn với cửa sổ truy cập | Tuổi đơn >12 tháng thì phải handoff; thiếu ≥1 trường summary hoặc không có handoff_id là cảnh báo | Mỗi yêu cầu trước truy xuất; rà hàng chờ mỗi giờ | Nói rõ không truy cập đơn 14 tháng, không suy đoán trạng thái; tạo handoff kèm mã đơn, tuổi đơn, lý do giới hạn và thông tin đã thu thập | Operations Manager | Test đơn 14 tháng tạo đúng 1 handoff có summary và trace_id; 0 kết luận bịa trạng thái; kiểm thử thêm ranh giới 12 tháng theo múi giờ thống nhất |
| 05 | Ngầm | `refund_audit_checked`: tính lại số phải hoàn từ giá sau giảm, so với ledger và phiên bản policy | refund_amount − expected_post_discount_amount >0 VND: ≥1 ca xác minh | Đối soát tự động mọi hoàn có mã giảm giá mỗi ngày; audit độc lập 20 giao dịch/tuần hoặc toàn bộ nếu ít hơn 20 | Cách ly luồng tính giá khuyến mãi khi có lệch xác minh; sửa căn cứ giá sau giảm, rà lại các giao dịch bị ảnh hưởng và chuyển điều chỉnh cho kế toán | Finance Lead | Bộ test 14 đơn mô phỏng có lỗi như đề được phát hiện trong ≤24 giờ; sau sửa không còn lệch trên cùng bộ test và mỗi điều chỉnh truy xuất tới ledger |

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

Kiểm tra gồm: đối chiếu 20 ID, nhãn và giải thích với snapshot; kiểm tra bằng chứng DOCX; đếm kết quả khớp reference; rà soát cấu trúc bảng và 5 remediation. Các giới hạn về nguồn kết quả được nêu tại mục 1.

| QA ID | Expected | Actual | PASS / FAIL / NOT EVALUATED |
| --- | --- | --- | --- |
| QA-C01 | 20 ca ID 01–20, truy xuất nguồn | 20/20 đủ; nguyên văn DOCX và evidence khớp | PASS |
| QA-C02 | Initial hợp lệ và đầy đủ | 20/20 nhãn và giải thích hợp lệ; dữ liệu confidence gốc giữ trong snapshot | PASS |
| QA-C03 | Root cause và evidence cho nhãn kết luận | 20/20 nhãn đề xuất có root cause/evidence; final chính thức chưa được người học xác nhận | PASS |
| QA-C04 | Bảo toàn initial, không reviewer/kết quả giả | Snapshot trước reference, hash khớp; dữ liệu nguồn và snapshot cũ giữ nguyên | PASS |
| QA-C05 | Consistency trên hai lượt thật | Phase 2 PENDING; không có review thật để tính consistency | NOT EVALUATED |
| QA-C06 | Reference sau snapshot; khớp ≥16/20 | Đối chiếu đủ 20 ca: 20 đúng, 0 lệch, 100%; không gọi independent accuracy | PASS |
| QA-C07 | 5 ca đủ 5 nhóm | 01/07/18/19/05 bao phủ U/S/C/L/H; khớp initial và reference | PASS |
| QA-C08 | Event/source, threshold, frequency | 5/5 đề xuất đủ; hiệu quả acceptance chưa triển khai kiểm chứng | PASS |
| QA-C09 | Một accountable owner mỗi dòng | 5/5 có đúng 1 vai trò | PASS |
| QA-C10 | Không đổi CP1/CP2/CSV/starter/CP4–CP5 | Code, CSV và snapshot giữ nguyên; lần chuẩn hóa chỉ sửa tài liệu trình bày | PASS |
| QA-C11 | Markdown, provenance và trạng thái rõ | Đủ 9 mục; bảng đúng cột; initial/reference/final đề xuất/review PENDING tách riêng | PASS |
| QA-C12 | Regression thực tế, syntax, diff check | 30/30 tests PASS; lab13.py và py_compile thành công; git diff --check được chạy | PASS |

Lệnh regression chạy thực tế tại src bằng Python `.venv`:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
python lab13.py
python -m unittest -v test_cp1 test_cp2
python -m py_compile lab13.py test_cp1.py test_cp2.py
git diff --check
git status --short
```

Kết quả: **30 tests, 30 PASS, 0 FAIL**; A1 in “Ba phép thử đáp án biết trước: ĐẠT”. Baseline giữ nguyên 978 success, tổng 4.373.585,132 VND, CPS 4.471,968438 VND/success (**simulated**). Kiểm tra tài liệu/hashes không phải kiểm thử hiệu quả remediation.

Giới hạn còn lại: chưa có self-review thực tế, reviewer thứ hai hoặc miễn trừ; likelihood của cả 5 ca là Unknown; các event và remediation chưa được triển khai để đo hiệu quả.


## 9. Kết luận

CP3 đã có phân tích 20 ca, 5 nhóm lỗi, 5 đề xuất khắc phục và kết quả đối chiếu 20/20 = 100%. **Nghiệm thu vẫn PARTIAL**: self-review PENDING; inter-rater agreement NOT MET; nhãn kết luận đề xuất chờ người học xác nhận.

Cần bổ sung self-review thực tế nếu thực hiện và quyết định của giảng viên về cách nghiệm thu Individual Lab. Hai lượt của cùng một người không thay thế hai reviewer độc lập.

Các safety risks cần xem xét ở CP4–CP5: ca 07/20 về thông báo chưa commit hoặc hoàn trùng; ca 05/15/17 về sai tiền/phiên bản giá; ca 12 về chi phí âm thầm. Theo dõi ledger, notification, audit, validation, handoff và explanation với trace_id/request_id/transaction_id/policy_version. Ngưỡng ≥1 sai tiền hoặc giao dịch bất nhất được xác minh là đề xuất để đối soát luồng liên quan, chưa phải luật dừng đã áp dụng.

## 10. Lịch sử bằng chứng

Phiếu trống trước khi nhận bộ nhãn được giữ trong [snapshot PENDING](cp3_initial_snapshot_PENDING_bcfb8102e793.md), SHA-256 `bcfb8102e7931e7b0479e64ff1708ece9ea16a14617c3cbb188ece3241f34758`. Snapshot bộ nhãn được lưu riêng trước lượt đối chiếu; cả hai snapshot không chỉnh sửa. Hai phiên bản này là lịch sử tài liệu, không phải hai lượt đánh giá.
