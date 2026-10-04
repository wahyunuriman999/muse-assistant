# 06 — Runtime: Agen yang Benar-Benar Jalan

`runtime/` adalah implementasi referensi: agen Python yang ditenagai **LLM apa pun**
via OpenAI-compatible API, dengan browser live, tools, memori, dan skill dari repo ini.

```
runtime/
├── __init__.py      ← Agent, Config
├── config.py        ← semua pengaturan via environment variables
├── llm.py           ← klien chat-completions + tool calling
├── agent.py         ← loop: pikir → panggil tool → lanjut sampai tuntas
├── tools.py         ← web_search/fetch/browse, file, shell, memory, skills
├── memory.py        ← ingatan markdown + recall keyword
├── skills.py        ← katalog & loader SKILL.md
└── chat.py          ← CLI: python -m runtime.chat
```

## Mulai cepat

```bash
cd muse-assistant
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium        # untuk tool web_browse (browser live)

export LLM_API_KEY="sk-..."        # wajib
export LLM_MODEL="gpt-4o-mini"     # opsional (default)
# export LLM_BASE_URL="http://localhost:11434/v1"  # untuk Ollama lokal
# export LLM_API_KEY="ollama"                       # (Ollama tidak cek key)

python -m runtime.chat
```

## LLM yang didukung

Apa pun yang bicara protokol OpenAI Chat Completions + tool calling:

| Penyedia | `LLM_BASE_URL` | Catatan |
|---|---|---|
| OpenAI | `https://api.openai.com/v1` (default) | butuh API key |
| OpenRouter | `https://openrouter.ai/api/v1` | banyak model, satu key |
| Ollama (lokal) | `http://localhost:11434/v1` | gratis, offline; key isi bebas |
| vLLM / LM Studio | URL server-mu | model sendiri |

> Model kecil/lokal bisa memakai tool, tapi kualitas pemakaian tool-nya
> bervariasi. Untuk hasil terbaik pakai model dengan function-calling yang kuat.

## Tools yang tersedia

| Tool | Fungsi |
|---|---|
| `web_search` | Cari web tanpa API key (DuckDuckGo → fallback Bing) |
| `web_fetch` | Ambil teks bersih dari URL (tanpa JS) |
| `web_browse` | **Browser Chromium live**: goto, text, click, fill, press, screenshot |
| `read_file` / `write_file` / `list_dir` | File — **terbatas di dalam `workspace/`** |
| `shell` | Perintah shell — **nonaktif** kecuali `ALLOW_SHELL=1` |
| `remember` / `recall` | Ingatan jangka panjang (`workspace/MEMORY.md`) |
| `load_skill` | Muat playbook `skills/<nama>/SKILL.md` sesuai kebutuhan |

## Environment variables

| Var | Default | Keterangan |
|---|---|---|
| `LLM_API_KEY` | — | **wajib** |
| `LLM_MODEL` | `gpt-4o-mini` | nama model |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | endpoint OpenAI-compatible |
| `WORKSPACE` | `./workspace` | direktori kerja agen (file tools terkunci di sini) |
| `ALLOW_SHELL` | `0` | set `1` untuk mengizinkan tool shell (berisiko!) |
| `MAX_ITERS` | `12` | batas putaran tool per pertanyaan |
| `BROWSER_HEADLESS` | `1` | `0` untuk melihat browser-nya |

## Keamanan

- **File terkunci di workspace** — path traversal (`../../`) ditolak.
- **Shell default mati** — nyalakan hanya jika kamu paham risikonya.
- **Kredensial** — `LLM_API_KEY` hanya di env, tidak pernah di-log/di-commit.
- Tool `web_browse` headless dan tidak menyimpan sesi login antar-run
  (tambah sendiri jika butuh login persisten).

## Yang belum ada (jujur)

Runtime ini adalah **fondasi yang jalan**, bukan replika penuh:

- ❌ Penjadwalan (cron/hook) — belum ada; pakai cron OS + `python -m runtime.chat <<< "..."` untuk sekarang
- ❌ Sub-agen paralel — belum ada
- ❌ Integrasi OAuth (Gmail, Kalender, dsb.) — perlu ditulis per layanan mengikuti `skills/`
- ❌ Widget/artefak kaya — output masih teks + file

Semua itu adalah extension point yang wajar — arsitekturnya di `docs/04-architecture.md`.
