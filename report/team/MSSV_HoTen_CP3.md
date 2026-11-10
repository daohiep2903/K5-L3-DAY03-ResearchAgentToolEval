# Báo cáo cá nhân — CP3: Tool mới và unit test

Điền thông tin thành viên và đổi tên file thành `MSSV_HoTen.md` trước khi nộp. Nội dung kỹ thuật dưới đây tổng hợp từ sản phẩm đã có với sự hỗ trợ của Codex; cần xác nhận đóng góp và việc tự kiểm tra thực tế của người phụ trách.

## 1. Thông tin thành viên

- Họ tên:
- MSSV:
- Email:
- GitHub:

## 2. Phần việc phụ trách

CP3: bổ sung tool `deduplicate_sources` cho research agent, viết tài liệu, đăng ký tool và unit test. Mục tiêu là loại nguồn trùng trước khi tạo digest, đồng thời kiểm tra code tool độc lập với việc model chọn tool.

## 3. Đóng góp cụ thể

Các sản phẩm của phần CP3:

- Implementation nhận danh sách nguồn có URL HTTP(S), giữ nguồn xuất hiện đầu tiên cùng metadata và trả số lượng/chỉ số nguồn trùng.
- Chuẩn hóa URL khi so sánh: bỏ fragment và tracking `utm_*`, `fbclid`, `gclid`; chuẩn hóa host và port mặc định. Giữ riêng đường dẫn, giao thức, port và tham số nội dung khác nhau.
- Kiểm tra input sai; trả error dict thay vì làm agent crash. Không trả kết quả dở dang khi một URL không hợp lệ.
- Có `TOOL.md`, đăng ký trong `TOOL_FUNCTIONS` và khai báo schema trong `tools.yaml`.
- Viết 5 hàm test, tương ứng 15 test case khi tính parametrization: happy path, input sai, lỗi URL, danh sách rỗng và không gộp nhầm nguồn khác nội dung.
- Chuẩn bị case định tuyến cho tool mới để nối sang CP4.

## 4. Bằng chứng

- [Implementation tool](../../starter_v0/tools/deduplicate_sources/tool.py).
- [Tài liệu và contract](../../starter_v0/tools/deduplicate_sources/TOOL.md).
- [Đăng ký tool](../../starter_v0/tools/__init__.py), [khai báo schema](../../starter_v0/artifacts/tools.yaml).
- [Unit tests](../../starter_v0/tests/test_tools_todo.py), [báo cáo CP3](../../starter_v0/analysis/CP3_REPORT.md).
- [Báo cáo nhóm — B5a](group_report.md#b5a-required-evidence--tool-mới-unit-test-ui).

Kết quả tại thời điểm hoàn thành CP3: **82 passed, 14 skipped** trên toàn suite; cả 15 case của tool mới đạt và không bị skip. Các skip còn lại là TODO tool có sẵn. Số test tăng ở CP4/CP5 không được tính là kết quả riêng của CP3.

Ví dụ unit test phát hiện lỗi mà routing eval không bắt được: code gộp nhầm URL `?id=1` và `?id=2`, làm mất nguồn, dù model gọi đúng tool và arguments. Unit test kiểm tra output còn routing eval kiểm tra lựa chọn của model.

**AI/công cụ đã dùng:** Codex hỗ trợ thiết kế, viết code/test, chạy kiểm tra và soạn báo cáo; pytest chạy offline, không dùng credit API cho unit test.

## 5. Tự đánh giá

Giới hạn kỹ thuật: tool chỉ nhận diện trùng URL theo quy tắc, không nhận diện bài cùng nội dung ở URL khác và không kiểm tra độ tin cậy. Tracking hoặc fragment có thể ảnh hưởng nội dung trên một số website nên quy tắc chuẩn hóa cần được giải thích khi demo.
