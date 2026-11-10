# CP3 — Tool mới và unit test

Tool `deduplicate_sources` đã được triển khai, đăng ký trong `tools/__init__.py` và khai báo ở `artifacts/tools.yaml`. Contract và ví dụ: [TOOL.md](../tools/deduplicate_sources/TOOL.md).

Tool loại nguồn trùng URL khỏi danh sách đã có, giữ item đầu tiên cùng URL/metadata gốc. So sánh bỏ fragment, tracking `utm_*`/`fbclid`/`gclid`, chuẩn hóa host và port mặc định. Tham số nội dung, đường dẫn, giao thức và port khác được giữ riêng. Không gọi mạng, không cần key, không ghi file.

Giới hạn: không nhận diện bài cùng nội dung ở URL khác, không xác minh độ tin cậy. Bỏ tracking/fragment là heuristic, có thể không phù hợp nếu website dùng chúng để chọn nội dung.

## Kiểm tra

Lệnh từ `starter_v0/`: `.\.venv\Scripts\python.exe -m pytest -q`.

Kết quả: **82 passed, 14 skipped**. Tool mới có **15 test case**, gồm 5 hàm test với các giá trị parametrized; không có test tool mới bị skip. Các skip còn lại là TODO của tool có sẵn, không phải bonus 0 skipped.

Test ở [test_tools_todo.py](../tests/test_tools_todo.py) kiểm tra: gộp nguồn và giữ metadata/input; input sai; lỗi URL trả error dict không có kết quả dở dang; danh sách rỗng; bảo toàn URL có tham số nội dung/giao thức/port khác nhau.

Ví dụ lỗi unit test bắt được nhưng routing eval không bắt: model gọi đúng tool và args nhưng code gộp nhầm `?id=1` và `?id=2`, làm mất nguồn. Unit test kiểm tra output phát hiện được lỗi này, còn routing eval chỉ so tool call.

## Nối sang CP4

Tại thời điểm hoàn thành CP3, mới thêm `G01_deduplicate_sources`, chưa chạy live model. Sau đó CP4 đã hoàn thiện đủ 5 single-turn và 5 multi-turn, chạy thật đạt 10/10. Bằng chứng và giới hạn: [CP4_REPORT.md](CP4_REPORT.md).

Snapshot CP2 v0–v3 giữ nguyên. Artifact tools hiện tại đã thêm tool CP3 nên hash khác snapshot v3; dùng snapshot khi muốn tái hiện số đo CP2.

Codex hỗ trợ thiết kế, code, test và soạn bằng chứng. Phân công thực tế và việc tự kiểm tra của thành viên cần ghi riêng trong TEAM.md/báo cáo cá nhân.
