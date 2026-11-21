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


## B1 · Đổi từng yếu tố

| Kịch bản | Cách tính | Chi phí mỗi việc thành công | Thay đổi (%) |
| --- | --- | ---: | ---: |
| Giá token gấp đôi | 52 đ và 260 đ cho 1.000 token; giá tool giữ nguyên | ... | ... |
| Giá token giảm một nửa | 13 đ và 65 đ | ... | ... |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | ... | ... |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại ÷ 2 | ... | ... |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | ... | ... |
| Số ca làm lại giảm một nửa | Tiền làm lại ÷ 2 | ... | ... |
| Lương nhân viên tăng 25% | 2.500 đ mỗi phút | ... | ... |
| Chỉ cho chạy tối đa 2 lần | Bỏ lần chạy có attempt > 2; yêu cầu có so_lan_chay > 2 coi là chuyen_nhan_vien | ... | ... |
| Chỉ cho chạy 1 lần | Như trên với giới hạn 1 | ... | ... |

## B2 · Đổi một cặp và xếp hạng

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: ...
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất: 1. ... · 2. ... · 3. ...

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

| Giới hạn | Tổng chi phí trợ lý | Số yêu cầu không thành công | Chi phí cả hệ thống | Chi phí mỗi việc thành công |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | ... | ... | ... | ... |
| 2 lần | ... | ... | ... | ... |
| 3 lần | ... | ... | ... | ... |

- Giới hạn nào rẻ nhất cho công ty? Có trùng với giới hạn cho chi phí mỗi việc thành công thấp nhất không? ...

## B4 · Nếu phải xem lại tất cả

- Chi phí mỗi việc thành công khi xem lại 100% (`noi_dia` + `hang_nang`), so với 12.000 đ: ...
- Kết quả này nói gì về thứ pilot cần học được? ...
