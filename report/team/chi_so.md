# Đặc tả chỉ số, event và rủi ro kinh tế · CP5 E1–E2

Nguyễn Thị Thùy Dung · 2A202603552 · L3A · Individual Lab. **CP5 CONTENT COMPLETE** về tài liệu/phép tính; 


## E1 · Đặc tả KPI

### Nguồn và phép tính mô tả

| Calculation | Numerator | Denominator | Result | Source |
| --- | --- | --- | --- | --- |
| KPI-01 | 994 | 1200 | 82,8333% | `sum((dong_trong_24h == 1) & (mo_lai_trong_7_ngay == 0)) / len(reqs)` |
| KPI-02 | 48 | 177 | 27,1186% | Lọc `duoc_xem_lai == 1`; `sum(quyet_dinh_xem_lai in [sua, bo]) / len(reviewed)` |
| KPI-03 overall | 51 | 1200 | 4,2500% | `sum(mo_lai_trong_7_ngay == 1) / len(reqs)` |
| KPI-03 pilot scope | 39 | 982 | 3,9715% | Lọc `loai in [noi_dia, hang_nang]`, cùng công thức mở lại |
| Rework baseline pilot | 48 | 982 | 4,8880% | Lọc scope; `sum(ket_qua == lam_lai) / len(eligible)` |

## Event Tracking Specification


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

## E2 · Economic Risk Register

| Risk ID | Risk Description | Quantified Impact | Early Warning Indicator | Trigger/Threshold | Monitoring Window | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-01 | Chi phí rework tăng | CP2 B1 rework ×2: CPS +51,765%, lên 6.786,897 VND/success (simulated) | Rework requests/eligible, mean duration, rework cost theo type; lab scope 48/982 = 4,8880% | Rework rate >7% với >=200 eligible trưởng thành; ngưỡng cao hơn baseline lab, không phải kiểm định efficacy | Tuần không chồng lấn; cohort đủ follow-up | PM rà 20 trace rework hoặc toàn bộ nếu ít hơn trong 3 ngày, phân loại root cause; giữ mở rộng. Thu hẹp noi_dia/retry <=2 chỉ sau duyệt, version lại nếu đổi can thiệp; theo system/request, không chỉ Agent CPS | PM trợ lý hoàn phí | Planned |
| RISK-02 | Human review bắt buộc làm mất lợi thế chi phí | B4 review100% requests có run ok: 948 lượt; rework9 phút CPS 11.742,793; rework15,3 phút CPS 12.414,793 >12.000; break-even review 4,803 phút (simulated) | Reviewed requests/eligible, mean review/rework minutes đo thật, sửa/bỏ và audit errors | Review coverage >50% và mean review >4,8 phút, >=100 requests reviewed; giữ đồng thời SR-02 CPS8000 | Tuần trưởng thành, kiểm tra lại cuối ramp25% | Giữ human review ở giao dịch rủi ro; đánh giá quy trình/UX và năng lực CSKH. Chỉ giảm theo bậc khi có phê duyệt dựa trên audit và safety; không tự bỏ kiểm soát để giảm CPS | Trưởng nhóm CSKH | Planned |
| RISK-03 | Volume thấp pha loãng fixed cost | A4 fixed40 triệu/tháng; volume45000→22500: fixed/success 1.185,185→2.370,370; total CPS 4.599,089→5.784,274 (simulated) | Eligible volume, success trưởng thành, coverage days, allocation fixed theo scope | Success tuần <50% kế hoạch volume đã khóa, kế hoạch phải >0; thiếu mẫu chi phí thì không kết luận | Tuần trưởng thành; forecast tháng, không áp thẳng volume toàn mạng lên pilot6 depot | Không mở rộng, rà hợp đồng fixed/volume; báo variable CPS và system cost riêng, gia hạn thu mẫu theo CP4. Không đổi MDE hoặc bỏ outcome xấu sau khi xem kết quả | Finance Lead | Planned |
| RISK-04 | Thiếu staff/coverage gây thiếu mẫu và kéo dài chi phí | Mục tiêu11960; giả định6 depot, capture80%: 28 ngày coverage13748; chỉ20 ngày9820, thiếu2140. Cần40 staff,299/người; không phải số quan sát | Enrollment từng staff/arm, coverage thực, roster và CV cụm | <40 staff trước randomization hoặc staff<299/arm<5980/tổng<11960 sau28 ngày | Trước ramp; đếm enrollment hằng ngày, quyết định gia hạn theo block7 ngày | Không bắt đầu nếu roster chưa đạt; giữ20+20 và cả hai arm đồng thời, gia hạn tối đa42 ngày dựa enrollment đã làm mù efficacy; hết hạn thiếu mẫu thì Inconclusive/không mở rộng. Bảo đảm coverage6 depot ngoài pilot | Operations Manager | Planned — giả định khả thi |
