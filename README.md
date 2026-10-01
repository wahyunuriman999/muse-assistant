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
├── docs/
│   ├── 01-persona.md          ← kepribadian & nilai inti
│   ├── 02-capabilities.md     ← semua kemampuan, dijelaskan satu per satu
│   ├── 03-integrations.md     ← katalog integrasi & cara menyambungkannya
│   ├── 04-architecture.md     ← cara kerja lapisan-lapisannya
│   └── 05-safety.md           ← keamanan, privasi, dan batasan
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
└── .github/
    └── workflows/ci.yml       ← cek markdown + struktur skill
```

## 🚀 Mulai cepat

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
