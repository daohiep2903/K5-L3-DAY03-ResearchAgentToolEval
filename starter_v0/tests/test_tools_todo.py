"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_deduplicate_sources_preserves_first_item_and_input() -> None:
    import copy

    items = [
        {"url": "https://EXAMPLE.com:443/a?id=1&utm_source=x#top", "title": "first", "summary": "keep"},
        {"url": "https://example.com/a?id=1&fbclid=x", "title": "duplicate"},
        {"url": "https://example.com/a?id=2", "title": "different"},
    ]
    original = copy.deepcopy(items)
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=items)
    assert result["items"] == [original[0], original[2]]
    assert result["input_count"] == 3
    assert result["item_count"] == 2
    assert result["duplicate_count"] == 1
    assert result["duplicates"] == [{"index": 1, "kept_index": 0}]
    assert items == original


@pytest.mark.parametrize("items", [None, "not a list", {}, [None], [{}], [{"url": 12}], [{"url": " "}]])
def test_deduplicate_sources_rejects_bad_input_from_model(items) -> None:
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=items)
    assert result["error"] == "ValueError"
    assert result["message"]
    assert "items" not in result


@pytest.mark.parametrize("url", ["relative/path", "ftp://example.com/a", "https://example.com:bad/a", "https://[broken", "https://user:secret@example.com/a"])
def test_deduplicate_sources_url_failure_returns_error_without_partial_results(url) -> None:
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=[{"url": "https://example.com/good"}, {"url": url}])
    assert result["tool"] == "deduplicate_sources"
    assert result["error"] == "ValueError"
    assert "items" not in result
    assert "secret" not in result["message"]


def test_deduplicate_sources_empty_list_is_valid() -> None:
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=[])
    assert result["items"] == []
    assert result["duplicate_count"] == result["item_count"] == result["input_count"] == 0


def test_deduplicate_sources_keeps_distinct_content_urls() -> None:
    urls = ["http://example.com/a", "https://example.com/a", "https://example.com/A", "https://example.com/a/", "https://example.com:8443/a", "https://example.com/a?id=1", "https://example.com/a?id=2"]
    result = TOOL_FUNCTIONS["deduplicate_sources"](items=[{"url": url} for url in urls])
    assert [item["url"] for item in result["items"]] == urls
    assert result["duplicate_count"] == 0
