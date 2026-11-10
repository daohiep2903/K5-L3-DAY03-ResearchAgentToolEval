from __future__ import annotations

import os

from providers.openai_provider import OpenAIProvider


class XAIProvider(OpenAIProvider):
    """Grok through xAI's OpenAI-compatible Chat Completions API."""

    def __init__(self) -> None:
        model = os.getenv("XAI_MODEL")
        if not model:
            raise RuntimeError("Set XAI_MODEL in .env to a model available in your xAI account.")
        super().__init__(
            api_key_env="XAI_API_KEY",
            base_url="https://api.x.ai/v1",
            default_model=model,
        )
