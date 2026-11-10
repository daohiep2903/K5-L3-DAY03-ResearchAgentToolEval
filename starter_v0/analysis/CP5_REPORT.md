# CP5 — UI, live chat và báo cáo

## Sản phẩm

- UI: [app.py](../app.py), Streamlit, dùng chung `run_model_tool_loop` và định dạng transcript với `chat.py`.
- Câu hỏi mẫu, chat nhiều lượt, xem kết quả tool, tải transcript và tạo cuộc trò chuyện mới.
- Dependency: `streamlit>=1.40,<2` trong requirements.txt.
- Truy cập local: http://127.0.0.1:8501 khi server đang chạy.
- Bắt buộc mã truy cập từ `DEMO_ACCESS_CODE` hoặc file `.local/demo_access_code.txt` ở root repo; file local được Git bỏ qua. Không nhập API key vào UI.
- Giới hạn tổng 30 lượt cho mỗi tiến trình, tối đa 4 vòng tool/lượt, 8000 ký tự đầu vào. Khởi động lại server sẽ reset ngân sách demo. UI tắt tool send; CLI vẫn dùng artifact đầy đủ để kiểm tra xác nhận.

## Chạy

Từ `starter_v0/`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true --browser.gatherUsageStats false
```

Mã truy cập demo đã tạo cục bộ tại `.local/demo_access_code.txt` (root repo). Nếu cài trên máy khác, cấu hình `DEMO_ACCESS_CODE` trong `.env`. Không commit mã, key hoặc `.env`. Mỗi phiên có transcript riêng trong `transcripts/`; cần xem nội dung trước khi chia sẻ.

## Live CLI

Đã chạy `chat.py` thực tế qua OpenRouter / `openai/gpt-4o-mini`, 5 lượt với artifact `v3-cp5`. Input kịch bản do Codex soạn, không phải lời thoại của người thử bên ngoài: [cp5_demo_input.txt](../samples/cp5_demo_input.txt).

Transcript: [v3-cp5_openrouter_20261110T205858874387.transcript.json](../transcripts/v3-cp5_openrouter_20261110T205858874387.transcript.json).

| Lượt | Yêu cầu | Công cụ | Trạng thái |
|---|---|---|---|
| 1 | Loại URL trùng từ hai nguồn có sẵn | deduplicate_sources | answered, giữ một nguồn |
| 2 | Format danh sách chưa cung cấp | clarify (text) | waiting_for_user |
| 3 | Bổ sung danh sách và yêu cầu bullets | format | answered |
| 4 | Yêu cầu gửi nội dung cụ thể lên Telegram | clarify (yes_no) | waiting_for_user |
| 5 | Từ chối và hủy đăng | không gọi tool | answered |

Không gọi send và không gửi Telegram thật. Đây là bằng chứng boundary, không phải bonus gửi thật.

## Kiểm tra

Toàn suite sau khi thêm UI: **88 passed, 14 skipped** (TODO tool có sẵn). Ba test UI ở `tests/test_ui.py` kiểm tra mã truy cập, lưu lượt clarify/history và lỗi provider không lộ dữ liệu bí mật. UI khởi tạo bằng Streamlit AppTest không có exception.

Một lượt UI live qua AppTest và model thật đã gọi deduplicate_sources, trả `answered` và lưu [UI transcript](../transcripts/v3-cp5_ui_20261110T140408247130Z_eea801.transcript.json). Endpoint `http://127.0.0.1:8501/_stcore/health` trả HTTP 200, `ok`. Đây là kiểm tra runtime, chưa phải kiểm tra hình ảnh trình duyệt hoặc người ngoài nhóm.

## Phần còn thiếu để chốt CP5

Automatic approval review từ chối mở Cloudflare Tunnel vì public exposure cho ứng dụng có API và policy nội bộ, kể cả sau khi thêm mã truy cập, budget và tắt send. Chưa có public URL. Cần người dùng xác nhận rõ cho phép phạm vi internet này trước khi thử lại; không chuyển sang cách mở tunnel khác để né xét duyệt.

Công cụ truy cập trình duyệt báo “browser access host is unavailable”; chưa kiểm tra hình ảnh/layout trong trình duyệt. Chưa có người ngoài nhóm dùng thử. Không khẳng định đã hoàn thành kiểm thử ngoài nhóm, deploy public hoặc hoàn thành trước mốc 16:30.

Báo cáo nhóm Phần A, B4 và B5a được cập nhật bằng bằng chứng thật. Thông tin thành viên khác và tự đánh giá cá nhân phải do người phụ trách bổ sung, không được suy diễn từ thao tác của Codex.
