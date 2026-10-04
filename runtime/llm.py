"""Klien LLM via OpenAI-compatible Chat Completions API + tool calling."""
from __future__ import annotations

from typing import Any

try:
    import httpx
except ImportError:  # beberapa env memakai nama paket httpx2
    import httpx2 as httpx  # type: ignore[no-redef]
from openai import OpenAI

from .config import Config


class LLMClient:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        try:
            self.client = OpenAI(
                base_url=cfg.llm_base_url,
                api_key=cfg.llm_api_key,
                timeout=cfg.llm_timeout,
            )
        except Exception:
            # Proxy env kadang berisi nilai aneh (mis. di sandbox) yang bikin
            # httpx gagal parse — coba lagi tanpa membaca proxy dari env.
            self.client = OpenAI(
                base_url=cfg.llm_base_url,
                api_key=cfg.llm_api_key,
                timeout=cfg.llm_timeout,
                http_client=httpx.Client(trust_env=False),
            )

    def chat(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None):
        """Satu turn chat; mengembalikan message object (bisa berisi tool_calls)."""
        kwargs: dict[str, Any] = {
            "model": self.cfg.llm_model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        return self.client.chat.completions.create(**kwargs)
