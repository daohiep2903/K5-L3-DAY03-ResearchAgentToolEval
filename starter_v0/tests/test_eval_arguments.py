from run_eval import compare_subset, evaluate_phase_b


def test_source_object_list_is_graded_without_sorting_dicts():
    items = [{"url": "https://example.com/a"}, {"url": "https://example.com/b"}]
    case = {"failure_type": "wrong_arg_value", "expect": {"tool_calls": [
        {"name": "deduplicate_sources", "args": {"items": items}},
    ]}}
    result = evaluate_phase_b(case, [{"name": "deduplicate_sources", "args": {"items": items}}], None)
    assert result["passed"] is True


def test_source_order_and_metadata_mismatches_are_not_hidden():
    items = [{"url": "https://example.com/a", "title": "First"}, {"url": "https://example.com/b"}]
    assert compare_subset({"items": items}, {"items": list(reversed(items))})[0] is False
    assert compare_subset({"items": items}, {"items": [{"url": "https://example.com/a", "title": "Invented"}, items[1]]})[0] is False


def test_scalar_list_matching_stays_case_and_order_insensitive():
    assert compare_subset({"tags": ["AI", "News"]}, {"tags": ["news", " ai "]})[0] is True
    assert compare_subset({"count": 2}, {"count": 3})[0] is False
