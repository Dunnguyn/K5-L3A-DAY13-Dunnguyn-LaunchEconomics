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

## 5. Xác nhận nhãn cuối và phân xử

Người học đã tự rà soát và xác nhận 20/20 Final Labels; giữ nguyên nhãn và Root Cause. Ngày xác nhận: 22/11/2026. Trạng thái bộ nhãn hiện tại: **CONFIRMED — 20/20**.

Tôi đối chiếu đủ 20 nhãn đề xuất trong bảng nguồn với bộ Final Labels hiện tại: **20/20 trùng**, không cần đổi nhãn. Đối chiếu với hướng dẫn Nhiệm vụ C tiếp tục cho kết quả **20/20 = 100%**.

| Case ID | Hai nhãn reviewer | Phân tích và nhãn phân xử đề xuất | Đối chiếu nhãn cuối |
| --- | --- | --- | --- |
| 13 | L / C | Yêu cầu bảo hiểm đối tác nằm ngoài phạm vi chức năng; phản hồi chung chung là yếu tố giao tiếp phụ. Chọn L — System Limitation. | Trùng L đã CONFIRMED |
| 17 | H / S | Cache dùng bảng giá cũ gây sai lệch ở 212 đơn trong 9 ngày mà không ai mở lại; taxonomy bài lab ưu tiên tính âm thầm kéo dài. Chọn H — Hidden Error; không bổ sung cơ chế phát hiện mà đề chưa nêu. | Trùng H đã CONFIRMED |

Phân tích chi tiết và quy tắc ranh giới nằm tại mục 5 của [báo cáo lỗi](bang_loi.md). Nhãn cuối đã được tôi xác nhận từ trước và không thay đổi. Tôi không suy diễn xác nhận nhãn cuối thành việc hai reviewer đã cùng chấp thuận phân xử hoặc đã phân loại độc lập.

## 6. Regression và bảo toàn dữ liệu

Ngày 22/11/2026, tôi chạy `src/.venv/Scripts/python.exe -m unittest -v test_cp1 test_cp2` từ thư mục `src`. Lượt đầu có 29/30 PASS do câu mở đầu báo cáo CP1 đã bị sửa ở lượt trước. Tôi khôi phục đúng câu gốc trong `bang_chi_phi.md` theo `HEAD` để đáp ứng kiểm tra bảo toàn; lượt chạy lại đạt **30 tests, 30 PASS, 0 FAIL**. Tôi không sửa code, tests hoặc CSV. `git diff --check` không báo lỗi.

Tôi giữ nguyên năm remediation, nhãn và nội dung self-review. Các phiếu nhãn lịch sử được tham chiếu theo commit `ed89502`, không gọi là file đang chờ xóa chưa commit. Kết quả30 tests ở mục này là mốc CP1–CP2 trước khi bổ sung CP4/CP5; tổng kiểm thử hiện tại là70. Không tự commit/push. Regression không phải chứng cứ reviewer độc lập hoặc hiệu quả remediation.

## 7. Checklist nghiệm thu CP3

| Điều kiện | Trạng thái và bằng chứng |
| --- | --- |
| Taxonomy và 20 ca có Root Cause/evidence | DONE; giữ nguyên |
| Bằng chứng hai reviewer phân loại độc lập | PENDING — có bảng tổng hợp, chưa có bằng chứng phân loại riêng trước khi xem bảng |
| Tỷ lệ trùng nhãn trong bảng ≥80% | DONE — tái tính đủ 20 cặp: 18 trùng, 2 lệch, 90%; tính độc lập xét riêng |
| Xác định và phân tích hai ca bất đồng | DONE — Case 13 L/C → L; Case 17 H/S → H, trùng Final Labels đã xác nhận |
| Người học xác nhận Final Labels | CONFIRMED — 20/20, ngày 22/11/2026 |
| Final Labels khớp reference ≥16/20 | DONE — tính lại 20/20 = 100% |
| 5 remediation đủ loại, ngưỡng, chu kỳ, owner | DONE — giữ nguyên; Proposed/Planned |
| Regression CP1–CP2 và diff check | DONE — 30/30 PASS; không có lỗi diff |

**CP3: PARTIAL.** Tôi đã tính lại 90% từ bảng tổng hợp, phân tích hai ca bất đồng và đối chiếu khớp bộ nhãn cuối CONFIRMED. Điều kiện còn thiếu là hai phiếu nhãn gốc hoặc bằng chứng hai reviewer tự phân loại riêng trước khi xem bảng. CP4 đã Design & QA Complete, CP5 đã Content Complete; nghiệm thu quy trình CP3 và Gate 2a vẫn PENDING.

## 8. Cập nhật CP4 và công cụ hỗ trợ

Ngày 22/11/2026, tôi hoàn thiện thiết kế CP4 trong `src/lab13.py`, `src/test_cp4.py` và `pilot_plan.yaml`. Đây là kế hoạch Planned để trình Gate 2a; chưa thực hiện phân nhóm hoặc pilot. Đây là mốc cập nhật CP4; trạng thái hiện tại được tổng hợp tại mục3 và10. CP3 vẫn chờ bằng chứng độc lập; CP5 được cập nhật tại mục9.

Tôi sử dụng ChatGPT/Codex để hỗ trợ lập trình, rà soát phép tính và soạn kế hoạch CP4 theo `RULES.md`. Cách kiểm chứng: đối chiếu công thức bằng SciPy, kiểm tra bất biến và tính tối thiểu của cỡ mẫu, đếm lại CSV bằng `csv.DictReader`, parse và duyệt cây YAML, chạy 25 tests CP4 cùng 30 regression tests CP1–CP2 sau rà soát tính khả thi, kiểm tra cú pháp và `git diff --check`. Không gọi model/API trong chương trình, không dùng kết quả thiết kế làm bằng chứng hiệu quả thực nghiệm.

### Rà soát tính khả thi trước CP5

Tôi giữ nguyên toàn bộ D1: MDE 6pp cần 859 effective/arm, 20 staff/arm, tối thiểu 299 requests/người, DE 6,96 và tổng 11.960 raw requests. Power khi tác động thật chỉ +5pp vẫn khoảng 0,642; gia hạn để đạt mẫu không thay đổi giới hạn này.

Lịch cũ 28/12/2026–10/01/2027 có 14 ngày. Với giả định chia đều 1.500 requests/ngày trên 12 depot, 6 depot có 750 requests/ngày; áp tỷ trọng eligible 982/1.200 cho khoảng 613,75 eligible/ngày. Trong 14 ngày chỉ có 8.592,5 requests kỳ vọng, thiếu 3.367,5; chia đều 40 staff là 214,8125/người, chưa đạt 299. Đây là phép ước tính từ bối cảnh và trace lab giả lập, không phải số đo thực tế. Con số 1.227,5 eligible/ngày trong kế hoạch trước thuộc toàn bộ 12 depot, không được dùng thay lưu lượng 6 depot.

Nếu staff cũng chia đều 40 người trên 12 depot, 6 depot chỉ khoảng 20 người. Tôi chưa có bằng chứng bố trí đủ 40 staff tại 6 depot; cần xác minh roster/năng lực hoặc điều chuyển thêm khoảng 20 người trước phân nhóm. Vì 40 là toàn bộ nguồn lực giả định của mạng, phương án điều chuyển phải bảo đảm coverage của 6 depot ngoài pilot; tôi không mặc định có thêm người hoặc đã được doanh nghiệp chấp thuận. Chỉ có 20 staff tổng thì 10/arm có trần effective 500 <859, không thể khắc phục bằng kéo dài thời gian. Mở phạm vi sang 12 depot chỉ là phương án khác cần xét và duyệt trước preregistration, không tự thay phạm vi khi đang chạy.

Tôi đổi kỳ chính dự kiến sang 11/01–07/02/2027 (28 ngày), có điều kiện: 40 staff tại 6 depot và đủ coverage. Theo phép chia đều, 28 ngày có 17.185 eligible kỳ vọng; kịch bản capture 80% còn 13.748, bình quân 343,7/người. Capture 80% là giả định hao hụt do exclusion bổ sung, routing và coverage, chưa được đo. Tối thiểu cần 20 ngày có lưu lượng ở capture 100%, hoặc 25 ngày ở capture 80%; nếu 28 ngày lịch chỉ có 20 ngày coverage thì kịch bản 80% chỉ thu 9.820, vẫn thiếu. Tổng đủ cũng không bảo đảm từng staff hoặc từng arm đủ, nhất là khi workload không đều.

Hai bước ramp dự kiến thu một tuần mỗi bước, sau đó chờ tối đa 1 ngày đóng và đủ 7 ngày follow-up, rồi qua gate: ramp 10% từ 30/11–06/12, gate không trước 15/12; ramp 25% từ 21–27/12, gate không trước 05/01. Main bắt đầu 11/01 nếu gate đạt; không gộp dữ liệu ramp vào mẫu efficacy chính. Economic rule dùng hai cohort tuần lịch liên tiếp, không chồng lấn, cùng phiên bản/scope và mỗi tuần đủ 100 success trưởng thành. Hai tuần cuối main có thể đánh giá đầy đủ ngày 16/02; sự cố giao dịch nghiêm trọng vẫn dừng ngay.

Nếu kết thúc thu mẫu ngày 07/02, request cuối có thể đóng ngày 08/02 và cần theo dõi đến hết 15/02; QA 16–17/02, quyết định sớm nhất 18/02/2027. Toàn bộ lịch là đề xuất chưa được LogiX chấp thuận. Khi chưa đủ mẫu, gia hạn đồng thời hai arm theo block 7 ngày, tối đa 42 ngày main; chỉ dùng số enrollment/coverage đã làm mù efficacy để quyết định gia hạn, không dùng p-value hoặc effect. Giữ nguyên arm, roster và eligibility; thu mọi eligible tới hết block, không bỏ request từ staff thu nhanh.

Nếu main bắt đầu đúng 11/01 và gia hạn hết 42 ngày thì kết thúc 21/02, follow-up đến 01/03, QA 02–03/03 và quyết định sớm nhất 04/03. Thiếu mẫu sau giới hạn, thiếu cụm, thiếu hai tuần kinh tế đủ mẫu hoặc dữ liệu chưa đạt QA thì Inconclusive/không mở rộng. Ramp/main bị lùi phải dịch toàn bộ lịch theo ngày thực và lưu audit. Các giới hạn khác còn lại gồm staff chưa xác minh, tải không đều, ICC/CV kích thước cụm, contamination, ngày nghỉ và ngưỡng adoption có thể làm rollout kéo dài.

## 9. Cập nhật CP5 — KPI, rủi ro và hồ sơ Launch v0

Ngày 22/11/2026, tôi hoàn thiện `chi_so.md`, `ho_so_launch_v0.md` và tạo `src/test_cp5.py`. Các ghi nhận CP5 chưa hoàn thành ở phần trước là lịch sử trước lượt cập nhật này; nội dung CP1–CP4 được giữ nguyên. Tôi tiếp tục dùng các công cụ hỗ trợ đã khai báo ở mục 8; kiểm chứng bằng tính lại CSV, gọi các hàm mô hình hiện có, kiểm thử tự động và kiểm tra tài liệu, không tạo dữ liệu pilot.

E1: primary 994/1.200 = 82,83%; sửa/bỏ 48/177 = 27,12%; reopen 51/1.200 = 4,25%, riêng scope 39/982 = 3,9715%. Đây là mô tả trace lab giả lập, không phải causal lift từ baseline thiết kế 70%. Adoption và Verified Incorrect Refund Rate là Proposed — Not Yet Measured. Tôi đặc tả 15 event có trace_id, timestamp và khóa nối/dedup, mapping đủ 5 KPI, phân biệt request-level với suggestion-level và ghi rõ instrumentation còn thiếu.

E2: có ba rủi ro kinh tế và một rủi ro khả thi. Rework ×2 tăng CPS 51,765%; review100%/rework15,3 phút đưa CPS lên 12.414,793 VND/success; fixed cost pha loãng khi volume giảm nửa. Các tác động kinh tế có phần simulated. Rủi ro staff/coverage giữ đúng CP4: mục tiêu 11.960 requests, 299/staff; 20 ngày coverage ở capture80% chỉ 9.820, thiếu 2.140. Ngưỡng cảnh báo, cadence, hành động và một accountable owner được ghi ở từng rủi ro.

E3: hồ sơ tóm tắt đúng bảy mục, dùng ba trạng thái theo đề, khuyến nghị **Go có điều kiện** chỉ cho kế hoạch noi_dia + hang_nang. Có bảy preconditions với owner, bằng chứng và ngày kiểm tra dự kiến trước ramp30/11/2026; kiểm tra lại main readiness08/01/2027. Mọi gate hiện Chưa; không kịp điều kiện thì hoãn lịch hoặc No-go cho lịch đề xuất. Không coi 70 unit tests là bằng chứng các remediation/ledger/kill switch đã được triển khai và nghiệm thu.

Lịch chính tham chiếu YAML hiện tại: 11/01–07/02/2027, quyết định sớm nhất18/02; gia hạn theo enrollment block7 ngày, tối đa42 ngày, quyết định sớm nhất04/03 nếu dùng hết hạn và bắt đầu đúng lịch. Power cho true effect +5pp vẫn khoảng0,642; 40 staff/6 depot, coverage, roster, event instrumentation, rollback và phê duyệt còn chưa xác minh. Bằng chứng CP3 độc lập vẫn thiếu.

QA thực thi: `python lab13.py` chạy thành công; `python -m unittest discover -s . -p "test_*.py" -v` đạt **70 tests, 70 PASS, 0 FAIL**, gồm 55 tests CP1–CP4 và 15 tests CP5. `python -m py_compile lab13.py test_cp1.py test_cp2.py test_cp4.py test_cp5.py` thành công; YAML validation, kiểm tra cấu trúc bảng Markdown và `git diff --check` không có lỗi. Kiểm thử CP5 xác minh KPI bằng pandas/csv độc lập, đối chiếu chi phí với mô hình, event-to-field mapping, bảy mục hồ sơ và ngày CP4. Lỗi QA ban đầu nhận nhầm dấu hỏi ở header bảng là placeholder đã được sửa để kiểm tra giá trị từng ô; không thay số liệu để vượt test.

**CP5 CONTENT COMPLETE · Gate 2a: PENDING EXTERNAL REVIEW · Pilot: Planned / Not Approved.** Tôi giữ nguyên `phieu_cham.md`, `group_report.md`, `TEAM.md`, reviewer source và toàn bộ CP1–CP4/CSV. Chưa tìm thấy quyết định hội đồng hoặc hướng dẫn miễn/thay thế thực tế, không tự chấm điểm. Không commit/push.

## 10. Rà soát hồ sơ nộp local và các xác nhận còn thiếu

Tôi đã hoàn thiện TEAM.md theo đúng một người thực hiện, khôi phục nguyên mẫu MSSV_HoTen.md từ commit `ed89502`, đồng bộ báo cáo tổng hợp/danh mục và đính chính self-review hiện có. Không thay20 Final Labels, Root Cause, năm remediation, reviewer source, CSV, starter, công thức hoặc kế hoạch CP4. Các bảng KPI/event/rủi ro và dossier CP5 giữ nguyên.

### Khai báo công cụ và phạm vi theo bằng chứng hiện có

| Phạm vi | Nguồn khai báo công cụ | Cách kiểm chứng và giới hạn |
| --- | --- | --- |
| CP1–CP2 | `bang_chi_phi.md` ghi Codex hỗ trợ; báo cáo cá nhân tại commit `ed89502` ghi ChatGPT/Codex hỗ trợ yêu cầu, code và rà soát | Thực thi Python, đối chiếu csv/Decimal, invariant tests; không coi phép tính simulated là kết quả vận hành thật |
| CP3 | Báo cáo cá nhân tại `ed89502` đã khai báo ChatGPT/Codex hỗ trợ phân loại và đối chiếu tham khảo | Giữ nguồn tổng hợp18/20, Final Labels đã xác nhận và một bộ self-review; hỗ trợ/đối chiếu không trở thành hai review độc lập |
| CP4–CP5 | Khai báo ở mục8–9; không thêm tên công cụ chưa có bằng chứng | SciPy/formula, CSV, tests và QA tài liệu; không gọi model/API trong chương trình |

Các ghi nhận trên dựa vào tài liệu hiện có và lịch sử Git, không phải xác nhận mới về ai đã điền self-review hoặc lúc nào. Tôi cần xác nhận nguồn/người/thời điểm review thực tế nếu muốn dùng phiếu làm bằng chứng đánh giá; chưa có thông tin để tự bổ sung công cụ khác hoặc tạo xác nhận độc lập.

### Trạng thái nộp và yêu cầu bên ngoài

- A. Chấp thuận nộp Individual Lab thay quy trình nhóm4 người: PENDING — cần giảng viên xác nhận.
- B. Hai reviewer độc lập CP3 hoặc văn bản miễn/thay thế thực tế: PENDING; không dùng self-review hoặc unit tests thay thế.
- C. Hình thức peer review Gate 2a cho bài cá nhân: PENDING EXTERNAL REVIEW; giữ nguyên phiếu chấm, không tự điền điểm/chữ ký.
- Pilot: Planned / Not Approved; Conditional Go chỉ là khuyến nghị kế hoạch trong dossier.
- LMS submission/deadline, chạy trên máy khác và số trang bản in: NOT VERIFIED; cần bằng chứng thực tế.

QA hiện tại gồm70 tests (14 CP1,16 CP2,25 CP4,15 CP5). Test e12 được đổi từ khóa toàn bộ tài liệu hành chính theo HEAD sang kiểm tra các bất biến nội dung: bảo toàn code/CSV/CP4/reviewer, giữ nguyên các mục chuyên môn CP3, mẫu gốc, đúng một sinh viên, trạng thái checkpoint/test counts và external pending. Kiểm tra âm phải phát hiện metadata sai; không khôi phục tài liệu lỗi thời chỉ để test PASS.

Mẫu khôi phục chưa được Git theo dõi lại vì lượt này không chạy git add. Danh sách cần người thực hiện review/stage gồm TEAM.md, mẫu gốc, báo cáo tổng hợp, README hồ sơ, bang_loi.md, báo cáo cá nhân, CP5 chi_so.md/ho_so_launch_v0.md và test_cp5.py. Không tự commit/push; chưa coi bản local là đã nộp GitHub/LMS.
