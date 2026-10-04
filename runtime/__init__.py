"""muse-assistant runtime — agen Python yang bisa ditenagai LLM apa pun (OpenAI-compatible)."""
from .agent import Agent
from .config import Config

__all__ = ["Agent", "Config"]
__version__ = "0.1.0"
