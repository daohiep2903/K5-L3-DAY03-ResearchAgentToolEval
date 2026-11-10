from pathlib import Path

from streamlit.testing.v1 import AppTest

import chat
import providers


APP = Path(__file__).resolve().parents[1] / "app.py"


def test_demo_requires_access_code_before_chat(monkeypatch):
    monkeypatch.setenv("DEMO_ACCESS_CODE", "test-demo-code")
    at = AppTest.from_file(str(APP)).run()
    assert not at.exception
    assert len(at.chat_input) == 0
    assert len(at.text_input) == 1


def test_ui_saves_clarification_turn_and_keeps_history(monkeypatch):
    monkeypatch.setenv("DEMO_ACCESS_CODE", "test-demo-code")
    monkeypatch.setattr(providers, "make_provider", lambda name: object())
    saved = []
    monkeypatch.setattr(chat, "write_transcript", lambda path, transcript: saved.append(transcript))

    def fake_loop(**kwargs):
        assert not any(t["function"]["name"] == "send" for t in kwargs["tools"])
        return {"status": "waiting_for_user", "assistant_text": "Please provide the URL.", "rounds": [], "tool_events": []}

    monkeypatch.setattr(chat, "run_model_tool_loop", fake_loop)
    at = AppTest.from_file(str(APP))
    at.session_state["authenticated"] = True
    at.run()
    at.chat_input[0].set_value("Read this article.").run()
    assert not at.exception
    assert saved[-1]["turns"][-1]["status"] == "waiting_for_user"
    assert at.session_state["history"][-1]["content"] == "Please provide the URL."


def test_ui_provider_error_is_generic_and_logged_without_secret(monkeypatch):
    monkeypatch.setenv("DEMO_ACCESS_CODE", "test-demo-code")

    def broken_provider(name):
        raise RuntimeError("private-api-key-should-not-leak")

    monkeypatch.setattr(providers, "make_provider", broken_provider)
    saved = []
    monkeypatch.setattr(chat, "write_transcript", lambda path, transcript: saved.append(transcript))
    at = AppTest.from_file(str(APP))
    at.session_state["authenticated"] = True
    at.run()
    at.chat_input[0].set_value("Search robotics news.").run()
    assert not at.exception
    turn = saved[-1]["turns"][-1]
    assert turn["status"] == "provider_error"
    assert "private-api-key" not in str(turn)
