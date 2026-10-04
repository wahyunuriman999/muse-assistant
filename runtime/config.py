"""Konfigurasi runtime dari environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    # LLM (OpenAI-compatible API — bisa OpenAI, OpenRouter, Ollama, vLLM, dll.)
    llm_base_url: str = field(default_factory=lambda: os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"))
    llm_api_key: str = field(default_factory=lambda: os.getenv("LLM_API_KEY", ""))
    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    llm_timeout: int = field(default_factory=lambda: int(os.getenv("LLM_TIMEOUT", "120")))

    # Agent
    max_iters: int = field(default_factory=lambda: int(os.getenv("MAX_ITERS", "12")))
    system_prompt_file: Path = field(default_factory=lambda: Path(os.getenv(
        "SYSTEM_PROMPT_FILE", str(REPO_ROOT / "prompts" / "system-prompt.md"))))
    skills_dir: Path = field(default_factory=lambda: Path(os.getenv(
        "SKILLS_DIR", str(REPO_ROOT / "skills"))))

    # Workspace: SEMUA operasi file dibatasi di dalam direktori ini (keamanan)
    workspace: Path = field(default_factory=lambda: Path(os.getenv(
        "WORKSPACE", str(REPO_ROOT / "workspace"))).resolve())

    # Shell: default MATI — nyalakan hanya jika sadar risikonya
    allow_shell: bool = field(default_factory=lambda: os.getenv("ALLOW_SHELL", "0") == "1")
    shell_timeout: int = field(default_factory=lambda: int(os.getenv("SHELL_TIMEOUT", "30")))

    # Browser
    browser_headless: bool = field(default_factory=lambda: os.getenv("BROWSER_HEADLESS", "1") == "1")
    browser_timeout: int = field(default_factory=lambda: int(os.getenv("BROWSER_TIMEOUT", "30000")))

    def validate(self) -> None:
        if not self.llm_api_key:
            raise RuntimeError(
                "LLM_API_KEY belum diset. Contoh:\n"
                '  export LLM_API_KEY="sk-..."\n'
                '  export LLM_MODEL="gpt-4o-mini"  # atau model lain\n'
                "# Untuk Ollama lokal:\n"
                '  export LLM_BASE_URL="http://localhost:11434/v1"\n'
                '  export LLM_API_KEY="ollama"\n'
            )
        self.workspace.mkdir(parents=True, exist_ok=True)
