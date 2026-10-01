# 02 — Kemampuan: Apa Saja yang Bisa Dilakukannya?

Daftar ini adalah *spesifikasi kemampuan* — setiap butir bisa dipetakan ke tool, skill, atau workflow nyata. Tandai mana yang kamu implementasikan di `prompts/system-prompt.md`.

## 1. Percakapan & penalaran
- Memahami konteks panjang, mengingat preferensi, dan menyesuaikan gaya bicara.
- Menjawab dalam bahasa pengguna, dengan kedalaman yang pas.
- Memberi pendapat saat diminta — tidak netral-netral saja.

## 2. Ingatan jangka panjang (Memory)
- Menyimpan fakta tahan lama: siapa pengguna, apa yang ia pedulikan, keputusan, komitmen.
- Ingatan ditulis *sebelum* menjawab, dalam bahasa ringkas untuk "percakapan berikutnya".
- Selalu mencari ingatan dulu sebelum bertindak/merekomendasikan — bahkan untuk pertanyaan yang terlihat generik.
- Menghormati permintaan "lupakan ini" dan merekonsiliasi fakta yang berubah (jadwal ulang, preferensi baru).

## 3. Komputer pribadi (Terminal & file)
- Shell Linux, baca/tulis/edit file, cari di filesystem.
- Menjalankan program, mengelola proses background, dan membangun software.
- Aturan: file tahan lama di home/workspace; `/tmp` hanya untuk scratch.

## 4. Browser nyata (Live browser)
- Chromium sungguhan: membuka situs, login, mengisi form, menangani JavaScript.
- Riset web mendalam dengan sumber terverifikasi (bukan sekadar snippet).
- Membedakan *teks yang di-fetch* (bukan kunjungan) vs *tugas browser langsung* untuk verifikasi live (harga, ketersediaan, status akun).
- Menangani CAPTCHA sesuai preferensi pengguna; tidak mem-bypass pengaman dengan cara curang.

## 5. Penjadwalan & otomatisasi (Background work)
- **Cron:** tugas terjadwal — pengingat, cek berkala, laporan rutin.
- **Hook:** pemicu berbasis kejadian, bukan jam.
- **Service:** program yang jalan terus (listener, kolektor data).
- Setiap job punya pemilik, kondisi selesai, dan tujuan pengiriman hasil.

## 6. Sub-agen & delegasi
- Mendelegasikan pekerjaan panjang/multi-langkah ke sub-agen yang berjalan di background.
- Koordinator bisa mem-fan-out ke banyak sub-agen untuk tugas paralel.
- Hasil delegasi diverifikasi dengan ketelitian yang sama seperti kerja sendiri.

## 7. Artefak (Dokumen, aplikasi, media)
- Membangun dokumen, spreadsheet, presentasi, halaman/aplikasi web, gambar, audio, video.
- Artefak diantar *di pesan yang sama* saat diumumkan jadi — pengguna tidak disuruh mencari.
- File untuk pengguna tinggal di folder yang memang untuk mereka, bukan tercampur file kerja internal.

## 8. UI interaktif di chat (Widget)
- Kartu interaktif: pilihan jawaban sekali ketuk, peta, visualisasi data, pratinjau.
- Satu widget per pesan; dipakai saat memperkaya, bukan menggantikan teks.

## 9. Feed & ide proaktif
- **Feed:** "koran pribadi" — tulisan editorial terjadwal sesuai prompt pengguna.
- **Ide:** kartu saran yang bisa dijalankan/ditolak pengguna.
- Proaktif hanya untuk info yang *benar-benar baru dan layak menginterupsi*; selebihnya diam.

## 10. Goals & tracking
- Tujuan tahan lama (mis. "cari kerja", "lancar lari 10K") dengan workspace sendiri.
- Komitmen konkret (reservasi, pengiriman, janji) dilacak sampai hasilnya jelas, lalu ditutup.

## 11. Perangkat pengguna (Devices)
- Perintah ke perangkat yang dipasangkan (mis. ponsel): baca pesan, kelola notifikasi.
- Akses minimal sesuai tugas; tidak mengintai.

## 12. Pencarian cerdas (Skills vertikal)
- **Produk/belanja:** cari, bandingkan, evaluasi produk nyata dengan harga & URL.
- **Tempat:** restoran, toko, POI — dengan peta dan jam operasional terverifikasi.
- **Gambar:** pencarian gambar berbasis teks untuk referensi visual.
- **Penerbangan:** status, delay, dan jadwal penerbangan spesifik yang terverifikasi.

## 13. Komunikasi
- Telepon, SMS, dan notifikasi ke pengguna; pesan ke chat lain/grup.
- Side chat: thread terpisah dengan konteks sendiri untuk topik yang butuh ruang.

## Cara memetakan ke implementasi

| Kemampuan | Implementasi tipikal |
|---|---|
| 1–2 | System prompt + memory store (file/DB) |
| 3 | Sandbox VM / container dengan shell |
| 4 | Headless Chromium + session persistence |
| 5 | Cron/hook runner + job store |
| 6 | Agent orchestrator (spawn, message passing) |
| 7 | Builder tools + file hosting |
| 8 | Rich message renderer |
| 9–10 | Scheduler + editorial pipeline |
| 11 | Device pairing (push channel) |
| 12–13 | Konektor & skill per layanan |

Tidak semua harus dibangun sekaligus. Mulai dari 1–3, tambah sisanya sesuai kebutuhan — arsitekturnya di `docs/04-architecture.md`.
