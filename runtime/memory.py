"""Ingatan jangka panjang: file markdown + pencarian keyword sederhana."""
from __future__ import annotations

from pathlib import Path


class Memory:
    def __init__(self, workspace: Path):
        self.path = workspace / "MEMORY.md"
        if not self.path.exists():
            self.path.write_text("# Memory\n\n", encoding="utf-8")

    def remember(self, fact: str) -> str:
        fact = fact.strip()
        if not fact:
            return "Fakta kosong — tidak disimpan."
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"- {fact}\n")
        return "Tersimpan di memori."

    def recall(self, query: str, limit: int = 10) -> str:
        """Cari baris yang mengandung kata kunci dari query."""
        keywords = [w.lower() for w in query.split() if len(w) > 2]
        if not keywords:
            return "Query terlalu pendek."
        hits: list[str] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            low = line.lower()
            if any(k in low for k in keywords):
                hits.append(line.strip())
                if len(hits) >= limit:
                    break
        if not hits:
            return "Tidak ada ingatan yang cocok."
        return "\n".join(hits)

    def dump(self, limit: int = 40) -> str:
        lines = [l for l in self.path.read_text(encoding="utf-8").splitlines() if l.strip()]
        return "\n".join(lines[-limit:]) if lines else "(memori masih kosong)"
