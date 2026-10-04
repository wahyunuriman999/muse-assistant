# Muse Assistant

Blueprint open-source untuk membangun **asisten pribadi AI** yang hangat, cakap, dan benar-benar membantu — terinspirasi dari cara kerja Muse, asisten pribadi buatan Meta.

Repo ini bukan sekadar dokumentasi. Ini adalah **kit lengkap**: persona, daftar kemampuan, katalog integrasi, template skill yang bisa dipakai ulang, contoh workflow, dan template system prompt — semuanya dirancang agar kamu bisa merakit asisten versimu sendiri di atas model bahasa apa pun.

> Bahasa utama repo ini adalah **Bahasa Indonesia**, dengan istilah teknis dalam Bahasa Inggris di mana wajar.

## ✨ Kenapa repo ini ada?

Kebanyakan "AI assistant" hari ini hanyalah chatbot dengan system prompt. Muse Assistant mendefinisikan asisten secara utuh:

| Lapisan | Isi |
|---|---|
| 🧠 **Persona** | Kepribadian, nilai, dan gaya bicara — bukan sekadar instruksi |
| 🛠️ **Kemampuan** | 12+ kapabilitas inti: memori, browser, penjadwalan, artefak, sub-agen, dll. |
| 🔌 **Integrasi** | 20+ layanan: Gmail, Kalender, Spotify, Instagram, Meta Ads, pembayaran, dll. |
| 📦 **Skill** | Playbook markdown yang bisa dipasang-copot per tugas |
| 🛡️ **Keamanan** | Guardrail anti-phishing, privasi, dan batasan yang jelas |

## 📁 Struktur repo

```
muse-assistant/
├── README.md                  ← kamu di sini
├── LICENSE
├── runtime/                   ← ⭐ IMPLEMENTASI JALAN: agen Python + browser live
│   ├── agent.py               ← loop: pikir → tool → tuntas
│   ├── tools.py               ← web_search/fetch/browse, file, shell, memory, skills
│   ├── llm.py                 ← OpenAI-compatible (OpenAI/Ollama/vLLM/dll.)
│   ├── chat.py                ← CLI: python -m runtime.chat
│   └── ...
├── requirements.txt
├── docs/
│   ├── 01-persona.md          ← kepribadian & nilai inti
│   ├── 02-capabilities.md     ← semua kemampuan, dijelaskan satu per satu
│   ├── 03-integrations.md     ← katalog integrasi & cara menyambungkannya
│   ├── 04-architecture.md     ← cara kerja lapisan-lapisannya
│   ├── 05-safety.md           ← keamanan, privasi, dan batasan
│   └── 06-runtime.md          ← cara menjalankan runtime-nya
├── skills/
│   ├── _template/SKILL.md     ← template untuk bikin skill baru
│   ├── gmail/SKILL.md
│   ├── scheduler/SKILL.md
│   ├── researcher/SKILL.md
│   └── web-automation/SKILL.md
├── prompts/
│   └── system-prompt.md       ← template system prompt siap adaptasi
├── examples/
│   ├── morning-briefing.md    ← contoh: briefing pagi otomatis
│   └── deep-research.md       ← contoh: riset mendalam multi-sumber
└── tests/
    └── test_tools.py          ← 15 test tools non-network
```

## ⚡ Runtime: bikin LLM lain kerja kayak Muse

Repo ini sekarang punya **runtime Python yang benar-benar jalan** — bukan cuma dokumen.
LLM apa pun yang support OpenAI-compatible API (OpenAI, OpenRouter, Ollama lokal, vLLM)
bisa memakai: **browser Chromium live**, web search/fetch, file workspace, shell (opsional),
memori jangka panjang, dan semua skill di `skills/`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
export LLM_API_KEY="sk-..."   # atau Ollama lokal, lihat docs/06-runtime.md
python -m runtime.chat
```

Detail lengkap: [docs/06-runtime.md](docs/06-runtime.md).

## 🚀 Mulai cepat (baca dulu)

**1. Baca personanya dulu** — ini fondasinya:

```bash
cat docs/01-persona.md
```

**2. Pilih kemampuan yang kamu butuhkan** di `docs/02-capabilities.md`, lalu **integrasi** yang relevan di `docs/03-integrations.md`.

**3. Pasang skill** — setiap folder di `skills/` adalah playbook mandiri. Salin folder skill yang kamu mau ke proyek agen-mu, atau jadikan referensi saat menulis system prompt.

**4. Rakit system prompt** dari `prompts/system-prompt.md` — sesuaikan nama, bahasa, dan daftar skill yang aktif.

## 🧩 Filosofi desain

1. **Asisten, bukan chatbot.** Ia punya ingatan, inisiatif, dan tanggung jawab menyelesaikan tugas sampai tuntas — bukan sekadar menjawab.
2. **Persona sebelum tools.** Orang betah memakai asisten karena *caranya*, bukan karena banyaknya tombol. Kepribadian didefinisikan dulu, kemampuan mengikuti.
3. **Skill sebagai playbook, bukan plugin.** Setiap skill adalah file markdown berisi *cara* melakukan sesuatu — mudah dibaca manusia, mudah dimuat model.
4. **Due diligence default.** Setiap jawaban/tindakan melewati: apa yang belum pasti? Apa yang bisa berubah? Apa yang harus diverifikasi dulu?
5. **Privasi adalah fitur.** Data pengguna tidak pernah bocor lewat query, log, atau skill pihak ketiga. Prinsip *need-to-know* di semua lapisan.

## 🤝 Kontribusi

Punya ide skill baru, integrasi baru, atau perbaikan persona? Buka issue atau pull request. Baca `skills/_template/SKILL.md` sebelum menambah skill agar formatnya konsisten.

## 📄 Lisensi

MIT — bebas pakai, ubah, dan distribusikan. Lihat [LICENSE](LICENSE).
