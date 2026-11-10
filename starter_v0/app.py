"""Streamlit UI using the same model/tool loop and transcript format as chat.py."""
from __future__ import annotations

import contextlib
import io
import json
import os
import secrets
import threading
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from chat import ROOT, now_iso, run_model_tool_loop, trim_history, write_transcript
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


st.set_page_config(page_title="Research Desk", page_icon="🔎", layout="centered")
st.markdown("""<style>
.stApp {background: #f5f6f2;}
.block-container {max-width: 960px; padding-top: 2.5rem;}
h1 {letter-spacing: -.045em; color: #163b34;}
[data-testid="stChatMessage"] {border: 1px solid #dce4df; border-radius: 16px; background: white;}
</style>""", unsafe_allow_html=True)
st.caption("VINUNI CODELAB · RESEARCH AGENT")
st.title("Research Desk")
st.markdown("Tìm nguồn, đọc bài và tạo bản tin — có dẫn chứng, có bước hỏi lại.")

# Optional shared demo access code, set only on the host. Never accept API keys.
code_path = ROOT.parent / ".local/demo_access_code.txt"
access_code = os.getenv("DEMO_ACCESS_CODE") or (code_path.read_text(encoding="utf-8").strip() if code_path.exists() else "")
if not access_code:
    st.info("Chủ phòng demo cần cấu hình mã truy cập trước khi mở ứng dụng.")
    st.stop()
if not st.session_state.get("authenticated"):
    entered = st.text_input("Mã truy cập buổi demo", type="password")
    if st.button("Mở Research Desk"):
        if secrets.compare_digest(entered, access_code):
            st.session_state.authenticated = True
            st.rerun()
        st.error("Mã chưa đúng.")
    st.stop()


@st.cache_resource
def demo_budget():
    return {"lock": threading.Lock(), "remaining": 30}

prompt_path = ROOT / "artifacts/system_prompt.md"
tools_path = ROOT / "artifacts/tools.yaml"
version = "v3-cp5"
provider_name = "openrouter"
model = "openai/gpt-4o-mini"

if "transcript" not in st.session_state:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    transcript_id = f"{version}_ui_{stamp}_{secrets.token_hex(3)}"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(build_artifact_version(version, prompt_path, tools_path)),
        "provider": provider_name, "model": model, "surface": "streamlit",
        "disabled_tools": ["send"],
        "system_prompt": str(prompt_path), "tools": str(tools_path),
        "history_window": 5, "max_tool_rounds": 4,
        "created_at": now_iso(), "turns": [],
    }
    st.session_state.history = []

transcript = st.session_state.transcript
cols = st.columns(3)
examples = [
    ("01 · Tìm nguồn", "Tìm trên web tin robotics tuần này, dùng query robotics."),
    ("02 · Loại trùng", 'Loại nguồn trùng từ [{"title":"A","url":"https://example.com/a"},{"title":"B","url":"https://example.com/a?utm_source=x"}], giữ bài đầu tiên.'),
    ("03 · Hỏi lại", "Tóm tắt bài viết này giúp mình."),
]
selected = None
for col, (label, text) in zip(cols, examples):
    if col.button(label, use_container_width=True):
        selected = text

with st.expander("Agent hỗ trợ những gì?"):
    st.markdown("Tìm web và bài đăng X, đọc URL, tra cứu policy nội bộ, tìm paper arXiv, loại nguồn trùng và tạo digest. Agent sẽ hỏi lại khi thiếu thông tin. Gửi Telegram bị tắt trong UI demo; kiểm tra bước xác nhận qua CLI.")

for turn in transcript["turns"]:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn.get("assistant_text") or "Chưa hoàn tất. Vui lòng thử lại.")
        if turn.get("tool_events"):
            with st.expander("Nguồn và kết quả công cụ"):
                st.json(turn["tool_events"])

user_text = st.chat_input("Bạn muốn nghiên cứu điều gì?", max_chars=8000) or selected
if user_text:
    budget = demo_budget()
    with budget["lock"]:
        if budget["remaining"] <= 0:
            st.info("Buổi demo đã hết lượt. Vui lòng báo người phụ trách.")
            st.stop()
        budget["remaining"] -= 1
    turn = {"turn_index": len(transcript["turns"]) + 1, "started_at": now_iso(), "user": user_text}
    with st.chat_message("user"):
        st.write(user_text)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Đang xử lý yêu cầu và kiểm tra nguồn…"):
                messages = [
                    {"role": "system", "content": prompt_path.read_text(encoding="utf-8")},
                    *trim_history(st.session_state.history, 5),
                    {"role": "user", "content": user_text},
                ]
                with contextlib.redirect_stdout(io.StringIO()):
                    result = run_model_tool_loop(
                        provider=make_provider(provider_name), messages=messages,
                        # Public demo never executes the publishing action.
                        tools=to_openai_tools([t for t in load_tool_declarations(tools_path) if t["name"] != "send"]),
                        model=model, max_tool_rounds=4,
                    )
                turn.update(result)
                st.session_state.history.extend([
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": result["assistant_text"]},
                ])
        except Exception:
            # Do not expose provider responses, credentials or local paths in UI.
            turn.update(status="provider_error", assistant_text="Chưa kết nối được dịch vụ. Vui lòng thử lại hoặc báo người phụ trách demo.", rounds=[], tool_events=[])
        st.markdown(turn["assistant_text"])
        if turn.get("tool_events"):
            with st.expander("Nguồn và kết quả công cụ"):
                st.json(turn["tool_events"])
    turn["ended_at"] = now_iso()
    transcript["turns"].append(turn)
    write_transcript(ROOT / "transcripts" / f"{transcript['transcript_id']}.transcript.json", transcript)

st.divider()
left, right = st.columns(2)
with left:
    st.download_button("Tải transcript cuộc trò chuyện", json.dumps(transcript, ensure_ascii=False, indent=2),
                       file_name=f"{transcript['transcript_id']}.transcript.json", mime="application/json")
with right:
    if st.button("Cuộc trò chuyện mới"):
        del st.session_state.transcript
        del st.session_state.history
        st.rerun()
st.caption("Chỉ gửi dữ liệu bạn được phép chia sẻ. Link demo tạm thời hoạt động khi máy chủ đang chạy.")
