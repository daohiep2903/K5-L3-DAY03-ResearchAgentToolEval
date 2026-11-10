# Nhóm agentcuibap — Research Agent Tool Eval

## Thông tin nhóm

- Tên nhóm: agentcuibap
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-agentcuibap-ResearchAgentToolEval`.
- URL repo nhóm đã khai báo: https://github.com/dinhphucdien179/K5-L3B-DAY03-agentcuibap-ResearchAgentToolEval
- Remote `origin` của bản làm việc hiện tại: https://github.com/daohiep2903/K5-L3-DAY03-ResearchAgentToolEval
- Nhánh làm việc hiện tại: `main`. 

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Đào Văn Hiệp | 2A202603813 | 26ai.hiepdv3@vinuni.edu.vn | https://github.com/daohiep2903 | CP2 |
|   2 | Chờ cung cấp | Chờ cung cấp | Chờ cung cấp | Chờ cung cấp | CP3: tool mới và unit test |
|   3 | Chờ cung cấp | Chờ cung cấp | Chờ cung cấp | Chờ cung cấp | CP4: group eval |

## Cá nhân
Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Đào Văn Hiệp — 2A202603813

### Phần việc phụ trách

- Phụ trách CP2 tối ưu prompt và tool declaration v1–v3.
- Không phụ trách CP1, CP3, CP4 hoặc CP5; 

### Đóng góp cụ thể

- CP2 đạt case accuracy 65% → 75% → 90% → 90%; lưu snapshot, hash, giả thuyết và phân tích lỗi. V3 không tăng tổng accuracy so với v2.
- Trong phạm vi CP2, Codex hỗ trợ chỉnh prompt/tool declaration, chạy kiểm tra và soạn báo cáo; thành viên bổ sung việc tự kiểm tra thực tế.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603813_DaoVanHiep.md).
- [CP2](starter_v0/analysis/CP2_REPORT.md), [version log](starter_v0/artifacts/version_log.csv).

## Thành viên phụ trách CP3 — Chờ thông tin

### Phần việc phụ trách

- Thiết kế và bổ sung tool `deduplicate_sources`, tài liệu TOOL.md, đăng ký implementation và schema.
- Viết unit test offline cho tool mới, giữ contract giữa tài liệu, tool declaration và code.

### Đóng góp cụ thể

- Xử lý nguồn trùng URL trước khi tạo digest; giữ nguồn đầu tiên và metadata gốc, không gọi mạng hoặc ghi file.
- Kiểm tra input/URL sai và trả error dict; bảo toàn URL khác tham số nội dung để tránh mất nguồn.
- Có 5 hàm test tương ứng 15 test case; toàn suite tại thời điểm CP3: 82 passed, 14 skipped, không có test tool mới bị skip.
- Chuẩn bị case định tuyến cho tool mới để nối sang CP4.
- Danh tính và cách tự kiểm tra cần thành viên bổ sung; Codex hỗ trợ implementation/test/báo cáo.

### Bằng chứng

- [Báo cáo cá nhân dự thảo](report/team/MSSV_HoTen_CP3.md), [phân tích CP3](starter_v0/analysis/CP3_REPORT.md).
- [Code tool](starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](starter_v0/tools/deduplicate_sources/TOOL.md).
- [Unit tests](starter_v0/tests/test_tools_todo.py), [đăng ký tool](starter_v0/tools/__init__.py), [schema](starter_v0/artifacts/tools.yaml).

## Thành viên phụ trách CP4 — Chờ thông tin

### Phần việc phụ trách

- Thiết kế 10 case group: 5 single-turn và 5 multi-turn, có định tuyến tool mới, missing information, sửa yêu cầu và boundary hủy gửi.
- Chạy model thật, đọc log và cập nhật bảng B3 trong báo cáo nhóm.

### Đóng góp cụ thể

- Hoàn thiện expect và metadata cho mỗi case, lưu snapshot artifact sau CP3; không sửa bộ base/extension.
- Phát hiện và sửa lỗi grader khi so danh sách object; thêm 3 regression test, chấm lại offline 80 kết quả CP2 không đổi.
- Run group hợp lệ đo đủ 10/10, tất cả đạt, không lỗi provider. Giữ run lỗi đầu tiên để giải thích, không dùng nó làm bằng chứng hoàn tất.
- Toàn suite tại thời điểm CP4: 85 passed, 14 skipped. Điểm group 100% không thay thế điểm base CP2 90%.
- Danh tính và cách tự kiểm tra cần thành viên bổ sung; Codex hỗ trợ case/eval/test/báo cáo.

### Bằng chứng

- [Báo cáo cá nhân dự thảo](report/team/MSSV_HoTen_CP4.md), [phân tích CP4](starter_v0/analysis/CP4_REPORT.md).
- [Bộ case group](starter_v0/data/eval_group.json), [run hợp lệ](starter_v0/runs/v3-cp4_B_group_openrouter_20261110T194540409975.json).
- [Grader](starter_v0/run_eval.py), [regression tests](starter_v0/tests/test_eval_arguments.py).

## Trạng thái bàn giao

- CP2, CP3, CP4: có sản phẩm và bằng chứng kiểm tra; chi tiết xem [báo cáo nhóm](report/team/group_report.md).
- CP5: có UI local và transcript live. Public tunnel bị automatic approval review chặn; chưa có link bên ngoài hoặc người ngoài nhóm dùng thử, nên chưa chốt hoàn tất CP5.
- Thông tin CP1 và người phụ trách CP1 chưa được xác nhận trong phân công này.
- Trước khi nộp: bổ sung danh tính hai thành viên, việc tự kiểm tra/tự đánh giá, nhánh nộp/commit chốt và đồng bộ repo nhóm. Không đưa `.env`, API key hoặc mã truy cập demo vào bài nộp.
