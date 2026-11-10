# Live test report

- Local unit tests: 62 passed, 17 skipped (unimplemented TODO tests).
- Gemini authentication and v1beta structured tool calling: successful.
- Tavily search, Firecrawl scrape, RapidAPI timeline: each returned one item.
- Default gemini-3.8-flash: HTTP 503 (high demand).
- Evaluation fallback: gemini-2.5-flash, API v1beta, runtime overrides only.
- Base: 20 attempted, 8 measured, 3 passed, 12 provider errors.
- Extension: 10 attempted, 1 measured, 1 passed, 9 provider errors.
- Initial provider failures: HTTP 429, 5 requests/minute.
- Paced rerun stopped after confirmed daily exhaustion: 20 requests/day; retry after approximately 20h49m. The interrupted rerun did not create another result file.
- Full model evaluation remains incomplete because of provider quota.
- eval_group.json contains no cases.
- No source changes, commits, or GitHub uploads. Keys were passed only to test processes and were not saved in project files.

Result files:
- v0_B_base_gemini_20261110T180439685922.json
- v0_B_extension_gemini_20261110T180454810418.json

Integration limitation: run_eval loads the local .env with override=True. It overwrote the supplied Tavily/Firecrawl/RapidAPI process values with empty values, so nine recorded tool executions returned missing-key errors. The separate live API smoke tests succeeded with the supplied keys. Routing scores measure model tool selection only. A future complete rerun must isolate environment loading (for example DAY03_ENV_FILE) and use renewed model quota.

## Grok v0 preparation

- Added the xai provider using the existing normalized Chat Completions adapter.
- Enabled --provider xai in preflight_provider.py, run_eval.py, and chat.py.
- Rechecked offline tests: 62 passed, 17 skipped (CP3 TODOs).
- Baseline system_prompt.md, tools.yaml, and eval cases were preserved.
- The local .env had no XAI_API_KEY/XAI_MODEL; Tavily, Firecrawl, and RapidAPI keys were empty at inspection. Added empty xAI configuration entries only.
- Grok preflight and baseline have not run. Awaiting local credentials and model ID; no Grok metrics or version-log evidence can be reported yet.

## Grok connection result

- User-supplied xAI key saved only in the ignored local .env.
- Actual request: GET https://api.x.ai/v1/models.
- Result: HTTP 403, permission-denied; team has exhausted credits or reached its monthly spending limit.
- Evidence: xai_v0_connection_check.json (credential and team identifier omitted).
- Grok baseline was not executed because the provider cannot accept requests. No v0 metric or version-log row was fabricated.
- Resume after adding credits or raising the spending limit; select an available XAI_MODEL and configure the missing research tool keys.

## OpenAI connection check

- OPENAI_API_KEY and all three research tool keys are populated (values not logged; tool keys not live-tested in this check).
- Ran scripts/preflight_provider.py --provider openai against gpt-4o-mini.
- API returned HTTP 429: no credits remaining; add credits to continue.
- Evidence: openai_v0_connection_check.json. Baseline remains blocked by provider billing; no new metrics were generated.
