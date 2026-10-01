# Contoh: Morning Briefing Otomatis

Skenario: setiap hari kerja jam 07:00, asisten mengirim briefing pagi ke chat utama.

## Setup (sekali saja)

Buat cron harian dengan instruksi mandiri berikut:

> Setiap hari kerja pukul 07:00 Asia/Jakarta:
> 1. Baca kalender hari ini (acara, waktu, lokasi, peserta).
> 2. Cek prakiraan cuaca kota pengguna untuk hari ini.
> 3. Cari 3 berita teratas yang relevan dengan minat pengguna (teknologi, data, lowongan analis data).
> 4. Susun briefing ≤ 15 baris: sapaan singkat, agenda hari ini, cuaca + saran pakaian/perjalanan, 3 berita (1 baris + link tiap berita).
> 5. Kirim ke chat utama. Jika kalender kosong, tetap kirim versi ringkas — jangan diam.

## Hasil yang diharapkan

```
Pagi! Ini rencanamu hari ini, Kamis:
• 09:00 — Standup tim (online)
• 14:00 — Interview user (kantor, bawa laptop)

Cuaca: 31°C, hujan ringan sore — bawa payung kalau keluar setelah jam 15.

Berita pilihan:
• ... (link)
• ... (link)
• ... (link)
```

## Pelajaran desain

- **Instruksi mandiri:** cron tidak melihat chat — semua konteks (kota, minat, format) tertulis di instruksinya.
- **Kondisi selesai implisit:** berjalan terus sampai pengguna bilang berhenti.
- **Diam itu opsi:** untuk job pemantauan (bukan briefing yang diminta), hasil "tidak ada perubahan" = tidak mengirim apa-apa.
