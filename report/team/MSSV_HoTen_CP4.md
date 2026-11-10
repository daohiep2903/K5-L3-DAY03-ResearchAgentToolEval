# Báo cáo cá nhân — CP4: Thiết kế và chạy group eval

Điền thông tin thành viên và đổi tên file thành `MSSV_HoTen.md` trước khi nộp. Nội dung kỹ thuật dưới đây tổng hợp từ sản phẩm đã có với sự hỗ trợ của Codex; cần xác nhận đóng góp và việc tự kiểm tra thực tế của người phụ trách.

## 1. Thông tin thành viên

- Họ tên:
- MSSV:
- Email:
- GitHub:

## 2. Phần việc phụ trách

CP4: thiết kế bộ group eval gồm đúng 10 case (5 single-turn, 5 multi-turn), có case gọi tool mới của CP3; chạy model thật, đọc log và tổng hợp bằng chứng trong bảng B3 của báo cáo nhóm.

## 3. Đóng góp cụ thể

Các sản phẩm của phần CP4:

- Hoàn thiện `data/eval_group.json`, mỗi case có `id`, `phase=B`, `failure_type`, `query` hoặc `turns`, `expect` và `metadata.what_it_tests`.
- Kiểm tra định tuyến `deduplicate_sources`, thiếu danh sách nguồn, tra policy nội bộ, format dữ liệu đã có và giải thích khả năng mà không gọi tool.
- Kiểm tra nhiều lượt: bổ sung dữ liệu sau câu hỏi, sửa template, hủy đăng, đổi nguồn tìm kiếm và sửa kiểu sắp xếp/số lượng bài đăng.
- Giữ nguyên prompt và tool trong lúc làm CP4; lưu snapshot để kết quả gắn đúng artifact sau CP3. Không sửa bộ base hoặc extension.
- Phát hiện lỗi grader sắp xếp danh sách object gây TypeError. Bản sửa giữ thứ tự của danh sách có cấu trúc, thêm 3 regression test; chấm lại offline 80 kết quả CP2 đã lưu không thay đổi kết quả.
- Chạy lại đủ 10 case sau sửa lỗi, cập nhật bảng B3 và version log. Không dùng run lỗi đầu tiên làm bằng chứng hoàn tất.

## 4. Bằng chứng

- [Bộ 10 case group](../../starter_v0/data/eval_group.json).
- [Run hợp lệ](../../starter_v0/runs/v3-cp4_B_group_openrouter_20261110T194540409975.json).
- [Phân tích CP4](../../starter_v0/analysis/CP4_REPORT.md), [version log](../../starter_v0/artifacts/version_log.csv).
- [Code grader](../../starter_v0/run_eval.py), [regression tests](../../starter_v0/tests/test_eval_arguments.py).
- [Báo cáo nhóm — B3](group_report.md#b3-team-eval-cases).
- Snapshot dùng cho run: `starter_v0/artifacts/versions/cp4/`.

| Chỉ số | Kết quả |
|---|---:|
| Tổng số case / được đo | 10 / 10 |
| Provider error | 0 |
| Case đạt | 10 / 10 |
| Case accuracy | 100% |
| Tool routing accuracy | 100% |
| Argument accuracy | 100% |
| Multi-turn accuracy | 100% |

Provider/model: OpenRouter / `openai/gpt-4o-mini`, temperature=0. Contract test CP4: **60 passed**; toàn suite tại thời điểm hoàn thành CP4: **85 passed, 14 skipped**. Điểm group 100% là phép đo riêng, không thay thế điểm base CP2 90%.

Run đầu tiên đo 8/10 case, hai lỗi TypeError bị ghi nhầm là provider_error do exception handler chung. Đó là lỗi grader, không phải bằng chứng model thất bại hoặc hết quota. Run hợp lệ phía trên đã đo lại toàn bộ case sau khi sửa.

**AI/công cụ đã dùng:** Codex hỗ trợ viết case, sửa grader, chạy eval/test, phân tích log và soạn báo cáo; model thật được gọi qua OpenRouter.

## 5. Tự đánh giá

Giới hạn kỹ thuật: chỉ một run hợp lệ trên bộ 10 case do nhóm xây dựng, chưa chứng minh khả năng tổng quát. Multi-turn eval đưa hội thoại trước làm ngữ cảnh và chấm lượt cuối, không thay thế buổi chat tương tác đầy đủ. Routing/arguments đúng cũng không đảm bảo chất lượng nội dung đầu ra của tool hoặc câu trả lời cuối.

