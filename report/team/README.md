# Hồ sơ Individual Lab Day 13

**Nguyễn Thị Thùy Dung · 2A202603552 · L3A · Individual Lab.** Thông tin trách nhiệm tại [TEAM.md](../../TEAM.md). Bảng dưới liệt kê toàn bộ file hiện có trong thư mục này; trạng thái nội dung tách riêng với trạng thái duyệt/nộp Git.

| File | Nội dung | Trạng thái hiện tại |
| --- | --- | --- |
| `README.md` | Danh mục và chỉ dẫn nguồn | Đã đồng bộ filesystem; không phải quyết định nghiệm thu |
| `bang_chi_phi.md` | CP1 A1–A4 và CP2 B1–B4 | Content Complete;30 tests CP1–CP2; chi phí có phần simulated |
| `bang_loi.md` | CP3 taxonomy,20 ca, Root Cause,5 remediation và phân xử | Content Complete về phân tích; Independent Review Pending; CP3 PARTIAL |
| `cp3_reviewer_summary.md` | Bảng tổng hợp nguồn20 cặp nhãn | 18/20=90%, lệch13/17; chưa chứng minh hai lượt độc lập |
| `cp3_self_review.md` | Một bộ self-review đã điền | Đủ20 nhãn/lý do/confidence; khớp Final Labels20/20; nguồn/người/thời điểm review chưa xác minh |
| `pilot_plan.yaml` | CP4: D1/D2, kế hoạch pilot, feasibility và stop rules | Design & QA Complete; Planned / Not Approved;25 tests CP4 |
| `chi_so.md` | CP5 E1–E2:5 KPI,15 event,4 rủi ro,7 preconditions | Content Complete; adoption/audit chưa đo;15 tests CP5 |
| `ho_so_launch_v0.md` | CP5 E3: dossier7 mục | Content Complete; Go có điều kiện là khuyến nghị, không phê duyệt |
| `phieu_cham.md` | Template đánh giá Gate 2a | PENDING EXTERNAL REVIEW; giữ nguyên, không tự điền điểm |
| `group_report.md` | Báo cáo tổng hợp bài cá nhân CP1–CP5 | Đã đồng bộ; tổng70/70 PASS |
| `2A202603552_NguyenThiThuyDung.md` | Báo cáo cá nhân, công cụ, bằng chứng và giới hạn | Đã cập nhật trạng thái hiện tại; các xác nhận bên ngoài còn PENDING |
| `MSSV_HoTen.md` | Mẫu báo cáo cá nhân gốc | Khôi phục đúng nội dung từ `ed89502`; giữ mẫu và báo cáo cá nhân riêng |

**Gate 2a: PENDING EXTERNAL REVIEW. Pilot: Planned / Not Approved.** Việc chấp nhận Individual Lab và cách thay thế quy trình nhóm/hai reviewer/peer review chưa có xác nhận giảng viên. [Báo cáo cá nhân](2A202603552_NguyenThiThuyDung.md) khai báo công cụ; [chi_so.md](chi_so.md) ghi bằng chứng gate cần nộp. Không dùng unit tests hoặc self-review làm phê duyệt ngoài.

## Lịch sử Git và nguồn tham chiếu

Các file dưới đây không thuộc danh mục filesystem hiện tại và không còn trong HEAD sau commit `f33bac6`; nội dung lịch sử có thể đọc tại commit `ed89502`, không phải hai phiếu reviewer thật.

| File lịch sử | Nguồn chỉ đọc | Ý nghĩa |
| --- | --- | --- |
| `cp3_danh_gia_ca_nhan.md` | `git show ed89502:report/team/cp3_danh_gia_ca_nhan.md` | Initial và biểu mẫu chờ review ở thời điểm đó |
| `cp3_initial_snapshot_PENDING_bcfb8102e793.md` | `git show ed89502:report/team/cp3_initial_snapshot_PENDING_bcfb8102e793.md` | Phiếu trống lịch sử; không mô tả self-review hiện tại |

File mẫu `MSSV_HoTen.md` vừa được khôi phục trong local, chưa stage theo yêu cầu không chạy git add. Trạng thái đã theo dõi/đã lên GitHub chỉ được xác nhận sau khi người thực hiện review, stage và commit/push; không suy từ việc file hiện có.
