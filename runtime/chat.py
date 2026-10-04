"""CLI chat interaktif:  python -m runtime.chat"""
from __future__ import annotations

import sys

from .agent import Agent
from .config import Config, REPO_ROOT


def main() -> int:
    cfg = Config()
    try:
        agent = Agent(cfg)
    except RuntimeError as e:
        print(e)
        return 1

    print(f"muse-assistant runtime — model: {cfg.llm_model} | workspace: {cfg.workspace}")
    print("Ketik 'keluar' untuk berhenti.\n")
    try:
        while True:
            try:
                text = input("kamu> ").strip()
            except EOFError:
                break
            if text.lower() in {"keluar", "exit", "quit"}:
                break
            if not text:
                continue
            print("asisten> ", end="", flush=True)
            print(agent.ask(text))
            print()
    except KeyboardInterrupt:
        pass
    finally:
        agent.close()
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    raise SystemExit(main())
