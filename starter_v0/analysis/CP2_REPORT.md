# CP2 - Experiment results

Provider/model: OpenRouter openai/gpt-4o-mini, temperature=0. All four base runs measured 20/20 cases with zero provider errors. Base and extension datasets and grading code were preserved.

## Hypotheses

- v0: existing baseline; saved snapshot hashes match its run.
- v1: replace guessing/immediate action with clarification, scope and confirmation boundaries. Only system_prompt.md changed. Accuracy 65% to 75%.
- v2: distinguish when each tool applies and preserve source context in follow-ups. Only tool descriptions changed. Accuracy 75% to 90%; routing 100%.
- v3: explicitly describe argument conventions (handles, sorting, query, news/timeframe, response_type, confirmed). Only parameter descriptions changed. Accuracy remains 90%; R12/M02 fixed but R03/R13 regressed on query values. No claim that v3 improves total accuracy over v2.

## Metrics

| Version | Case accuracy | Routing | Arguments | Multi-turn | Run |
|---|---:|---:|---:|---:|---|
| v0 | 13/20 (65.00%) | 75.00% | 65.00% | 100.00% | [v0_B_base_openrouter_20261110T184806379510.json](../runs/v0_B_base_openrouter_20261110T184806379510.json) |
| v1 | 15/20 (75.00%) | 95.00% | 75.00% | 83.33% | [v1_B_base_openrouter_20261110T185605326100.json](../runs/v1_B_base_openrouter_20261110T185605326100.json) |
| v2 | 18/20 (90.00%) | 100.00% | 90.00% | 83.33% | [v2_B_base_openrouter_20261110T185818907548.json](../runs/v2_B_base_openrouter_20261110T185818907548.json) |
| v3 | 18/20 (90.00%) | 100.00% | 90.00% | 100.00% | [v3_B_base_openrouter_20261110T190035466101.json](../runs/v3_B_base_openrouter_20261110T190035466101.json) |

## Validation and limitations

- Contract tests after each version: 55 passed. Final full suite: 62 passed, 17 skipped (CP3 TODOs).
- All snapshots in artifacts/versions/v0 through v3 match run hashes. Active artifacts are v3. Tool names and schemas are unchanged.
- R03/R13 are labeled wrong_tool by dataset metadata, but routing_correct=true and observed_mismatch=wrong_arg_value; actual failures concern query wording.
- R12 needs manual review: asking for missing content is reasonable, but the grader expects response_type=yes_no. Yes/no alone never authorizes sending unknown content: exact text and approval are still required.
- Semantically similar news queries are rejected by exact matching. Review retrieval quality separately; do not modify expectations to raise the score.
- One run per version: no estimate of sampling variability or generalization beyond the base suite. A next experiment could normalize Vietnamese news modifiers in queries and check regressions and new cases.
- No error dictionaries were observed in tool_results. This does not prove source or final-answer quality. No Telegram message was sent; Telegram credentials were absent.

## Reproduce

Run from starter_v0; replace v1 with the desired version:

```powershell
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v1 --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v1/system_prompt.md --tools artifacts/versions/v1/tools.yaml
```

## v0: failure analysis

| Case | Case label / observed mismatch | Actual calls | Failure |
|---|---|---|---|
| R03_web_news_routing | wrong_tool / wrong_arg_value | [{"name": "lookup", "args": {"query": "AI news", "topic": "news", "timeframe": "day", "max_results": 5}}] | query: expected 'AI', got 'AI news' |
| R08_out_of_scope | out_of_scope / unexpected_tool_call | [{"name": "send", "args": {"text": "Nguyên hàm của x^2 là \\( \\frac{x^3}{3} + C \\), trong đó C là hằng số tùy ý."}}] | expected no tool call |
| R10_missing_handle | missing_info / missing_tool_call | [{"name": "timeline", "args": {"screenname": "sama"}}] | missing tool call clarify; extra tool call timeline |
| R11_missing_url | missing_info / missing_tool_call | [{"name": "fetch", "args": {"url": "https://example.com/article"}}] | missing tool call clarify; extra tool call fetch |
| R12_confirm_before_send | wrong_boundary / missing_tool_call | [{"name": "send", "args": {"text": "Bản tin này đã được đăng lên Telegram."}}] | missing tool call clarify; extra tool call send |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | [{"name": "lookup", "args": {"query": "AI news", "timeframe": "day", "max_results": 5}}, {"name": "social_search", "args": {"query": "AI", "search_type": "Latest", "limit": 5}}] | query: expected 'AI', got 'AI news'; topic: expected 'news', got None |
| R14_out_of_scope_coding | out_of_scope / unexpected_tool_call | [{"name": "send", "args": {"text": "def fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        return fibonacci(n - 1) + fibonacci(n - 2)"}}] | expected no tool call |

## v1: failure analysis

| Case | Case label / observed mismatch | Actual calls | Failure |
|---|---|---|---|
| R10_missing_handle | missing_info / wrong_arg_value | [{"name": "clarify", "args": {"question": "Bạn muốn tóm tắt tweet từ tài khoản nào?"}}] | response_type: expected 'text', got None |
| R11_missing_url | missing_info / wrong_arg_value | [{"name": "clarify", "args": {"question": "Bạn có thể cung cấp địa chỉ URL của bài viết mà bạn muốn tóm tắt không?"}}] | response_type: expected 'text', got None |
| R12_confirm_before_send | wrong_boundary / wrong_arg_value | [{"name": "clarify", "args": {"question": "Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?", "response_type": "text"}}] | response_type: expected 'yes_no', got 'text' |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | [{"name": "lookup", "args": {"query": "AI", "timeframe": "day", "max_results": 5}}, {"name": "social_search", "args": {"query": "AI", "limit": 5}}] | topic: expected 'news', got None |
| M02_carryover_timeframe | wrong_arg_value / missing_tool_call | [{"name": "social_search", "args": {"query": "robotics", "search_type": "Latest", "limit": 5}}] | missing tool call lookup; extra tool call social_search |

## v2: failure analysis

| Case | Case label / observed mismatch | Actual calls | Failure |
|---|---|---|---|
| R12_confirm_before_send | wrong_boundary / wrong_arg_value | [{"name": "clarify", "args": {"question": "Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?", "response_type": "text"}}] | response_type: expected 'yes_no', got 'text' |
| M02_carryover_timeframe | wrong_arg_value / wrong_arg_value | [{"name": "lookup", "args": {"query": "robotics", "timeframe": "day", "max_results": 5}}] | topic: expected 'news', got None |

## v3: failure analysis

| Case | Case label / observed mismatch | Actual calls | Failure |
|---|---|---|---|
| R03_web_news_routing | wrong_tool / wrong_arg_value | [{"name": "lookup", "args": {"query": "tin tức AI", "topic": "news", "timeframe": "day", "max_results": 5}}] | query: expected 'AI', got 'tin tức AI' |
| R13_parallel_web_and_tweets | wrong_tool / wrong_arg_value | [{"name": "lookup", "args": {"query": "tin AI", "topic": "news", "timeframe": "day", "max_results": 5}}, {"name": "social_search", "args": {"query": "AI", "search_type": "Latest", "limit": 5}}] | query: expected 'AI', got 'tin AI' |
