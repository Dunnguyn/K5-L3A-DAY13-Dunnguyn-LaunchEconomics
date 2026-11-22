# Bảng chi phí · Nhiệm vụ A và B

Người thực hiện: **Nguyễn Thị Thùy Dung · 2A202603552 · L3A**. Individual Lab: một cá nhân phụ trách A–E; báo cáo này hoàn thành CP1 (A1–A4).

Nguồn tính: `src/lab13.py`, hai CSV gốc; đối chiếu `CHECKPOINTS.md`, `RUBRIC.md`, `docs/du_lieu_va_cong_thuc.md` và phần A của hướng dẫn chi tiết. Công cụ hỗ trợ: Codex; kiểm chứng bằng thực thi Python và unit tests độc lập, không gọi LLM/API trong chương trình.

**Quy ước dữ liệu và đơn vị:** toàn bộ bộ dữ liệu lab là giả lập. “Observed/trace” dưới đây là giá trị ghi trong CSV, không phải đo tại doanh nghiệp thật. Hai cột phút `_simulated` là simulated inputs; giá, lương, baseline và fixed cost là assumptions của đề. CPS, tổng chi phí và tỷ lệ suy ra có phần phút giả lập đều ghi **simulated**. Tiền dùng VND, dấu chấm phân cách nghìn, dấu phẩy thập phân; chỉ làm tròn khi trình bày, giữ số thực khi tính.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Expected | Kết quả thực thi | Trạng thái |
| --- | ---: | ---: | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 | 1,20 lần/yêu cầu | PASS |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 | 1,25 lần/yêu cầu | PASS |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 | 1,25 lần giá một lượt chạy | PASS |

Giả định toán: các lần thử độc lập, xác suất p không đổi, chi phí mỗi lần bằng nhau; E[N] = (1 − (1 − p)^k)/p, P = 1 − (1 − p)^k, M = E[N]/P = 1/p khi p > 0. Không dùng giả định độc lập này để thay thế kết quả trace của A2–A3.

Biên và validation: p hữu hạn trong [0; 1], k nguyên dương hoặc None; p=1 cho E=P=M=1. p=0 cho P=0, E=k hữu hạn hoặc ∞ khi không giới hạn, M=∞ (không có thành công); k=1 cho E=1. Tham số sai báo ValueError, không chia cho 0.

## A2 · Mô hình chi phí từ trace

**Observed data:** requests 1.200 dòng × 13 cột; runs 1.624 dòng × 8 cột. `request_id` duy nhất ở requests, liên kết 1–n với runs; `run_id` và cặp (`request_id`, `attempt`) duy nhất. Đủ attempt 1..`so_lan_chay`, không khóa mồ côi, không thiếu giá trị bắt buộc; requests đọc với `keep_default_na=False` để giữ quyết định xem lại trống.

Kiểu dữ liệu: ID, `loai`, trạng thái và quyết định là chuỗi; tokens, tool_calls, attempt, số lượt chạy, số tiền, phút simulated và các cờ là số nguyên. Runs có 1.052 `ok`, 572 `loi`; requests có 978 `thanh_cong`, 74 `lam_lai`, 148 `chuyen_nhan_vien`.

**Assumptions:** input 26 VND/1.000 token, output 130 VND/1.000 token, tool 15 VND/lượt; lương 2.000 VND/phút, hai hệ số phút bằng 1; A2 giữ toàn bộ trace, không cộng fixed cost.

| Khoản | Giá trị | Nguồn / phép tính | Nhãn |
| --- | ---: | --- | --- |
| Token | 245.585,132 VND | 5.771.712 input × 26/1.000 + 734.774 output × 130/1.000 | observed/trace × giá giả định |
| Tool | 84.000,000 VND | 5.600 lượt × 15 | observed/trace × giá giả định |
| Trong đó, phần của lần chạy thứ 2 và 3 | 93.804,488 VND | token + tool của các run có attempt > 1 | observed/trace; đã nằm trong 2 dòng trên |
| Xem lại | 1.780.000,000 VND | 890 phút `phut_xem_lai_simulated` × 2.000 | simulated |
| Làm lại | 2.264.000,000 VND | 1.132 phút `phut_lam_lai_simulated` × 2.000 | simulated |
| Tổng chi phí | 4.373.585,132 VND | token + tool + xem lại + làm lại | simulated |
| Số việc thành công | 978 việc | đếm `ket_qua == 'thanh_cong'` | observed/requests |
| Chi phí mỗi việc thành công (CPS) | 4.471,968 VND/việc | 4.373.585,132 / 978 | simulated |
| Hoá đơn token và tool chia cho số yêu cầu | 274,654 VND/yêu cầu | (245.585,132 + 84.000) / 1.200 | observed/trace × giá giả định |

- **Chênh lệch với hóa đơn:** CPS / hóa đơn trung bình = 4.471,968 / 274,654 = **16,28 lần (simulated)**; mẫu số của CPS là 978 việc, còn hóa đơn là 1.200 yêu cầu.
- **Khoản lớn nhất:** làm lại chiếm **51,77% (simulated)**, xem lại 40,70% (simulated); tổng thời gian nhân viên chiếm 92,46% (simulated).
- **Vì sao chỉ token là thiếu:** token chỉ chiếm **5,62% (simulated)** tổng chi phí, bỏ sót tool và 4.044.000 VND giờ nhân viên (simulated), đồng thời chia 1.200 thay vì 978 còn làm thấp CPS.

**So sánh cả hệ thống với nhân viên tự làm (assumption, simulated):** coi mọi yêu cầu không thành công cần thêm một lần nhân viên xử lý đủ 12.000 VND; đây là khoản bổ sung sau chi phí đã ghi nhận, chưa được chứng minh bằng trace.

| Metric | Phép tính | Kết quả (simulated) |
| --- | --- | ---: |
| Chưa thành công | 1.200 − 978 = 148 chuyển nhân viên + 74 làm lại | 222 yêu cầu |
| Nhân viên xử lý bổ sung | 222 × 12.000 | 2.664.000 VND |
| Tổng chi phí cả hệ thống | 4.373.585,132 + 2.664.000 | 7.037.585,132 VND |
| Chi phí cả hệ thống / yêu cầu | 7.037.585,132 / 1.200 | 5.864,654 VND/yêu cầu |
| So với toàn bộ tự làm | 5.864,654 / 12.000; baseline tổng = 14.400.000 VND | 0,489×; tiết kiệm 51,13% |

- **Phân biệt metric:** 5.864,654 VND/yêu cầu (simulated) có fallback và mẫu số 1.200; CPS A2 là 4.471,968 VND/việc thành công (simulated) với mẫu số 978, chưa có fallback/fixed cost.
- **Giới hạn giả định:** 74 ca `lam_lai` đã có tiền phút làm lại trong A2; cộng thêm 12.000 VND/ca có thể chồng chi phí nếu số phút đó đã giải quyết xong việc, nên pilot phải đo riêng phần xử lý còn lại.

## A3 · Tách theo loại yêu cầu

Mỗi dòng gọi lại `mo_hinh(runs, reqs[reqs.loai == loai])`; hàm tự lọc runs theo request_id. Tỷ lệ thành công = việc thành công / số yêu cầu của loại; số lần chạy = số runs của loại / số yêu cầu. Cột CPS và so baseline dưới đây đều **simulated**, chưa cộng fixed cost hoặc fallback; tỷ lệ baseline là phép chia CPS / 12.000, chưa phải mức tiết kiệm toàn hệ thống.

| Loại | Số yêu cầu | Số thành công | Tỉ lệ thành công | Lần/yêu cầu | CPS (VND/việc, simulated) | So với 12.000 VND (simulated) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 783 | 95,02% | 1,112 | 2.695,642 | 0,225× |
| hang_nang | 158 | 117 | 74,05% | 1,468 | 8.220,735 | 0,685× |
| quoc_te | 150 | 41 | 27,33% | 2,320 | 22.515,165 | 1,876× |
| doi_tac | 68 | 37 | 54,41% | 1,882 | 10.214,867 | 0,851× |

**Retry observed/trace:** mỗi ô là số run `ok` / số run thực sự đến attempt đó (tỷ lệ %). Các nhóm đến lượt 2–3 đã thất bại trước đó, nên tỷ lệ có điều kiện này không phải một thử nghiệm ngẫu nhiên về tác động retry.

| Loại | Attempt 1: ok/n (%) | Attempt 2: ok/n (%) | Attempt 3: ok/n (%) | Việc thành công cuối cùng có lượt chạy ≤1 → ≤2 → ≤3 |
| --- | ---: | ---: | ---: | ---: |
| noi_dia | 750/824 (91,02%) | 56/74 (75,68%) | 7/18 (38,89%) | 723 → 777 → 783 |
| hang_nang | 112/158 (70,89%) | 18/46 (39,13%) | 5/28 (17,86%) | 99 → 115 → 117 |
| quoc_te | 45/150 (30,00%) | 12/105 (11,43%) | 2/93 (2,15%) | 32 → 41 → 41 |
| doi_tac | 35/68 (51,47%) | 6/33 (18,18%) | 4/27 (14,81%) | 27 → 33 → 37 |

`status='ok'` chỉ phản ánh lần chạy, không bảo đảm việc thành công; ví dụ quốc tế có 59 run ok nhưng chỉ 41 việc thành công. Dãy thành công tích lũy đếm `ket_qua='thanh_cong'` và `so_lan_chay <= k`, tương thích quy ước giới hạn của đề; không khẳng định quan hệ nhân quả.

- **Phù hợp:** ưu tiên noi_dia (95,02%; CPS 2.695,642 VND, simulated); hang_nang có thể pilot có điều kiện (74,05%; 8.220,735 VND, simulated), cần kiểm tra phút nhân viên thực.
- **Không hiệu quả:** loại quoc_te khỏi pilot: 27,33% thành công, CPS 1,876× baseline (simulated); cả hệ thống có fallback cũng 14.874,145 VND/yêu cầu (simulated), vượt 12.000 VND.
- **Retry theo loại:** nội địa thêm 54 rồi 6 việc thành công, hàng nặng thêm 16 rồi 2; quốc tế thêm 9 rồi 0, đối tác thêm 6 rồi 4. Lượt 3 không cải thiện số việc thành công quốc tế trong mẫu.
- **Phạm vi pilot:** giữ 2 loại noi_dia + hang_nang; tạm loại doi_tac vì chỉ 37/68 việc thành công (54,41%) và CPS 0,851× baseline (simulated), biên dự phòng chi phí còn hẹp dù retry có thêm việc.

Kiểm tra cộng nhóm: 824 + 158 + 150 + 68 = **1.200 yêu cầu**; 783 + 117 + 41 + 37 = **978 việc thành công**. Tổng chi phí bốn nhóm lần lượt 2.110.687,298 + 961.825,976 + 923.121,766 + 377.950,092 = **4.373.585,132 VND (simulated)**, khớp A2.

## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

**Observed:** phạm vi có 982/1.200 yêu cầu và 900 việc thành công; thành công có điều kiện trong phạm vi là 900/982 = **91,65%**. **Assumption:** 45.000 là tổng nhu cầu doanh nghiệp/tháng, không phải toàn bộ nhu cầu thuộc phạm vi; giữ cơ cấu loại và tỷ lệ thành công của mẫu.

Xác suất một yêu cầu bất kỳ vừa thuộc phạm vi vừa thành công = (982/1.200) × (900/982) = **900/1.200 = 75,00%**. Vì vậy dự báo việc thành công là volume × 75%, đúng mẫu số hướng dẫn chính thức; không dùng 91,65% trực tiếp nhân 45.000.

**Assumptions (simulated):** fixed = 40.000.000 VND/tháng; chi phí biến đổi trong phạm vi = 3.072.513,274 / 900 = **3.413,904 VND/việc**, giữ nguyên ở hai mức volume; A4 không sửa metric A2, chưa cộng chi phí nhân viên fallback cho phần ngoài phạm vi/chưa thành công.

| Tổng nhu cầu/tháng | Việc thành công ước lượng | Fixed/success (VND) | Variable/success (VND, simulated) | Total/success gồm fixed (VND, simulated) | So với 12.000 VND (simulated) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 45.000 yêu cầu | 33.750 | 1.185,185 | 3.413,904 | 4.599,089 | 0,383× |
| 22.500 yêu cầu | 16.875 | 2.370,370 | 3.413,904 | 5.784,274 | 0,482× |

Phép tính: fixed/success = 40.000.000 / việc thành công ước lượng; total/success = variable/success + fixed/success; tỷ lệ baseline = total/success / 12.000.

- **Hiệu quả kinh tế:** trong giả định trên, CPS gồm fixed vẫn dưới 12.000 VND ở cả hai volume: 4.599,089 và 5.784,274 VND (simulated); đây chưa phải kết luận tiết kiệm toàn doanh nghiệp có fallback.
- **Giảm khối lượng:** volume giảm 50% làm fixed/success tăng đúng 2 lần; CPS tăng 1.185,185 VND, tương đương **25,77% (simulated)**, không tăng gấp đôi vì phần biến đổi giữ nguyên.
- **Cần kiểm tra trong pilot:** xác minh 75,00% thành công trên toàn nhu cầu và 91,65% trong phạm vi, cơ cấu 982/1.200, phút simulated bằng đo thật, fixed 40 triệu/tháng và khả năng giữ CPS biến đổi 3.413,904 VND (simulated).

## Bằng chứng kiểm chứng CP1

Chạy tại `src/` trên môi trường `.venv` hiện có (Python mặc định ngoài venv thiếu pandas):

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
$env:PYTHONIOENCODING = 'utf-8'
python lab13.py
python -m unittest -v test_cp1
python -m py_compile lab13.py test_cp1.py
```

Kết quả thực thi: `Ba phép thử đáp án biết trước: ĐẠT`; A1 = 1.2, 1.25, 1.25; script chạy hết A4 không exception. Unit tests: **14 tests, OK**; biên k=1 đã được sửa để trả chính xác 1, không còn sai số 0,9999999999999999.

| Test ID | Mục tiêu | Expected | Actual | PASS/FAIL |
| --- | --- | --- | --- | --- |
| QA-01 | Toán và validation | 3 known answers, biên p=0/1/k=1, tham số sai rõ ràng | 1,20; 1,25; 1,25; biên và ValueError đúng | PASS |
| QA-02 | Toàn vẹn dữ liệu | 1.200 requests, 1.624 runs; 0 trùng/mồ côi; CSV/starter giữ nguyên | Đúng số dòng, khóa, kiểu và nội dung so với Git HEAD | PASS |
| QA-03 | Đối chiếu độc lập csv + Decimal | Token, tool, phút, tổng và CPS khớp | 5.771.712 input; 734.774 output; 5.600 tool; 890/1.132 phút simulated; tổng 4.373.585,132 VND (simulated) | PASS |
| QA-04 | Cộng 4 phân nhóm | 1.200 requests; 978 success; tổng bằng A2 | 1.200; 978; 4.373.585,132 VND (simulated) | PASS |
| QA-05 | Fixed chỉ A4, đúng mẫu số | Success 33.750/16.875; fixed/success ×2 | 1.185,185 → 2.370,370 VND | PASS |
| QA-06 | Execution, syntax, regression | Chạy hết; giới hạn 1/2/3 đúng quy ước; input không đổi | 14 tests OK; không lỗi runtime/syntax; không NaN bất ngờ | PASS |

Đối chiếu hướng dẫn: A2 tất cả 9 dòng sai lệch <0,02% so với số làm tròn của giảng viên; A3 CPS cả 4 loại và A4 cả 2 mức volume sai lệch <0,02%, thấp hơn ngưỡng 2%. Không hardcode số hướng dẫn vào hàm tính; các số đối chiếu chỉ là expected trong tests.

QA findings: không có lỗi dữ liệu gốc; xử lý p=0/CPS không thành công bằng ∞ có chủ đích, tập requests rỗng có hóa đơn/yêu cầu bằng 0; từ chối dữ liệu thiếu/trùng/âm và giá không hợp lệ. Khác biệt `status ok`/thành công cuối, mẫu số A4 và nguy cơ chồng chi phí fallback cho 74 ca làm lại đã được ghi rõ; không còn lỗi triển khai CP1 chưa xử lý.

**CP1 COMPLETE:** A1 DONE · A2 DONE (9 dòng) · A3 DONE (4 loại) · A4 DONE (2 volume) · Code execution DONE · Unit tests DONE · Report phần A DONE. `mo_hinh()` sẵn sàng CP2 với tham số giá/hệ số và giới hạn lượt chạy; cần trace đầy đủ 1..so_lan_chay trước khi gọi, không tự suy diễn kết quả phản thực hay fallback. CP2–CP5 chưa triển khai; B1–B4 bên dưới giữ nguyên template.


## B1 · One-factor Sensitivity — Đổi từng yếu tố

CP2 tiếp nối CP1; trạng thái “CP2–CP5 chưa triển khai” ở phần kiểm chứng CP1 phía trên là ghi nhận lịch sử, được giữ nguyên theo yêu cầu bảo toàn phần A. Phần B này hoàn thành riêng CP2, không triển khai CP3–CP5.

**Nguồn và assumptions:** cùng 1.200 requests, 1.624 runs; measured trace trong lab là CSV giả lập, không phải đo tại doanh nghiệp thật. Phút `_simulated` là simulated inputs; giá, hệ số, giới hạn retry và lương là giả định. Mọi tổng chi phí, CPS, delta và tỷ lệ trong B1–B4 đều **simulated**, trừ khi chỉ rõ số đếm/giá trị từ trace.

Mỗi kịch bản gọi lại `mo_hinh()`, giữ nguyên input; giá tool vẫn 15 VND/lượt. Hệ số xem lại/làm lại chỉ nhân tiền của hoạt động đó, không tạo thêm yêu cầu hay tự đổi kết quả chất lượng. Không đưa fixed cost 40 triệu VND/tháng vào B1–B4.

Đơn vị: total cost = VND; CPS và delta tuyệt đối = VND/success; delta phần trăm = (CPS kịch bản / CPS baseline − 1) × 100. Giữ số thực khi tính, làm tròn 3 chữ số thập phân khi trình bày.


| Scenario ID | Kịch bản | Parameter | Total cost (VND, simulated) | Successes | CPS (VND/success, simulated) | Delta CPS (VND/success, simulated) | Delta CPS (%, simulated) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1-00 | Baseline | `{}` | 4.373.585,132 | 978 | 4.471,968 | 0,000 | 0,000 |
| B1-01 | Token ×2 | `{'gia_vao': 52, 'gia_ra': 260}` | 4.619.170,264 | 978 | 4.723,078 | 251,110 | 5,615 |
| B1-02 | Token ×0,5 | `{'gia_vao': 13, 'gia_ra': 65}` | 4.250.792,566 | 978 | 4.346,414 | -125,555 | -2,808 |
| B1-03 | Review ×2 | `{'he_so_xem_lai': 2.0}` | 6.153.585,132 | 978 | 6.292,009 | 1.820,041 | 40,699 |
| B1-04 | Review ×0,5 | `{'he_so_xem_lai': 0.5}` | 3.483.585,132 | 978 | 3.561,948 | -910,020 | -20,349 |
| B1-05 | Rework ×2 | `{'he_so_lam_lai': 2.0}` | 6.637.585,132 | 978 | 6.786,897 | 2.314,928 | 51,765 |
| B1-06 | Rework ×0,5 | `{'he_so_lam_lai': 0.5}` | 3.241.585,132 | 978 | 3.314,504 | -1.157,464 | -25,883 |
| B1-07 | Lương +25% | `{'luong_phut': 2500}` | 5.384.585,132 | 978 | 5.505,711 | 1.033,742 | 23,116 |
| B1-08 | Tối đa 2 lần | `{'max_lan_chay': 2}` | 4.093.220,230 | 966 | 4.237,288 | -234,680 | -5,248 |
| B1-09 | Tối đa 1 lần | `{'max_lan_chay': 1}` | 3.621.780,644 | 881 | 4.110,988 | -360,980 | -8,072 |


**Đối chiếu:** CPS của 9 kịch bản lệch tối đa 0,0150% so với CPS đã làm tròn của giảng viên; delta % lệch tương đối tối đa 0,9194% so với delta % làm tròn, đều dưới 2%. Chênh lệch chỉ do làm tròn, không hiệu chỉnh số tính.

**Kiểm tra tuyến tính (simulated):** delta giảm 50% bằng −0,5 × delta gấp đôi; unit tests kiểm chứng số chưa làm tròn với sai số tuyệt đối dưới 1e-7 VND/success.


| Yếu tố | Delta ×2 (VND/success) | Delta ×0,5 (VND/success) | −0,5 × delta ×2 (VND/success) | Kết quả |
| --- | --- | --- | --- | --- |
| Token | 251,110 | -125,555 | -125,555 | PASS |
| Review | 1.820,041 | -910,020 | -910,020 | PASS |
| Rework | 2.314,928 | -1.157,464 | -1.157,464 | PASS |


- **Nhận xét:** tăng rework gấp đôi làm CPS tăng 51,765%, lớn hơn token gấp đôi (+5,615%, simulated); cần ưu tiên đo công sức nhân viên. Giới hạn attempts đổi cả chi phí và số success (978 → 966 → 881), nên không áp dụng kiểm tra tuyến tính cho retry.

## B2 · Combined Sensitivity — Đổi một cặp và xếp hạng

Kịch bản: `gia_vao=52, gia_ra=260, he_so_xem_lai=2.0`; các tham số khác giữ nguyên. Interaction I = delta CPS kết hợp − (delta CPS token + delta CPS review), đơn vị VND/success; đây là tác động trên CPS với mẫu số không đổi.


| Metric | Giá trị (simulated) |
| --- | --- |
| Total cost | 6.399.170,264 VND |
| Successes | 978 |
| Combined CPS | 6.543,119 VND/success |
| Combined delta CPS | 2.071,150 VND/success |
| Combined delta % | 46,314% |
| Tổng hai delta riêng | 2.071,150 VND/success |
| Interaction effect | 0,000000000 VND/success |


Xếp hạng theo mức tăng CPS của các cú sốc bất lợi được chỉ định (simulated):


| Hạng | Cú sốc | Delta CPS (%) |
| --- | --- | --- |
| 1 | Rework ×2 | 51,765% |
| 2 | Review ×2 | 40,699% |
| 3 | Lương +25% | 23,116% |


- **Tuyến tính:** combined CPS 6.543,119 VND/success (+46,314%, simulated), interaction 0,000000000; không có tương tác trong mô hình cộng khi 978 success giữ nguyên.
- **Ý nghĩa ranking:** rework/review là cú sốc +100%, lương là +25%; thứ hạng 51,765% → 40,699% → 23,116% (simulated) không phải hệ số nhạy chuẩn hóa giữa các tham số.
- **Nhân sự so với token:** review + rework chiếm 92,464% tổng chi phí, token chỉ 5,615% (simulated); đây là lý do chi phí nhân sự ảnh hưởng mạnh hơn.
- **Retry:** kỹ thuật của lượt 2–3 là 93.804,488 VND, chỉ 2,145% tổng chi phí (simulated), đã nằm trong token + tool; không được cộng thêm và không bỏ qua ảnh hưởng lên success/fallback.
- **Pilot cần theo dõi:** 3 nhóm yếu tố là tỷ lệ và phút làm lại/ca, tỷ lệ và phút xem lại/yêu cầu, lương thực trả/phút; các cú sốc hiện tại lần lượt làm CPS tăng 51,765%, 40,699% và 23,116% (simulated).

## B3 · Retry Economics — Giới hạn chạy lại và chi phí cả hệ thống

**Quy ước đề:** `attempt <= k`; yêu cầu có `so_lan_chay > k` chuyển nhân viên và đặt cả hai cột phút simulated về 0. Không giữ success cuối cùng nếu phải dùng lượt đã bị cắt; không sửa DataFrame gốc.

**Assumption fallback:** 12.000 VND cho mỗi unresolved = 1.200 − agent successes. System cost = agent cost + fallback; system/request chia 1.200, agent CPS chia successes. Toàn bộ chi phí trong bảng **simulated**, chưa cộng fixed cost 40 triệu VND/tháng của A4.


| Max attempts | Agent total cost (VND) | Agent successes | Unresolved | Fallback cost (VND) | System cost (VND) | System cost/request (VND/request) | Agent CPS (VND/success) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3.621.780,644 | 881 | 319 | 3.828.000,000 | 7.449.780,644 | 6.208,151 | 4.110,988 |
| 2 | 4.093.220,230 | 966 | 234 | 2.808.000,000 | 6.901.220,230 | 5.751,017 | 4.237,288 |
| 3 | 4.373.585,132 | 978 | 222 | 2.664.000,000 | 7.037.585,132 | 5.864,654 | 4.471,968 |


- **Agent CPS thấp nhất:** 1 attempt, 4.110,988 VND/success (simulated); đây không phải chính sách rẻ nhất cho công ty vì còn 319 unresolved.
- **System cost thấp nhất:** 2 attempts, 6.901.220,230 VND cho 1.200 yêu cầu, tương đương 5.751,017 VND/request (simulated).
- **Vì sao khác nhau:** từ 2 xuống 1 attempt tiết kiệm 471.439,586 VND agent nhưng thêm 85 việc sang nhân viên, tăng fallback 1.020.000,000 VND; ròng system cost tăng 548.560,414 VND (simulated).
- **Khuyến nghị:** dùng system cost/request để chọn 2 attempts trong mô hình toàn mẫu (5.751,017 VND/request, simulated), kèm success và an toàn; cần xác minh lại theo phạm vi pilot và dữ liệu thực trước khi chốt chính sách.
- **Giới hạn mô hình:** 12.000 VND/unresolved có thể chồng với phút rework đã tính, nhất là 74 ca lam_lai tại k=3; giữ nguyên công thức đề và đo phần xử lý còn lại trong pilot, không tự xóa rework để giảm chi phí.

## B4 · 100% Human Review — Xem lại toàn bộ đầu ra có run ok

Phạm vi **noi_dia + hang_nang**; “100%” là mọi yêu cầu có ít nhất 1 run `status='ok'`, không phải tất cả yêu cầu hay tất cả run. Các số đếm dưới đây lấy từ CSV; toàn bộ dữ liệu lab vẫn là giả lập.


| Đầu vào | Giá trị | Điều kiện lọc |
| --- | --- | --- |
| Requests trong phạm vi | 982 | loai thuộc noi_dia/hang_nang |
| Successful resolutions | 900 | ket_qua == 'thanh_cong' trong phạm vi |
| Requests cần review | 948 | request_id duy nhất có >=1 run ok trong phạm vi |
| Rework cases | 48 | ket_qua == 'lam_lai' trong phạm vi |
| Technical cost | 224.513,274 VND | token + tool của mọi run trong phạm vi, kể cả lỗi |
| Review time / lương | 5 phút/yêu cầu; 2.000 VND/phút | assumptions của đề |


Thống kê **simulated inputs**, lọc theo `ket_qua == lam_lai` (không lọc theo phút > 0 trên mọi yêu cầu):


| Tập lọc | Số ca | Tổng phút simulated | Mean phút/ca (simulated) | Median phút/ca (simulated) |
| --- | --- | --- | --- | --- |
| Toàn mẫu | 74 | 1132 | 15,297297297 | 14,500 |
| Riêng phạm vi pilot | 48 | 780 | 16,250 | 16,000 |


Scenario 2 theo hướng dẫn dùng mean **toàn mẫu** để áp lên 48 ca trong phạm vi; không dùng nhầm mean 16,25 phút của riêng pilot. Bảng báo cả mean toàn mẫu làm tròn 15,3 và giá trị đầy đủ; không làm tròn trung gian ở dòng đầy đủ. Phút review/rework mới **thay thế** chi phí review/rework cũ, không cộng chồng hai bộ phút.

Công thức: review = 948 × 5 × 2.000; rework = 48 × t_rework × 2.000; total = technical + review + rework; CPS = total / 900. Bảng dưới có chi phí **simulated**; CPS chỉ chia thành công agent, chưa gồm fallback/fixed và không phải mô hình end-to-end cho cả 982 yêu cầu.


| Kịch bản | Rework phút/ca | Review (VND) | Rework (VND) | Total (VND) | CPS (VND/success) | CPS/12.000 |
| --- | --- | --- | --- | --- | --- | --- |
| 9 phút theo đề | 9,000000000 | 9.480.000,000 | 864.000,000 | 10.568.513,274 | 11.742,793 | 0,978566× |
| Mean toàn mẫu làm tròn 1 số lẻ | 15,300000000 | 9.480.000,000 | 1.468.800,000 | 11.173.313,274 | 12.414,793 | 1,034566× |
| Mean toàn mẫu đầy đủ | 15,297297297 | 9.480.000,000 | 1.468.540,541 | 11.173.053,815 | 12.414,504 | 1,034542× |


- **Chênh do làm tròn:** dùng 15,3 thay mean đầy đủ 15,297297297 phút làm CPS tăng 0,288288 VND/success (simulated); mốc giảng viên ~12.414 VND là xấp xỉ, không phải kết quả làm tròn đến VND gần nhất của 12.414,793.

