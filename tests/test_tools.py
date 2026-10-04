"""Test non-network: config, skills, memory, file tools, shell gating, path traversal."""
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from runtime.config import Config
from runtime.memory import Memory
from runtime.skills import SkillStore
from runtime.tools import Browser, build_tools

tmp = Path(tempfile.mkdtemp(prefix="ma-test-"))
cfg = Config()
cfg.llm_api_key = "test-key"  # bypass validasi tanpa network
cfg.workspace = tmp
cfg.allow_shell = False

mem = Memory(tmp)
skills = SkillStore(REPO / "skills")
browser = Browser(cfg)
schemas, funcs = build_tools(cfg, mem, skills, browser)

ok = 0
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    assert cond, name
    ok += 1

# --- skills
check("skill catalog ada gmail", "gmail" in skills.names)
check("skill catalog ada scheduler", "scheduler" in skills.names)
check("load_skill gmail berisi konten", "Gmail" in skills.load("gmail"))
check("load_skill unknown ditangani", "tidak ditemukan" in skills.load("ngawur"))

# --- memory
check("remember", "Tersimpan" in funcs["remember"](fact="Pengguna bernama Wahyu"))
check("recall menemukan", "Wahyu" in funcs["recall"](query="siapa nama pengguna"))
check("recall kosong ditangani", "Tidak ada" in funcs["recall"](query="xyzzyplugh"))

# --- file tools (workspace-scoped)
check("write_file", "Tersimpan" in funcs["write_file"](path="notes/halo.txt", content="halo dunia"))
check("read_file", funcs["read_file"](path="notes/halo.txt") == "halo dunia")
check("list_dir", "halo.txt" in funcs["list_dir"](path="notes"))
check("path traversal ditolak", "di luar workspace" in funcs["read_file"](path="../../etc/passwd").lower()
      or "Gagal" in funcs["read_file"](path="../../etc/passwd"))

# --- shell gating
check("shell default nonaktif", "nonaktif" in funcs["shell"](command="echo hi").lower()
      or "ALLOW_SHELL" in funcs["shell"](command="echo hi"))

# --- schemas valid untuk OpenAI tools
for s in schemas:
    fn = s["function"]
    assert fn["name"] and fn["description"] and "parameters" in fn, fn["name"]
check("semua schema tool valid", True)

# --- agent tanpa LLM (bangun system prompt saja)
from runtime.agent import build_system_prompt
sp = build_system_prompt(cfg, skills, mem)
check("system prompt memuat persona", "Wahyu" in sp or "asisten pribadi" in sp.lower())
check("system prompt memuat katalog skill", "gmail" in sp.lower())

browser.close()
print(f"\n{ok} test lolos.")
