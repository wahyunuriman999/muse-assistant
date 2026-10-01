# Scheduler

> Pekerjaan terjadwal & otomatis: pengingat, cek berkala, laporan rutin, dan pemicu kejadian.

## Kapan dipakai

- "Ingatkan aku tiap...", "cek ... setiap pagi", "kirimi laporan mingguan"
- Tugas yang harus jalan saat pengguna tidak ada

## Kapan TIDAK dipakai

- Tugas satu-kali yang langsung dikerjakan → kerjakan sekarang, tanpa job

## Prasyarat

- Tiga hal wajib sebelum membuat job: **pemilik** (goal/chat asal), **kondisi selesai**, **tujuan pengiriman hasil**
- Zona waktu pengguna untuk penjadwalan yang akurat

## Langkah kerja

1. **Tentukan jenisnya:**
   - `cron` — berbasis jam (pengingat, laporan rutin)
   - `hook` — berbasis kejadian (ada email baru dari X, harga berubah)
   - `service` — jalan terus (listener, kolektor)
2. **Tulis instruksi lengkap** — job harus bisa jalan tanpa konteks chat: apa yang dicek, dari sumber mana, format hasil.
3. **Tulis batasan pengguna** ke dalam instruksi job (frekuensi, jam tenang, kondisi berhenti).
4. **Verifikasi setelah dibuat** — baca kembali job yang tersimpan sebelum bilang "sudah dijadwalkan".
5. **Lapor dengan bijak** — hasil yang diminta pengguna selalu diantar; hasil rutin yang tidak berubah → diam.

## Batasan & edge case

- Satu "ya" untuk tugas satu-kali = SATU job sekali jalan. Menjadikannya rutin butuh persetujuan baru yang menyebut jadwalnya.
- Job yang error: perbaiki dalam scope-nya; kalau tidak bisa, matikan dan lapor — jangan biarkan mengirim laporan rusak.
- Jadwal itu bukan bukti eksekusi. Verifikasi pengiriman nyata saat penting.

## Contoh pemakaian

```
Pengguna: "Ingatkan aku minum obat tiap jam 8 pagi"
Asisten: (buat cron harian 08:00 Asia/Jakarta → verifikasi tersimpan → "Siap, aku ingatkan tiap jam 8 pagi.")
```
