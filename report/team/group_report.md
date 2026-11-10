# Báo cáo nhóm — Day 03 Research Agent Tool Eval

Báo cáo trình bày sản phẩm Research Desk và quá trình tối ưu dựa trên run JSON/transcript thật. Phần A giới thiệu cách dùng; Phần B ghi kết quả và giới hạn. CP5 còn thiếu link public và kiểm thử ngoài nhóm; chưa xác nhận hoàn thành trước mốc demo tại lớp.

## 1. Thông tin nhóm

- Tên nhóm: agentcuibap
- Lớp: L3B.
- Repo nhóm đã khai báo: https://github.com/dinhphucdien179/K5-L3B-DAY03-agentcuibap-ResearchAgentToolEval
- Phân công: Đào Văn Hiệp — CP2; hai thành viên CP3/CP4 chờ thông tin định danh; người phụ trách CP5 chưa xác nhận. Nhánh nộp và commit chốt chưa xác nhận.
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini`, temperature = 0, cùng bộ base 20 case.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Desk giúp tìm nguồn web và mạng xã hội, đọc bài viết, tra cứu policy/paper, loại nguồn trùng và tạo digest. Agent hỏi lại khi thiếu dữ liệu. CLI kiểm tra bước xác nhận trước khi gửi; UI demo tắt gửi Telegram.

**Cách chạy UI:**

Từ `starter_v0/`:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless true --browser.gatherUsageStats false
```

Dependency `streamlit>=1.40,<2` đã thêm vào `requirements.txt`. Dùng chung backend và định dạng transcript với `chat.py`. UI hỗ trợ câu hỏi mẫu, xem kết quả tool, tải transcript và cuộc trò chuyện mới.

**Link dùng thử (deploy):**

Local: http://127.0.0.1:8501 khi máy chủ đang chạy. Mã truy cập lấy từ `.local/demo_access_code.txt` tại root repo hoặc `DEMO_ACCESS_CODE` trong `.env`, không commit. Tổng ngân sách UI là 30 lượt/tiến trình, tối đa 4 vòng tool mỗi lượt; restart server sẽ reset ngân sách.

**Chưa có link public:** automatic approval review chặn Cloudflare Tunnel do phạm vi internet có thể truy cập API và policy nội bộ. Cần xác nhận rõ của người dùng cho việc chia sẻ này. Chưa có bằng chứng người ngoài nhóm dùng thử và chưa kiểm tra layout bằng trình duyệt. Chi tiết: [CP5_REPORT.md](../../starter_v0/analysis/CP5_REPORT.md).

### A2. Tool agent có

Tool đang khai báo trong `artifacts/tools.yaml`:

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| deduplicate_sources | loại nguồn trùng URL khỏi danh sách đã có, giữ item đầu tiên | có (CP3) |
| timeline | đọc bài đăng của một tài khoản X | không |
| social_search | tìm thảo luận trên X theo chủ đề | không |
| lookup | tìm nguồn web/tin tức | không |
| fetch | đọc nội dung URL | không |
| format | trình bày nguồn đã có thành digest | không |
| policy | tra cứu policy nội bộ | không |
| papers | tìm paper arXiv | không |
| paper_text | trích text từ paper arXiv | không |
| send | gửi Telegram sau xác nhận; chưa cấu hình gửi thật | không |

### A3. Câu hỏi mẫu để thử

1. Tìm trên web tin robotics tuần này, dùng query robotics.
2. Loại nguồn trùng từ `[{"title":"A","url":"https://example.com/a"},{"title":"B","url":"https://example.com/a?utm_source=x"}]`, giữ bài đầu tiên.
3. Tóm tắt bài viết này giúp mình. (Agent cần hỏi URL.)
4. Trình bày thành bullets: `[{"title":"Demo","url":"https://example.com/demo","summary":"Nội dung minh họa được cung cấp."}]`.
5. Qua CLI: đăng nội dung “Research demo completed.” lên Telegram. Kiểm tra hỏi xác nhận rồi trả lời hủy; UI tắt send.

## 3. Giải pháp

CP2 được thực hiện theo vòng lặp đọc log → đặt một giả thuyết → sửa một artifact → chạy lại base eval. Bộ eval và code chấm điểm giữ nguyên.

- **V1 — hành vi chung:** sửa `system_prompt.md` để bỏ chỉ dẫn đoán thông tin và gửi ngay; yêu cầu hỏi lại, giữ đúng phạm vi và chờ xác nhận nội dung trước khi gửi. Accuracy tăng từ 65% lên 75%.
- **V2 — routing:** chỉ sửa description của tool trong `tools.yaml`, nêu khi dùng/không dùng, phân biệt web/timeline/thảo luận xã hội và giữ nguồn ở lượt đổi chủ đề. Accuracy tăng lên 90%, routing đạt 100%.
- **V3 — arguments:** chỉ sửa description của tham số, nêu chuẩn handle không `@`, `Top/Latest`, `topic=news`, timeframe, query, `response_type` và `confirmed`. Accuracy giữ ở 90%; multi-turn tăng từ 83,33% lên 100%.

Các snapshot nằm trong `starter_v0/artifacts/versions/v0` đến `v3`; mỗi snapshot đã được đối chiếu hash với run tương ứng. Sau CP2, tools.yaml đang hoạt động được bổ sung tool CP3 nên hash khác snapshot v3. Muốn tái hiện số đo CP2 phải dùng snapshot tương ứng.

**CP3:** thêm `deduplicate_sources` để loại URL trùng trước khi tổng hợp digest. Tool chỉ xử lý nguồn đã có, giữ item đầu tiên và metadata gốc; không tìm kiếm hoặc xác minh nội dung. Tool có TOOL.md, implementation, khai báo schema và đăng ký TOOL_FUNCTIONS. Không cần key, mạng hoặc quyền ghi. Bằng chứng: [CP3_REPORT.md](../../starter_v0/analysis/CP3_REPORT.md). CP4 đã hoàn tất 10 case, kết quả xem B3.

**CP4:** tạo 10 case group, lưu snapshot sau CP3 và giữ nguyên prompt/tool khi đo. Sửa lỗi grader so danh sách object, bổ sung regression test và chấm lại offline kết quả CP2 trước khi chạy lại group.

**CP5:** UI Streamlit dùng chung vòng lặp model/tool với CLI, lưu transcript theo phiên, có mã truy cập và giới hạn lượt. UI không khai báo send; CLI giữ tool đầy đủ để kiểm tra boundary gửi qua hỏi xác nhận/hủy.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo baseline chưa tối ưu với cùng model. | N/A | 65.00% | [v0_B_base_openrouter_20261110T184806379510.json](../../starter_v0/runs/v0_B_base_openrouter_20261110T184806379510.json) |
| v1 | system_prompt.md | Hỏi lại và giới hạn hành động sẽ giảm lỗi thiếu thông tin, ngoài phạm vi và xác nhận. | 65.00% | 75.00% | [v1_B_base_openrouter_20261110T185605326100.json](../../starter_v0/runs/v1_B_base_openrouter_20261110T185605326100.json) |
| v2 | tools.yaml: tool descriptions | Nêu khi dùng/không dùng tool và giữ nguồn ở lượt sau sẽ giảm nhầm routing. | 75.00% | 90.00% | [v2_B_base_openrouter_20261110T185818907548.json](../../starter_v0/runs/v2_B_base_openrouter_20261110T185818907548.json) |
| v3 | tools.yaml: parameter descriptions | Quy ước arguments rõ sẽ giảm sai response_type/topic và lỗi nhiều lượt. | 90.00% | 90.00% | [v3_B_base_openrouter_20261110T190035466101.json](../../starter_v0/runs/v3_B_base_openrouter_20261110T190035466101.json) |

Chi tiết số đo và lỗi từng version: [CP2_REPORT.md](../../starter_v0/analysis/CP2_REPORT.md). Cả bốn run đo đủ 20/20 case, `provider_error_cases=0`. V3 ngang v2 về tổng accuracy (90%): sửa lỗi xác nhận/multi-turn nhưng phát sinh hai lỗi query. Contract test sau mỗi vòng: 55 passed; toàn suite cuối: 62 passed, 17 skipped thuộc TODO CP3.

Metric trước/sau trong bảng là case accuracy. Số đo chi tiết trên base:

| Version | Case đạt | Routing | Arguments | Multi-turn |
|---|---:|---:|---:|---:|
| v0 | 13/20 | 75% | 65% | 100.00% |
| v1 | 15/20 | 95% | 75% | 83.33% |
| v2 | 18/20 | 100% | 90% | 83.33% |
| v3 | 18/20 | 100% | 90% | 100.00% |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| v0 — R08, R14 | out_of_scope | `send(text=...)` | Gọi công cụ gửi để trả lời toán/code; expected no tool | V1 thêm giới hạn phạm vi; cả hai case đạt từ v1 đến v3 |
| v0 — R10 | missing_info | `timeline(screenname="sama")` | Đoán tài khoản khi người dùng chưa chỉ định | V1 chuyển sang `clarify`; v1 còn thiếu response_type, v2/v3 đạt |
| v0 — R11 | missing_info | `fetch(url="https://example.com/article")` | Tự đoán URL thay vì hỏi lại | V1 chuyển sang `clarify`; v2/v3 đạt đầy đủ arguments |
| v0 — R12 | wrong_boundary | `send(text="Bản tin này đã được đăng lên Telegram.")` | Gọi send khi chưa xác nhận và tự tạo nội dung | V1/v2 chuyển sang clarify nhưng sai response_type; v3 đạt với câu hỏi xác nhận |
| v2 — M02 | wrong_arg_value | `lookup(query="robotics", timeframe="day")` | Thiếu `topic=news` khi đổi chủ đề ở lượt tiếp theo | V3 ghi rõ giữ topic/timeframe; case đạt |
| v3 — R03 | Nhãn case: wrong_tool; mismatch: wrong_arg_value | `lookup(query="tin tức AI", topic="news", timeframe="day")` | Chọn đúng tool nhưng query khác `AI` theo exact matching | Chưa sửa trong CP2; đề xuất thử chuẩn hóa query ở vòng sau |
| v3 — R13 | Nhãn case: wrong_tool; mismatch: wrong_arg_value | `lookup(query="tin AI", topic="news", timeframe="day")` và `social_search(query="AI", search_type="Latest")` | Chọn đúng hai tool nhưng query web khác `AI` | Chưa sửa trong CP2; cần kiểm tra cả regression và chất lượng truy xuất |

Các tool call trong bảng được rút gọn để làm rõ lỗi; giá trị đầy đủ và `failures` nằm trong run JSON được liên kết ở B1. Nhãn `wrong_tool` của R03/R13 đến từ metadata case; lỗi quan sát thực tế ở v3 là arguments, không phải routing.

### B3. Team Eval Cases

Bộ [eval_group.json](../../starter_v0/data/eval_group.json) gồm đúng 5 đơn lượt và 5 nhiều lượt, mỗi case có phase B, failure_type, expect và metadata.what_it_tests. G01 và GM01 kiểm tra tool mới. Arguments đầy đủ giữ trong JSON; bảng dưới là bản tóm tắt.

| Case ID | Mục tiêu | Tool/hành vi kỳ vọng | Kết quả |
|---|---|---|---|
| G01_deduplicate_sources | Loại trùng nguồn đã có; không tìm kiếm hoặc format. | deduplicate_sources, items gốc | PASS |
| G02_missing_source_list | Hỏi lại khi chưa có danh sách nguồn. | clarify, response_type=text | PASS |
| G03_internal_privacy_policy | Dùng policy nội bộ thay vì tìm web. | policy, policy_area=data_privacy | PASS |
| G04_format_without_fetch | Format dữ liệu đã có, không đọc URL lại. | format, template=bullets | PASS |
| G05_explain_capability | Chỉ giải thích khả năng, không xử lý dữ liệu. | Không gọi tool | PASS |
| GM01_supplied_sources_after_clarification | Dùng nguồn bổ sung sau câu hỏi, giữ input gốc. | deduplicate_sources, items được bổ sung | PASS |
| GM02_latest_template_wins | Áp dụng sửa template mới nhất, giữ nguồn. | format, template=thread | PASS |
| GM03_cancel_publish | Hủy đăng ghi đè yêu cầu trước, không gửi. | Không gọi tool | PASS |
| GM04_switch_source_keep_scope | Chuyển X sang web và giữ thời gian tuần này. | lookup, query=robotics, topic=news, timeframe=week | PASS |
| GM05_social_sort_correction | Giữ chủ đề, sửa sắp xếp và số lượng. | social_search, query=battery recycling, search_type=Top, limit=2 | PASS |

[Run group hợp lệ](../../starter_v0/runs/v3-cp4_B_group_openrouter_20261110T194540409975.json) đo đủ 10/10, không lỗi provider; cả 10 case đạt, case/routing/arguments/multi-turn accuracy đều 100%. Đây là điểm group riêng, không thay thế điểm base CP2 90%.

Run đầu lỗi hai phép so object-list trong grader, bị ghi nhầm là provider_error; giữ run này nhưng không dùng làm bằng chứng hoàn tất. Bản sửa giữ thứ tự danh sách có cấu trúc, thêm ba regression test; chấm lại offline 80 kết quả CP2 không đổi. Toàn suite lúc CP4: 85 passed, 14 skipped; contract test: 60 passed. Chi tiết: [CP4_REPORT.md](../../starter_v0/analysis/CP4_REPORT.md).

### B4. Live Chat Evidence

Live CLI bằng `chat.py`, OpenRouter / `openai/gpt-4o-mini`, 5 lượt. Input demo do Codex soạn; không phải transcript người ngoài nhóm. Bằng chứng: [CLI transcript](../../starter_v0/transcripts/v3-cp5_openrouter_20261110T205858874387.transcript.json). Version `v3-cp5`, prompt hash `ee034de39d8b…`, tools hash `ea87e856d312…` (giá trị đầy đủ trong transcript).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Loại URL trùng từ hai nguồn đã có | deduplicate_sources | v3-cp5 | answered, còn một nguồn |
| 2 | Format danh sách chưa cung cấp | clarify, response_type=text | v3-cp5 | waiting_for_user |
| 3 | Cung cấp danh sách và chọn bullets | format | v3-cp5 | answered |
| 4 | Gửi nội dung cụ thể lên Telegram | clarify, response_type=yes_no | v3-cp5 | Chờ xác nhận, chưa gửi |
| 5 | Hủy đăng Telegram | Không gọi tool | v3-cp5 | Xác nhận hủy; không gửi thật |

UI live được kiểm tra bằng Streamlit AppTest với model thật: [UI transcript](../../starter_v0/transcripts/v3-cp5_ui_20261110T140408247130Z_eea801.transcript.json), gọi deduplicate_sources và trả lời thành công. Endpoint health local trả HTTP 200. Đây chưa thay thế kiểm thử trực quan/người ngoài nhóm.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới: deduplicate_sources | [TOOL.md](../../starter_v0/tools/deduplicate_sources/TOOL.md), [tool.py](../../starter_v0/tools/deduplicate_sources/tool.py) | Loại nguồn trùng URL, giữ thứ tự và metadata; trả số lượng và chỉ số nguồn trùng | Input sai trả error dict; không gọi mạng/ghi file; không khẳng định nguồn đáng tin |
| Unit test tool mới (≥ 3 test/tool) | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), [CP3_REPORT.md](../../starter_v0/analysis/CP3_REPORT.md) | 15 test case tool mới, không skip; toàn suite 82 passed, 14 skipped | Kiểm tra input sai, URL lỗi, không trả kết quả dở dang và không gộp URL khác nội dung |
| UI (lệnh chạy + link dùng thử) | [app.py](../../starter_v0/app.py), [CP5_REPORT.md](../../starter_v0/analysis/CP5_REPORT.md) | UI khởi tạo và một lượt live thành công; localhost:8501 health 200; toàn suite sau UI 88 passed, 14 skipped | Mã truy cập bắt buộc, 30 lượt/tiến trình, tắt send; public tunnel đang chờ cho phép |

Tool mới có 5 hàm test, tương ứng 15 test case khi tính parametrization. Nếu code gộp nhầm `?id=1` và `?id=2`, unit test phát hiện mất nguồn; routing eval vẫn có thể PASS vì model đã gọi đúng tên/arguments. Các skip còn lại thuộc tool có sẵn; chưa đạt bonus 0 skipped.

### B5. Bonus Evidence

Chưa có bằng chứng đủ điều kiện cho các hạng mục bonus dưới đây.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | Không có run local | Chưa thực hiện | Không khai số đo local |
| Hơn 3 tool mới (≥ 4) | Chỉ thêm deduplicate_sources | Đủ CP3 bắt buộc | Chưa đủ bonus |
| `send` gửi thật lên Telegram sau xác nhận | CLI transcript chỉ hỏi rồi hủy | Kiểm tra được boundary | Không gửi thật |
| Test challenge (0 skipped / regression test) | 88 passed, 14 skipped sau UI | Có regression test grader | Chưa đạt 0 skipped hoặc bằng chứng bug tool có sẵn |

Regression test sửa grader CP4 không được tự tính là regression bug của tool có sẵn.

### B7. Small Local Model Challenge (bonus)

Chưa thực hiện: không có run của hai model local hay vòng tối ưu local. Không khai metric hoặc kết luận cloud/local khi chưa có bằng chứng.

## 5. Khó khăn và cách xử lý

- Gemini hết quota, xAI/OpenAI trực tiếp hết credit hoặc đạt spending limit: giữ log thất bại, không dùng các run chưa đo đủ làm baseline. Các run CP2 hợp lệ dùng OpenRouter. Bằng chứng: [LIVE_TEST_REPORT.md](../../starter_v0/runs/LIVE_TEST_REPORT.md), [kiểm tra xAI](../../starter_v0/runs/xai_v0_connection_retry.json), [kiểm tra OpenAI](../../starter_v0/runs/openai_v0_connection_check.json).
- Grader CP4 không xử lý danh sách object: sửa có ba regression test, đối chiếu 80 kết quả CP2 không đổi và chạy lại group đủ 10/10; xem [CP4_REPORT.md](../../starter_v0/analysis/CP4_REPORT.md).
- Public tunnel bị automatic approval review chặn vì phạm vi API/policy nội bộ; giữ demo local và ghi rõ chưa chia sẻ internet. Công cụ trình duyệt không kết nối được nên AppTest/health chưa thay thế kiểm thử layout; xem [CP5_REPORT.md](../../starter_v0/analysis/CP5_REPORT.md).

## 6. Tổng hợp đóng góp

| Thành viên | Phân công | Bằng chứng |
|---|---|---|
| Đào Văn Hiệp — 2A202603813 | CP2 tối ưu v1–v3 | [Báo cáo cá nhân](2A202603813_DaoVanHiep.md) |
| Thành viên CP3 — chờ thông tin | Tool mới, tài liệu, đăng ký/schema và unit test | [Dự thảo CP3](MSSV_HoTen_CP3.md) |
| Thành viên CP4 — chờ thông tin | 10 case group, eval, regression grader và bảng B3 | [Dự thảo CP4](MSSV_HoTen_CP4.md) |

CP5 có sản phẩm UI/demo và bằng chứng ở B4–B5a; người phụ trách chưa xác nhận, không tính vào đóng góp của Đào Văn Hiệp.

Chi tiết: [TEAM.md](../../TEAM.md). Codex hỗ trợ code, kiểm tra và biên soạn; từng người cần xác nhận phần trực tiếp thực hiện và cách tự kiểm tra. Chưa có thông tin người phụ trách CP1.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **System prompt:** quy tắc hành vi chung như hỏi lại khi thiếu thông tin, không xử lý yêu cầu ngoài phạm vi bằng tool và chỉ gửi khi có nội dung đã xác nhận.
- **Tools.yaml:** description giúp phân biệt công cụ và nguồn; parameter description quy định giá trị và cách truyền arguments. V2 giữ nguyên prompt của v1; v3 giữ nguyên prompt và tool descriptions của v2.
- **Review thủ công:** R12 hỏi nội dung còn thiếu là hợp lý nhưng grader yêu cầu `yes_no`. Không được coi cờ xác nhận hay câu trả lời yes/no là đủ để gửi nội dung chưa biết. R03/R13 bị chấm sai vì query gần nghĩa không khớp chuỗi chính xác; cần kiểm tra chất lượng nguồn riêng.
- **Giới hạn kết quả:** chỉ một run/version trên cùng bộ base, chưa có đo lặp hay kiểm tra tổng quát trên case mới. V3 ngang v2 ở 90%, không tăng liên tục trên mọi metric. CP2 không chứng minh gửi Telegram thật hoặc chất lượng câu trả lời cuối.
- **CP4/CP5:** group 100% chỉ áp dụng bộ 10 case; nhiều lượt chấm lượt cuối với ngữ cảnh cho trước. UI chưa có public URL, kiểm thử ngoài nhóm hoặc layout trực quan. AppTest/health không thay thế các bước đó.
- **Tool mới:** không phát hiện bài cùng nội dung ở URL khác; bỏ tracking/fragment có thể không phù hợp với một số website.
- **Vòng tiếp theo:** thử một giả thuyết chuẩn hóa query chỉ còn chủ đề, tách từ chỉ tin tức/thời gian sang topic/timeframe, đặc biệt với tiếng Việt; đo lại cả case cũ và case mới, giữ nguyên grader.

Codex hỗ trợ chỉnh artifact, chạy eval/test, phân tích và soạn báo cáo. Phân công thực tế và việc từng thành viên tự kiểm tra cần được bổ sung trong TEAM.md và báo cáo cá nhân trước khi nộp.

## 8. Tài liệu tham khảo

- Yêu cầu lab: [CHECKPOINTS.md](../../CHECKPOINTS.md), [RULES.md](../../RULES.md), [RUBRIC.md](../../RUBRIC.md), [SUBMISSION.md](../../SUBMISSION.md).
- Contract và mẫu test: [tools/README.md](../../starter_v0/tools/README.md), [test_tools_examples.py](../../starter_v0/tests/test_tools_examples.py).
- Bằng chứng nội bộ: [CP2](../../starter_v0/analysis/CP2_REPORT.md), [CP3](../../starter_v0/analysis/CP3_REPORT.md), [CP4](../../starter_v0/analysis/CP4_REPORT.md), [CP5](../../starter_v0/analysis/CP5_REPORT.md).
- Công cụ AI: Codex hỗ trợ triển khai, kiểm thử và soạn báo cáo; số đo lấy từ run/transcript thật.

## 9. Trạng thái trước khi nộp

- CP2–CP4 có sản phẩm và bằng chứng. CP5 còn thiếu link bên ngoài và người ngoài nhóm dùng thử; không khai đã deploy hoặc gửi Telegram thật.
- Bổ sung danh tính hai thành viên, tự đánh giá/xác nhận đóng góp và nhánh nộp/commit chốt; đồng bộ bản nộp với repo nhóm.
- Xem lại transcript trước khi chia sẻ; không nộp `.env`, API key, mã truy cập hoặc `.local/`.
