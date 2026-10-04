"""Agent loop: system prompt + skill + memory + tool-calling sampai tuntas."""
from __future__ import annotations

import json
from typing import Any

from .config import Config
from .llm import LLMClient
from .memory import Memory
from .skills import SkillStore
from .tools import Browser, build_tools


def build_system_prompt(cfg: Config, skills: SkillStore, memory: Memory) -> str:
    base = cfg.system_prompt_file.read_text(encoding="utf-8") if cfg.system_prompt_file.exists() else ""
    runtime_ctx = f"""
---

## KONTEKS RUNTIME (instruksi operasional, prioritaskan saat bekerja)

Kamu berjalan di runtime Python `muse-assistant`. Ikuti aturan kerja ini:

1. **Ingat dulu:** sebelum menjawab hal yang menyentuh preferensi/fakta pengguna,
   panggil `recall` dengan kata kunci relevan.
2. **Skill:** katalog skill yang terpasang:
{skills.catalog_text()}
   Muat playbook lengkapnya dengan `load_skill` saat tugasnya cocok — JANGAN menebak isinya.
3. **Web:** untuk fakta yang bisa berubah (harga, jadwal, berita), gunakan `web_search`
   lalu `web_fetch`. Untuk situs JavaScript / butuh interaksi (klik, isi form),
   gunakan `web_browse` (browser Chromium live).
4. **File:** semua operasi file HANYA di dalam workspace ({cfg.workspace}).
   Gunakan path relatif. Jangan keluar dari workspace.
5. **Simpan:** fakta tahan lama (nama, preferensi, keputusan) → `remember` SEBELUM menjawab.
6. **Jujur:** bedakan yang terverifikasi tool vs perkiraan. Jangan mengarang hasil tool.
7. **Selesai:** akhiri dengan jawaban langsung ke pengguna dalam bahasanya,
   tanpa membeberkan proses internal / nama tool.

Ingatan relevan saat ini:
{memory.dump(limit=15)}
""".strip()
    return (base + "\n\n" + runtime_ctx).strip()


class Agent:
    def __init__(self, cfg: Config):
        cfg.validate()
        self.cfg = cfg
        self.llm = LLMClient(cfg)
        self.memory = Memory(cfg.workspace)
        self.skills = SkillStore(cfg.skills_dir)
        self.browser = Browser(cfg)
        self.tool_schemas, self.tool_funcs = build_tools(cfg, self.memory, self.skills, self.browser)
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": build_system_prompt(cfg, self.skills, self.memory)}
        ]

    def _exec_tool(self, name: str, args: dict[str, Any]) -> str:
        fn = self.tool_funcs.get(name)
        if not fn:
            return f"Tool tidak dikenal: {name}"
        try:
            return str(fn(**args))
        except TypeError as e:
            return f"Argumen salah untuk {name}: {e}"
        except Exception as e:
            return f"Error di {name}: {e}"

    def ask(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})
        final = ""
        for _ in range(self.cfg.max_iters):
            resp = self.llm.chat(self.messages, tools=self.tool_schemas)
            msg = resp.choices[0].message
            # simpan pesan asisten (termasuk tool_calls) ke riwayat
            self.messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name,
                                 "arguments": tc.function.arguments}}
                    for tc in (msg.tool_calls or [])
                ] or None,
            })
            if not msg.tool_calls:
                final = msg.content or ""
                break
            for tc in msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                result = self._exec_tool(tc.function.name, args)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })
        else:
            final = final or "(batas iterasi tercapai)"
        return final.strip()

    def close(self):
        self.browser.close()
