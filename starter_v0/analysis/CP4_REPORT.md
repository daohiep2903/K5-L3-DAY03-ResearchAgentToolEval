# CP4 - Group evaluation

Dataset: data/eval_group.json, 10 cases (5 single-turn, 5 multi-turn).
Provider: OpenRouter / openai/gpt-4o-mini, temperature=0.
Artifact version: v3-cp4+pee034de39d8b+tea87e856d312.
Prompt hash: ee034de39d8ba6a7e1153c0a2a3dd127e90076c1840377e4dfd70a1f7d9ce574.
Tools hash: ea87e856d312878c2be4e9700c8116efc20c07c9b2f5deb4375dd9391190dbd1.
Snapshot: artifacts/versions/cp4/. No prompt or tool tuning was performed during CP4.

## Result

Valid run: [v3-cp4_B_group_openrouter_20261110T194540409975.json](../runs/v3-cp4_B_group_openrouter_20261110T194540409975.json).

```json
{
  "total_cases": 10,
  "measured_cases": 10,
  "provider_error_cases": 0,
  "passed_cases": 10,
  "case_accuracy": 1.0,
  "tool_routing_accuracy": 1.0,
  "argument_accuracy": 1.0,
  "multiturn_accuracy": 1.0,
  "failure_counts": {},
  "observed_mismatch_counts": {}
}
```

No tool execution error dictionaries were recorded. Deduplication is tested in G01 (single-turn) and GM01 (context supplied after clarification). Other cases cover missing inputs, internal policy, formatting, capability explanations, cancellation, source switches, and argument corrections. No Telegram send is requested by the final turns.

## Grader defect and validation

The first run, v3-cp4_B_group_openrouter_20261110T194412171420.json, is incomplete (8 measured, 2 errors), so it is not evidence of a complete evaluation. Its TypeError came from sorting dictionaries in normalize_value, not a model provider failure. The generic exception handler mislabeled this as provider_error.

Fix: retain order for structured lists (important because deduplication keeps the first source); continue case/order-insensitive comparison for scalar lists. Expected arguments were not removed or loosened. Added tests/test_eval_arguments.py with three regression tests, including reordered sources and wrong metadata failing comparison.

Full suite: 85 passed, 14 skipped. Contract tests: 60 passed. Regraded all 80 existing CP2 recorded results offline with the fix: pass, routing, argument and failure fields all unchanged. Base/extension datasets preserved.

This is one run on a small group-authored suite; 100% does not establish generalization or output quality. Multi-turn cases provide prior conversation as context and score the latest turn, not a complete interactive session. Routing eval checks calls/args; CP3 tests check actual deduplication output. Group score must not replace the base-suite score.

## Reproduce

From starter_v0:

```powershell
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v3-cp4 --suite group --eval-cases data/eval_group.json --system-prompt artifacts/versions/cp4/system_prompt.md --tools artifacts/versions/cp4/tools.yaml
```

## Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_deduplicate_sources | Route an explicit deduplication request with available items to the new local tool, preserving the original source arguments rather than fetching or formatting. | deduplicate_sources {"items": [{"title": "Original", "url": "https://example.com/article"}, {"title": "Tracking copy", "url": "https://example.com/article?utm_source=newsletter#top"}]} | PASS |
| G02_missing_source_list | Clarify missing items instead of inventing sources or searching. | clarify {"response_type": "text"} | PASS |
| G03_internal_privacy_policy | Use local internal policy rather than public web search. | policy {"policy_area": "data_privacy"} | PASS |
| G04_format_without_fetch | Format provided items without refetching or deduplicating unique sources. | format {"items": [{"title": "Research note", "url": "https://example.com/research", "summary": "A supplied summary."}], "template": "bullets"} | PASS |
| G05_explain_capability | Explain capability without calling a tool or processing absent data. | no_tool | PASS |
| GM01_supplied_sources_after_clarification | Use the source list supplied after clarification and preserve both original input items. | deduplicate_sources {"items": [{"title": "First", "url": "https://example.com/a"}, {"title": "Copy", "url": "https://example.com/a?utm_source=x"}]} | PASS |
| GM02_latest_template_wins | Apply the latest layout correction while retaining provided source items. | format {"items": [{"title": "Paper note", "url": "https://example.com/note", "summary": "Provided text."}], "template": "thread"} | PASS |
| GM03_cancel_publish | An explicit cancellation overrides an earlier publishing request; never send or ask to reconfirm. | no_tool | PASS |
| GM04_switch_source_keep_scope | Switch from social to web and preserve the latest explicit news time window. | lookup {"query": "robotics", "topic": "news", "timeframe": "week"} | PASS |
| GM05_social_sort_correction | Apply the latest sort and count corrections without switching sources. | social_search {"query": "battery recycling", "search_type": "Top", "limit": 2} | PASS |
