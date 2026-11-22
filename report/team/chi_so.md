# Đặc tả chỉ số, event và rủi ro kinh tế · CP5 E1–E2

Nguyễn Thị Thùy Dung · 2A202603552 · L3A · Individual Lab. **CP5 CONTENT COMPLETE** về tài liệu/phép tính; Gate 2a **PENDING EXTERNAL REVIEW**; Pilot **Planned / Not Approved**.


## E1 · Đặc tả KPI

### Nguồn và phép tính mô tả

Toàn bộ CSV là trace giả lập của lab, không phải số đo vận hành thực tế. Các cờ nhị phân là dữ liệu được cung cấp; CSV không có timestamp để tự xác minh lại thời hạn 24 giờ/7 ngày, không có arm, event dùng agent hoặc kết quả audit. Tôi tính mô tả theo cờ, không suy diễn causal lift.

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | KPI-01 · Tỷ lệ yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `(dong_trong_24h == 1) AND (mo_lai_trong_7_ngay == 0)`, chia tổng yêu cầu đủ điều kiện | 994/1.200 = **82,83%**; mô tả trace lab |
| Dùng | KPI-02 · Tỷ lệ gợi ý bị sửa hoặc bỏ | Request đã review có quyết định `sua` hoặc `bo`, chia số request đã review | 48/177 = **27,12%**; mô tả trace lab |
| An toàn | KPI-03 · Tỷ lệ yêu cầu mở lại trong 7 ngày | Request có `mo_lai_trong_7_ngay == 1`, chia tổng request có kết quả trong CSV | 51/1.200 = **4,25%** toàn mẫu; 39/982 = **3,97%** trong scope noi_dia + hang_nang |
| Dùng (tự đề xuất) | KPI-04 · Agent Usage Rate | Eligible request treatment có ít nhất một `agent_action_used`, chia mọi eligible request được giao treatment | Chưa có event tương ứng trong CSV; **chưa đo** |
| An toàn (tự đề xuất) | KPI-05 · Verified Incorrect Refund Rate | Request audit ngẫu nhiên hợp lệ xác nhận hoàn sai, chia tổng request audit ngẫu nhiên hợp lệ | Chưa có audit/ledger event trong CSV; **chưa đo** |

Baseline 70% của CP4 là **giả định thiết kế**, không phải tỷ lệ control quan sát. Không lấy 82,83% trừ 70% để tuyên bố hiệu quả. Tỷ lệ mở lại là proxy an toàn, không khẳng định mọi lần mở lại do agent gây ra; cần audit để phát hiện sai hoàn tiền không bị khách mở lại.

KPI-01 làm tròn 82,83%; KPI-02 là 27,12%. Trong 177 requests reviewed có 129 giữ, 41 sửa và 7 bỏ: `(41+7)/177`, không chia cho 1.200. Primary 994 khác successful resolutions CP1 là 978: CP1 dùng ket_qua=thanh_cong (có điều kiện không sai tiền), còn KPI-01 dùng hai cờ 24h/7 ngày; hai định nghĩa không tương đương. Baseline 70% của CP4 là **giả định thiết kế**, không phải control quan sát; không lấy 82,83% trừ 70% để tuyên bố hiệu quả agent.

### KPI Specification Table

| KPI ID | Name | Numerator | Denominator | Filter/Window | Baseline/Result | Event Sources | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KPI-01 | Đóng trong 24h và không mở lại 7 ngày | Requests duy nhất đóng <=24h từ received_at, không reopened trong 7 ngày từ closed_at | Tất cả eligible requests kỳ chính theo ITT; không loại handoff, lỗi hoặc non-use | Pilot scope noi_dia + hang_nang; tách arm ban đầu; chờ cohort trưởng thành, trường hợp không đóng đúng 24h là không đạt | CSV lab 994/1200 = 82,83%; baseline thiết kế .70, MDE .06 | refund_request_created, ticket_closed, ticket_reopened, request_observation_finalized | Product Manager | Mô tả lab đã tính; đo pilot chưa triển khai |
| KPI-02 | Gợi ý bị sửa/bỏ, cấp request | Requests reviewed có quyết định sửa/bỏ cho gợi ý chuẩn của request | Requests đã review, đếm request_id duy nhất; không gồm shown chưa review | Cohort tuần; mỗi request chọn gợi ý đầu tiên có review theo shown_at/suggestion_id, lấy quyết định cuối hợp lệ của gợi ý đó | CSV lab 48/177 = 27,12%; không phải adoption | agent_suggestion_shown, agent_suggestion_viewed, staff_review_decision | Trưởng nhóm CSKH | Mô tả lab đã tính; pilot cần instrumentation |
| KPI-03 | Mở lại trong 7 ngày | Requests duy nhất reopened <=7 ngày từ lần đóng đầu tiên | Requests trong cohort có cửa sổ reopen trưởng thành và coverage_complete; báo riêng requests chưa đóng/chưa đủ cửa sổ | Theo arm, scope và cohort tuần; không gán 0 nếu thiếu log/follow-up | Lab 51/1200 = 4,25%; scope 39/982 = 3,9715% | refund_request_created, ticket_closed, ticket_reopened, request_observation_finalized | Operations Manager | Mô tả lab đã tính; safety proxy |
| KPI-04 | Agent Usage Rate | Eligible requests treatment có >=1 agent_action_used do staff chủ động request_run hoặc apply_suggestion | Tất cả eligible requests giao cho treatment trong cùng cohort, gồm không mở/không dùng | Theo tuần và kỳ chính; dedup request_id; mở UI hay chỉ xem gợi ý không tự tính là sử dụng | Không có kết quả từ CSV | refund_request_created, agent_ui_opened, agent_suggestion_viewed, agent_action_used | Product Manager | Proposed — Not Yet Measured |
| KPI-05 | Verified Incorrect Refund Rate | Requests audit ngẫu nhiên có verified_incorrect=true: thừa/thiếu tiền, sai tỷ lệ, giá hết hiệu lực hoặc hoàn trùng có bằng chứng | Requests audit ngẫu nhiên hợp lệ, duy nhất; không dùng số giao dịch làm mẫu số | Mỗi tuần/arm; chỉ audit hoàn tất, linked ledger/policy và sampling_frame=random; audit nhắm đích báo riêng | Không có kết quả từ CSV hoặc 20 ca CP3 | refund_request_created, refund_ledger_write, audit_sample_checked, refund_customer_notification | Finance Lead | Proposed — Not Yet Measured |

**Quy tắc pilot:** ITT giữ assigned_staff_id và arm gốc kể cả handoff/crossover; không chuyển arm theo người xử lý cuối. Primary báo cả tử số, mẫu số, missing và 95% CI điều chỉnh clustering theo staff, theo CP4. Cohort chưa đủ follow-up không vào phân tích cuối; khi đã đủ cửa sổ mà outcome thiếu thì primary coi không đạt, có sensitivity best/worst; missing >5% một arm chặn kết luận hiệu lực. Request không đóng không tự được gán reopen=0: báo số không đóng và mẫu số trưởng thành của KPI-03, tránh so tỷ lệ giữa các mẫu số khác nhau.

**Funnel sử dụng:** đo riêng shown, viewed, reviewed, kept, modified, rejected, no_decision và action_used. KPI-02 ở cấp request; SR-03 của CP4 ở cấp suggestion_id: `(sua+bo)/reviewed suggestions`, >=100 suggestion/tuần. Không tráo mẫu số hoặc dùng KPI-02 làm proxy adoption. Không có reviewed/audited denominator thì tỷ lệ là Not evaluated, không phải 0%.

**Audit:** Finance Lead khóa sampling seed và frame trước tuần, lấy ngẫu nhiên đơn giản 20 requests/arm/tuần hoặc toàn bộ nếu ít hơn 20; lưu inclusion_probability và nonresponse. Đối chiếu tổng các ledger entry cùng request với số đúng theo policy/pricing có hiệu lực tại thời điểm giao dịch, refund_count/idempotency và notification. Mỗi request chỉ một kết quả audit tổng hợp; mức độ low/high/critical, hoàn trùng và thành công giả là critical, điều tra ngay theo SR-01. Audit nhắm đích mọi incident và giao dịch rủi ro cao được ghi sampling_frame=targeted, báo riêng; không gộp thẳng vào tỷ lệ mẫu ngẫu nhiên. Báo sai số và số đếm theo arm, không xem 20 mẫu/arm là bảo đảm đủ sức phát hiện lỗi hiếm. Sai tiền và thành công giả được báo riêng; thành công giả kích hoạt incident ngay dù chưa có tiền hoàn để tính KPI-05.

## Danh sách event

Các event dưới đây là **đặc tả đề xuất**, chưa được instrument hoặc thu thập trong pilot. Mỗi event có `trace_id` để nối luồng xử lý; control cũng nhận correlation ID từ lúc tạo request.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| refund_request_created | Ticket intake | `trace_id`, `request_id`, `event_timestamp`, `assigned_staff_id`, `depot_id`, `arm`, `eligible`, `request_correlation_id` | Khi nhận request và chốt eligibility/assignment |
| agent_run_completed | Agent orchestrator | `trace_id`, `request_id`, `event_timestamp`, `run_id`, `attempt`, `staff_id`, `arm`, `status`, `policy_version`, `pricing_version` | Mỗi run kết thúc, kể cả lỗi |
| agent_suggestion_shown | Staff UI | `trace_id`, `request_id`, `event_timestamp`, `suggestion_id`, `staff_id`, `arm`, `proposed_refund_amount` | Khi gợi ý được render |
| staff_review_decision | Review UI | `trace_id`, `request_id`, `event_timestamp`, `suggestion_id`, `staff_id`, `arm`, `decision`, `review_duration_minutes` | Khi lưu quyết định giữ/sửa/bỏ |
| staff_rework_completed | CSKH workflow | `trace_id`, `request_id`, `event_timestamp`, `rework_id`, `staff_id`, `rework_duration_minutes`, `reason`, `error_type` | Khi hoàn tất work session làm lại |
| refund_ledger_write | Ledger service | `trace_id`, `request_id`, `event_timestamp`, `transaction_id`, `attempt`, `idempotency_key`, `ledger_status`, `refund_amount`, `committed_at` | Mỗi lần ghi hoặc đọc lại trạng thái giao dịch |
| handoff_to_staff | Routing service | `trace_id`, `request_id`, `event_timestamp`, `handoff_id`, `assigned_staff_id`, `handling_staff_id`, `arm`, `reason` | Khi chuyển request cho người xử lý |
| ticket_closed | Ticket service | `trace_id`, `request_id`, `event_timestamp`, `closed_at`, `closure_id`, `staff_id`, `arm`, `resolution_status` | Khi ticket được đóng |
| ticket_reopened | Ticket service | `trace_id`, `request_id`, `event_timestamp`, `reopened_at`, `closure_id`, `reason`, `arm` | Khi ticket được mở lại |
| audit_sample_checked | Finance audit | `trace_id`, `request_id`, `event_timestamp`, `audit_id`, `sampling_frame`, `valid_audit`, `verified_incorrect`, `severity` | Khi hoàn tất hoặc đánh dấu audit không hợp lệ |
| agent_ui_opened | Staff UI | `trace_id`, `request_id`, `event_timestamp`, `staff_id`, `arm`, `session_id` | Khi nhân viên mở màn hình agent |
| agent_suggestion_viewed | Staff UI | `trace_id`, `request_id`, `event_timestamp`, `suggestion_id`, `staff_id`, `arm`, `viewed_at` | Khi nhân viên chủ động xem gợi ý |
| agent_action_used | Staff UI | `trace_id`, `request_id`, `event_timestamp`, `staff_id`, `arm`, `action`, `action_id`, `initiated_by` | Khi nhân viên chủ động yêu cầu chạy agent hoặc áp dụng gợi ý |
| refund_customer_notification | Notification service | `trace_id`, `request_id`, `event_timestamp`, `notification_id`, `transaction_id`, `notified_status`, `ledger_status_at_send` | Khi gửi thông báo trạng thái cho khách |
| request_observation_finalized | Data pipeline | `trace_id`, `request_id`, `event_timestamp`, `arm`, `followup_complete_at`, `coverage_complete`, `source_watermark`, `missing_reason` | Khi đủ cửa sổ quan sát và kiểm tra độ đầy đủ |

**Kiểm tra chéo:**

| Chỉ số | Event dùng để tính | Đo được từ CSV hiện có? | Còn thiếu |
| --- | --- | --- | --- |
| KPI-01 · Primary outcome | `refund_request_created`, `ticket_closed`, `ticket_reopened`, `request_observation_finalized` | Có thể tính mô tả từ cờ CSV; chưa xác minh timestamp/ITT | Timestamp thật, roster/arm, coverage và follow-up |
| KPI-02 · Sửa/bỏ gợi ý | `agent_suggestion_shown`, `agent_suggestion_viewed`, `staff_review_decision` | Có thể tính mô tả từ CSV; chưa có suggestion-level funnel | `suggestion_id`, event shown/viewed và decision đã instrument |
| KPI-03 · Mở lại | `refund_request_created`, `ticket_closed`, `ticket_reopened`, `request_observation_finalized` | Có thể tính mô tả từ cờ CSV; chưa xác minh cửa sổ/coverage | Timestamp thật, cohort trưởng thành và source watermark |
| KPI-04 · Agent Usage Rate | `refund_request_created`, `agent_ui_opened`, `agent_suggestion_viewed`, `agent_action_used` | Chưa đo được | Action audit để phân biệt mở UI, xem và thực sự dùng |
| KPI-05 · Verified Incorrect Refund Rate | `refund_request_created`, `refund_ledger_write`, `audit_sample_checked`, `refund_customer_notification` | Chưa đo được | Audit ngẫu nhiên, ledger join, policy/pricing version và notification outbox |

## Event Tracking Specification

Mọi event có `event_id` duy nhất, `trace_id`, `request_id`, `event_timestamp` dạng UTC có timezone và `schema_version`; pipeline bổ sung `ingested_at` để kiểm tra độ trễ; các bảng dưới lặp bốn khóa bắt buộc để kiểm tra coverage. Required Properties liệt kê thêm thuộc tính riêng. Mọi event là **Proposed — Not Instrumented**, không phải log đã có. Data Source là nguồn hệ thống dự kiến.

| Event Name | Producer | Trigger | Required Properties | Data Source | KPI Supported |
| --- | --- | --- | --- | --- | --- |
| refund_request_created | Ticket intake | Nhận request và chốt eligibility/assignment ban đầu | event_id, trace_id, request_id, event_timestamp, received_at, assigned_staff_id, depot_id, arm, loai, eligible, exclusion_reason, roster_version, request_correlation_id | Ticket intake + roster đã khóa | KPI-01, KPI-02, KPI-03, KPI-04, KPI-05 |
| agent_run_completed | Agent orchestrator | Mỗi run kết thúc, kể cả lỗi | event_id, trace_id, request_id, event_timestamp, run_id, attempt, staff_id, arm, status, tokens_in, tokens_out, tool_calls, policy_version, pricing_version | Run trace | Cost, retry, anomaly; KPI-04 đối soát |
| agent_suggestion_shown | Staff UI | Gợi ý được render cho staff | event_id, trace_id, request_id, event_timestamp, suggestion_id, staff_id, arm, shown_at, proposed_refund_amount, policy_version, pricing_version | UI telemetry | KPI-02; funnel KPI-04 |
| staff_review_decision | Review UI | Lưu quyết định giữ/sửa/bỏ | event_id, trace_id, request_id, event_timestamp, suggestion_id, staff_id, arm, decision, decision_version, review_started_at, review_completed_at, review_duration_minutes | Review audit | KPI-02, SR-03, review cost |
| staff_rework_completed | CSKH workflow | Hoàn tất một work session làm lại | event_id, trace_id, request_id, event_timestamp, rework_id, staff_id, arm, rework_started_at, rework_completed_at, rework_duration_minutes, reason, error_type | Staff worklog | Rework rate/cost; RISK-01 |
| refund_ledger_write | Ledger service | Mỗi lần ghi/đọc lại trạng thái giao dịch | event_id, trace_id, request_id, event_timestamp, transaction_id, attempt, idempotency_key, ledger_status, refund_amount, currency, committed_at, policy_version, pricing_version | Ledger + read-back | KPI-05, SR-01, cost reconciliation |
| handoff_to_staff | Routing service | Chuyển ngoài phạm vi/lỗi/pending cho người xử lý | event_id, trace_id, request_id, event_timestamp, handoff_id, assigned_staff_id, handling_staff_id, arm, reason, summary, source_transaction_id | Handoff queue | KPI-01 ITT, fallback cost |
| ticket_closed | Ticket service | Đóng ticket | event_id, trace_id, request_id, event_timestamp, closed_at, closure_id, staff_id, arm, resolution_status | Ticket state history | KPI-01, KPI-03 |
| ticket_reopened | Ticket service | Request được mở lại | event_id, trace_id, request_id, event_timestamp, reopened_at, closure_id, reason, arm | Ticket state history | KPI-01, KPI-03 |
| audit_sample_checked | Finance audit | Hoàn tất hoặc đánh dấu audit chưa hợp lệ | event_id, trace_id, request_id, event_timestamp, audit_id, sampling_frame, sampling_seed, inclusion_probability, arm, valid_audit, actual_refund_amount, expected_refund_amount, refund_count, verified_incorrect, error_type, severity, transaction_ids, policy_version, pricing_version, auditor_role | Audit register + ledger/policy | KPI-05; SR-01 |
| agent_ui_opened | Staff UI | Staff mở màn hình agent | event_id, trace_id, request_id, event_timestamp, staff_id, arm, session_id | UI telemetry | Funnel KPI-04, contamination |
| agent_suggestion_viewed | Staff UI | Staff chủ động mở/xem nội dung gợi ý | event_id, trace_id, request_id, event_timestamp, suggestion_id, staff_id, arm, viewed_at | UI telemetry | Funnel KPI-04, KPI-02 |
| agent_action_used | Staff UI | Staff chủ động yêu cầu run hoặc áp dụng gợi ý | event_id, trace_id, request_id, event_timestamp, staff_id, arm, action, action_id, initiated_by, suggestion_id_if_applicable, run_id_if_applicable | UI action audit | KPI-04 |
| refund_customer_notification | Notification service | Gửi thông báo trạng thái cho khách | event_id, trace_id, request_id, event_timestamp, notification_id, transaction_id, notified_status, ledger_status_at_send, sent_at, staff_id, arm | Notification outbox + ledger | KPI-05 đối soát, SR-01 |
| request_observation_finalized | Data pipeline | Đủ cửa sổ quan sát và kiểm tra completeness | event_id, trace_id, request_id, event_timestamp, arm, received_at, closed_at_if_any, followup_complete_at, coverage_complete, source_watermark, missing_reason, snapshot_version | Ticket stream + ingestion watermark | KPI-01, KPI-03 |

### Traceability và quy tắc tính

- Intake tạo request_correlation_id và trace_id cho cả treatment/control dù control không gọi agent. Dùng request_id nối xuyên mọi execution; trace_id phân biệt execution, run_id/attempt phân biệt retry. Không phát sinh event agent giả cho control; control access thực nếu có là contamination phải báo.
- Dedup delivery bằng event_id; business event dùng action_id/suggestion_id/transaction_id + version. Retry ghi sổ không đồng nghĩa nhiều lần hoàn: đối soát commit/read-back và idempotency_key. Số request audit/reopen/usage luôn dedup request_id; suggestion-level SR-03 dedup suggestion_id, dùng decision_version cuối trước cutoff.
- Cohort theo received_at; giữ các timestamp sự kiện gốc, log sửa đổi version. 24 giờ = closed_at − received_at; 7 ngày = reopened_at − closed_at của lần đóng đầu tiên. Request cuối có thể cần tối đa 1 ngày đóng +7 ngày follow-up, phù hợp CP4. Không suy ra không mở lại chỉ từ việc không thấy event: cần coverage_complete và source_watermark đã qua cửa sổ, audit log độ trễ/mất dữ liệu.
- Review/rework minutes đo từ work session start/end, trừ idle theo rule khóa trước; cộng mọi session hợp lệ, không dùng phút `_simulated` làm số đo pilot. Khóa cost cohort, rate card và xử lý phiên bản; tránh đếm trùng fallback với rework. Thiếu thời gian đo thật thì chi phí chưa đủ điều kiện kết luận.

### KPI-to-Event Mapping

| KPI | Required Events | Required Fields | Calculation Feasible? | Missing Instrumentation |
| --- | --- | --- | --- | --- |
| KPI-01 | refund_request_created, ticket_closed, ticket_reopened, request_observation_finalized | request_id, trace_id, assigned_staff_id, arm, eligible, received_at, closed_at, reopened_at, followup_complete_at, coverage_complete, source_watermark | Lab: tính được từ flags; pilot: đủ thiết kế nếu event đầy đủ | Timestamp thật, roster/arm, completion/watermark chưa có trong CSV |
| KPI-02 | agent_suggestion_shown, agent_suggestion_viewed, staff_review_decision | request_id, trace_id, suggestion_id, shown_at, viewed_at, decision, decision_version, review_completed_at | Lab: requests reviewed; pilot: đủ thiết kế theo gợi ý chuẩn | suggestion_id/funnel chưa instrument; SR-03 cần suggestion denominator riêng |
| KPI-03 | refund_request_created, ticket_closed, ticket_reopened, request_observation_finalized | request_id, trace_id, arm, closed_at, reopened_at, followup_complete_at, coverage_complete, source_watermark | Lab: từ flags; pilot: cần cohort trưởng thành | Chưa có timestamp và bằng chứng coverage thật |
| KPI-04 | refund_request_created, agent_ui_opened, agent_suggestion_viewed, agent_action_used | request_id, trace_id, staff_id, arm, eligible, action, initiated_by, event_timestamp | Proposed; chưa đo được từ CSV | Thiếu action audit; phân biệt UI open/view/use trước thu thập |
| KPI-05 | refund_request_created, refund_ledger_write, audit_sample_checked, refund_customer_notification | request_id, trace_id, arm, transaction_id, sampling_frame, valid_audit, verified_incorrect, policy_version, pricing_version, actual_refund_amount, expected_refund_amount, severity | Proposed; chưa đo được từ CSV/20 tình huống | Thiếu audit ngẫu nhiên, ledger join, policy/pricing version và notification outbox |

## E2 · Rủi ro kinh tế

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| RISK-01 · Chi phí rework tăng | CP2 rework ×2 làm CPS tăng **51,765%**, lên **6.786,897 VND/success** (simulated) | Rework rate >7%/tuần với ít nhất 200 eligible requests trưởng thành; theo dõi duration và cost | Rà 20 trace rework hoặc toàn bộ nếu ít hơn; phân loại nguyên nhân; giữ mở rộng và xem xét thu hẹp scope/retry sau phê duyệt | PM trợ lý hoàn phí |
| RISK-02 · Human review bắt buộc làm mất lợi thế chi phí | Review100%, rework9 phút: **11.742,793 VND/success**; rework15,3 phút: **12.414,793**, vượt baseline12.000; break-even review **4,803 phút** (simulated) | Review coverage >50%, mean review >4,8 phút và tối thiểu100 requests reviewed | Giữ review ở giao dịch rủi ro; chỉ giảm theo bậc sau phê duyệt dựa trên audit và safety | Trưởng nhóm CSKH |
| RISK-03 · Volume thấp pha loãng fixed cost | Fixed40 triệu/tháng; half volume làm fixed/success **1.185,185→2.370,370**, total CPS **4.599,089→5.784,274** (simulated) | Eligible volume, success trưởng thành, coverage days và allocation fixed theo scope | Không mở rộng khi thiếu volume; rà chi phí fixed; báo riêng variable CPS/system cost; gia hạn thu mẫu theo CP4 | Finance Lead |
| RISK-04 · Thiếu staff/coverage gây thiếu mẫu | Cần11.960 eligible requests và40 staff; 28 ngày ×80% capture ước tính13.748, còn20 ngày ước tính9.820, thiếu2.140 | Enrollment từng staff/arm, coverage và roster; kiểm tra capacity ít nhất299 requests/staff | Không bắt đầu nếu thiếu roster; giữ phân bổ20+20, gia hạn theo block7 ngày trong giới hạn CP4; thiếu mẫu thì Inconclusive, không mở rộng | Operations Manager |

### Economic Risk Register (chi tiết ngưỡng và trạng thái)

Các ngưỡng dưới đây là **Planned**, cần phê duyệt; cảnh báo quản trị bổ sung không sửa SR-01–SR-03 của CP4. Mọi tác động chi phí là **simulated**, không phải kết quả pilot hoặc dự báo chắc chắn. Theo dõi theo arm/type/staff và báo mẫu số, dữ liệu thiếu; ít mẫu thì giữ rollout thay vì kết luận an toàn/kinh tế đạt.

| Risk ID | Risk Description | Quantified Impact | Early Warning Indicator | Trigger/Threshold | Monitoring Window | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-01 | Chi phí rework tăng | CP2 B1 rework ×2: CPS +51,765%, lên 6.786,897 VND/success (simulated) | Rework requests/eligible, mean duration, rework cost theo type; lab scope 48/982 = 4,8880% | Rework rate >7% với >=200 eligible trưởng thành; ngưỡng cao hơn baseline lab, không phải kiểm định efficacy | Tuần không chồng lấn; cohort đủ follow-up | PM rà 20 trace rework hoặc toàn bộ nếu ít hơn trong 3 ngày, phân loại root cause; giữ mở rộng. Thu hẹp noi_dia/retry <=2 chỉ sau duyệt, version lại nếu đổi can thiệp; theo system/request, không chỉ Agent CPS | PM trợ lý hoàn phí | Planned |
| RISK-02 | Human review bắt buộc làm mất lợi thế chi phí | B4 review100% requests có run ok: 948 lượt; rework9 phút CPS 11.742,793; rework15,3 phút CPS 12.414,793 >12.000; break-even review 4,803 phút (simulated) | Reviewed requests/eligible, mean review/rework minutes đo thật, sửa/bỏ và audit errors | Review coverage >50% và mean review >4,8 phút, >=100 requests reviewed; giữ đồng thời SR-02 CPS8000 | Tuần trưởng thành, kiểm tra lại cuối ramp25% | Giữ human review ở giao dịch rủi ro; đánh giá quy trình/UX và năng lực CSKH. Chỉ giảm theo bậc khi có phê duyệt dựa trên audit và safety; không tự bỏ kiểm soát để giảm CPS | Trưởng nhóm CSKH | Planned |
| RISK-03 | Volume thấp pha loãng fixed cost | A4 fixed40 triệu/tháng; volume45000→22500: fixed/success 1.185,185→2.370,370; total CPS 4.599,089→5.784,274 (simulated) | Eligible volume, success trưởng thành, coverage days, allocation fixed theo scope | Success tuần <50% kế hoạch volume đã khóa, kế hoạch phải >0; thiếu mẫu chi phí thì không kết luận | Tuần trưởng thành; forecast tháng, không áp thẳng volume toàn mạng lên pilot6 depot | Không mở rộng, rà hợp đồng fixed/volume; báo variable CPS và system cost riêng, gia hạn thu mẫu theo CP4. Không đổi MDE hoặc bỏ outcome xấu sau khi xem kết quả | Finance Lead | Planned |
| RISK-04 | Thiếu staff/coverage gây thiếu mẫu và kéo dài chi phí | Mục tiêu11960; giả định6 depot, capture80%: 28 ngày coverage13748; chỉ20 ngày9820, thiếu2140. Cần40 staff,299/người; không phải số quan sát | Enrollment từng staff/arm, coverage thực, roster và CV cụm | <40 staff trước randomization hoặc staff<299/arm<5980/tổng<11960 sau28 ngày | Trước ramp; đếm enrollment hằng ngày, quyết định gia hạn theo block7 ngày | Không bắt đầu nếu roster chưa đạt; giữ20+20 và cả hai arm đồng thời, gia hạn tối đa42 ngày dựa enrollment đã làm mù efficacy; hết hạn thiếu mẫu thì Inconclusive/không mở rộng. Bảo đảm coverage6 depot ngoài pilot | Operations Manager | Planned — giả định khả thi |

A4 dùng cơ cấu thành công trong scope so toàn mẫu: `45000 × 900/1200 = 33750 success`; fixed `40000000/33750 = 1185,185`. Half volume cho 16875 success và fixed 2370,370. Đây là kịch bản giữ nguyên mix/hiệu suất, không phải volume pilot thật. B3 có fallback12000/unresolved có thể chồng rework, chưa gồm fixed; không xem CPS/success và system cost/request là cùng mẫu số.

## Gate 2a · Điều kiện và bằng chứng cần nộp

**Khuyến nghị: Go có điều kiện**, chỉ xét hướng thiết kế pilot noi_dia + hang_nang. Hiện mọi điều kiện dưới đây là **Chưa**, không cho phép kích hoạt agent. Các ngày là mốc kiểm tra **dự kiến**, chưa được doanh nghiệp chấp thuận. Áp dụng cho lần tiếp xúc đầu tiên ramp10% dự kiến 30/11/2026, không chỉ kỳ main 11/01/2027.

| Gate ID | Condition | Evidence Required | Accountable Owner | Check Date | Status |
| --- | --- | --- | --- | --- | --- |
| GATE-01 | Transaction safety trước mọi ghi hoàn tự động | Fault injection 503/pending, idempotency retry và duplicate request test PASS; ledger commit/read-back trước notification; đối soát pending/failed, số tiền và phiên bản giá cho ca05/07/15/17/20 | AI Engineering Lead | 2026-11-27 | Chưa |
| GATE-02 | Duyệt thiết kế và preregistration | Chấp thuận MDE6pp, power khi true effect +5pp≈0,642; 20+20 staff; analysis ITT/cluster-aware, missing/crossover, seed, eligibility và ngưỡng được khóa/version trước deadline29/11 | Giám đốc vận hành LogiX-VN | 2026-11-26 | Chưa |
| GATE-03 | Đủ staff và volume có coverage | Roster thật40 staff/6 depot,20 mỗi arm, coverage depot ngoài pilot; capacity từng người>=299 eligible, source volume/capture, lịch làm và kế hoạch gia hạn có bằng chứng | Operations Manager | 2026-11-26 | Chưa |
| GATE-04 | Instrumentation đo KPI và chi phí | Integration test15 event, trace cho cả control, timestamp/watermark, dedup, roster/arm, review/rework đo thật, ledger/audit join và data completeness/latency PASS | Data Engineering Lead | 2026-11-27 | Chưa |
| GATE-05 | Stop rules và rollback sẵn sàng | Phê duyệt SR01–03, danh sách người có quyền dừng; diễn tập kill switch/fallback/pending reconciliation, xác minh mục tiêu<=30 phút và audit log | Giám đốc vận hành LogiX-VN | 2026-11-27 | Chưa |
| GATE-06 | Chính sách human review và kinh tế | Review theo risk được duyệt; bảo vệ kiểm soát tiền; worklog/đơn giá thật, response plan CPS>8000, xử lý fixed/fallback không trùng rework; không bỏ review bắt buộc vì chi phí | Trưởng nhóm CSKH | 2026-11-27 | Chưa |
| GATE-07 | Hoàn thiện bằng chứng CP3 độc lập | Hai phiếu reviewer gốc trước khi so bảng hoặc hướng dẫn miễn/thay thế bằng văn bản thực của giảng viên; không dùng self-review làm hai reviewer | Operations Manager | 2026-11-27 | Chưa |

**Mốc kiểm tra chung:** hội đồng/người có thẩm quyền xem bằng chứng trước 29/11/2026; main readiness kiểm tra lại ngày 08/01/2027 trước main11/01. Nếu điều kiện/ramp/follow-up chưa kịp, hoãn bắt đầu và dịch toàn bộ lịch theo `pilot_plan.yaml`; không giả định đã kịp. Không hoàn tất an toàn hoặc roster không khả thi trước hạn thì **No-go cho lịch đề xuất**, phải thiết kế lại rồi trình duyệt. Không đổi CP4 trong lượt viết hồ sơ này.

**Logic quyết định:** Go chỉ khi mọi điều kiện thiết yếu và quyền phê duyệt được xác nhận; Go có điều kiện chỉ thông qua hướng/kế hoạch, chưa cho kích hoạt; No-go nếu không thể đáp ứng an toàn hoặc khả thi. Không dùng unit tests tài liệu làm bằng chứng giao dịch thật đã được kiểm chứng.

**Duyệt chéo:** `phieu_cham.md` giữ nguyên; chưa có kết quả hội đồng hoặc hướng dẫn miễn/thay thế trong RULES/CHECKPOINTS/RUBRIC/SUBMISSION/TEAM và bằng chứng hiện có. Trạng thái **PENDING EXTERNAL REVIEW**. Tự QA C6: đã nêu B4>12000 và power0,642; C7: số giả lập và scope ghi rõ; C8: đủ thiết kế cỡ mẫu/đối chứng/luật dừng nhưng roster, instrumentation, safety approval và rollback còn thiếu. Đây không phải điểm chính thức hoặc quyết định hội đồng.

## Checklist nội dung và QA

- E1: ba KPI tính lại từ CSV, hai KPI đề xuất chưa đo, đủ15 event và mapping5 KPI.
- E2: ba rủi ro kinh tế và một rủi ro khả thi có số, ngưỡng, cửa sổ, mitigation và một owner.
- E3: [hồ sơ một trang](ho_so_launch_v0.md) đúng7 mục, nhãn trạng thái theo đề, khuyến nghị có điều kiện.
- QA tự động: `cd src; python -m unittest discover -s . -p "test_*.py" -v`; tests CP5 đối chiếu phép tính, cấu trúc bảng, event properties, mapping và ngày CP4. Syntax/YAML/diff kiểm tra riêng; kết quả thực thi ghi trong báo cáo cá nhân.
- Không tự điền điểm hội đồng, không tạo event logs/pilot outcome/approval; không commit/push.
