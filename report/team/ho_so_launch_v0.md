# Hồ sơ launch v0 · LogiX-VN · Gate 2a

**Nguyễn Thị Thùy Dung · 2A202603552 · L3A · Individual Lab.** Pilot **Planned / Not Approved**; **PENDING EXTERNAL REVIEW**. Bản tóm tắt một trang; chi tiết và bằng chứng cần nộp tại [E1–E2/Gates](chi_so.md), [chi phí](bang_chi_phi.md), [CP3](bang_loi.md), [pilot](pilot_plan.yaml). Giả lập = simulated; không có kết quả RCT hoặc quyết định hội đồng.

| Mục | Con số chính và giới hạn | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | CPS **4.471,968 VND/success**; 978 success; tổng **4.373.585,132 VND**. Phút nhân sự simulated; chưa gồm fixed/fallback. | Giả lập | Finance Lead |
| 2 · Ba yếu tố nhạy nhất | Theo các cú sốc CP2 chỉ định: rework×2 **+51,765%**; review×2 **+40,699%**; wage+25% **+23,116%** (simulated). | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Manual giả định **12.000 VND/request**; agent CPS/success khác mẫu số. B3 system/request: 3 attempts **5.864,654**, 2 attempts **5.751,017 VND** (simulated), cùng đơn vị request với manual. Chưa fixed; fallback có thể chồng rework; toàn mẫu khác pilot scope. | Giả lập | Finance Lead |
| 4 · KPI chính, dùng, an toàn | Trace lab: primary **994/1.200=82,83%**; sửa/bỏ **48/177=27,12%**; reopen **51/1.200=4,25%** (scope39/982=3,9715%). Mô tả, không causal lift; baseline70% là giả định. Adoption và audit sai hoàn là đề xuất chưa đo. | Giả lập | Product Manager |
| 5 · Error taxonomy & remediation | **20 ca, 5 nhóm, 5 đề xuất**; bảng reviewer18/20=90%, chưa chứng minh hai lượt độc lập. Rủi ro05/15/17 sai tiền/giá;07 báo thành công giả;20 hoàn trùng. Remediation chưa kiểm chứng. | Chưa | AI Engineering Lead |
| 6 · Pilot plan | Scope **noi_dia + hang_nang**, loại quoc_te/doi_tac. Staff **20+20**, MDE6pp; **859 effective/arm**, **5.980 raw/arm**, tổng11.960; **299/staff**. Power true5pp≈**0,642**. Main dự kiến **11/01–07/02/2027**; quyết định sớm nhất **18/02/2027**, hoặc **04/03/2027** nếu gia hạn42 ngày. 40 staff/6 depot, coverage, roster, events, kill switch và approval chưa xác minh. | Chưa | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Rework×2: CPS **6.786,897**; review100%/rework15,3 phút: **12.414,793 >12.000**, break-even review≈4,8 phút. Fixed/success **1.185,185→2.370,370** khi volume giảm nửa (simulated). Rà trace, bảo vệ human review, giữ mở rộng khi thiếu volume. Ước tính capture80%:28 ngày coverage13.748;20 ngày9.820, thiếu2.140 so mục tiêu. | Giả lập | PM trợ lý hoàn phí |

**Điều kiện trước mọi kích hoạt:** GATE-01 giao dịch/idempotency — AI Engineering Lead, 27/11/2026; GATE-02 thiết kế/ITT — Giám đốc vận hành, 26/11; GATE-03 staff/volume — Operations Manager, 26/11; GATE-04 events/đo phút thật — Data Engineering Lead, 27/11; GATE-05 stop/rollback≤30 phút — Giám đốc vận hành, 27/11; GATE-06 human review — Trưởng nhóm CSKH, 27/11; GATE-07 CP3 độc lập/miễn thay thế hợp lệ — Operations Manager, 27/11. Tất cả **Chưa**; bằng chứng nghiệm thu tại bảng Gates trong `chi_so.md`. Ngày kiểm tra là dự kiến, không phải phê duyệt.

**Kiểm tra lịch:** duyệt trước29/11 cho ramp30/11; main kiểm tra lại08/01. Phải xác minh40 staff và coverage6 depot ngoài pilot. Lưu lượng6 depot giả định đều:613,75 eligible/ngày, chưa đo thật. Không kịp điều kiện/ramp/follow-up thì hoãn và dịch lịch; không dùng dữ liệu ramp để đủ mẫu. SR-01 dừng sự cố ngay; SR-02 CPS>8.000 hai tuần trưởng thành; SR-03 sửa/bỏ>40% suggestions reviewed. Thiếu mẫu gia hạn block7 ngày, tối đa42, không dựa p-value; hết hạn thiếu thì Inconclusive/không mở rộng.

**Đề xuất Gate 2a: Go có điều kiện — chỉ xem xét kế hoạch pilot noi_dia + hang_nang; chưa cho kích hoạt. Nếu an toàn hoặc nguồn lực không thể đáp ứng, No-go cho lịch đề xuất và trình lại; hội đồng chưa ra quyết định.**
