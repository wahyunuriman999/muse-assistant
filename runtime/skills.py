"""Skill loader: katalog + baca playbook SKILL.md sesuai kebutuhan."""
from __future__ import annotations

from pathlib import Path


class SkillStore:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self._catalog: dict[str, str] = {}
        self._scan()

    def _scan(self) -> None:
        if not self.skills_dir.is_dir():
            return
        for d in sorted(self.skills_dir.iterdir()):
            if d.name.startswith("_") or not d.is_dir():
                continue
            skill_file = d / "SKILL.md"
            if not skill_file.exists():
                continue
            # Deskripsi = baris non-heading pertama setelah judul
            desc = ""
            for line in skill_file.read_text(encoding="utf-8").splitlines():
                s = line.strip()
                if not s or s.startswith("#") or s.startswith(">"):
                    if s.startswith(">") and not desc:
                        desc = s.lstrip("> ").strip()
                    continue
                desc = desc or s
                break
            self._catalog[d.name] = desc or "(tanpa deskripsi)"

    def catalog_text(self) -> str:
        if not self._catalog:
            return "(tidak ada skill terpasang)"
        return "\n".join(f"- {name}: {desc}" for name, desc in self._catalog.items())

    def load(self, name: str) -> str:
        skill_file = self.skills_dir / name / "SKILL.md"
        if not skill_file.exists():
            return f"Skill '{name}' tidak ditemukan. Katalog:\n{self.catalog_text()}"
        return skill_file.read_text(encoding="utf-8")

    @property
    def names(self) -> list[str]:
        return sorted(self._catalog)
