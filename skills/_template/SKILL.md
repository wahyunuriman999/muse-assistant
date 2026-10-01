# Template Skill

Salin folder ini sebagai `skills/<nama-skill/` dan isi bagian-bagiannya. Satu skill = satu tugas yang jelas.

---

# Nama Skill

> Satu kalimat: apa yang dilakukan skill ini dan kapan dipakai.

## Kapan dipakai

- Kondisi 1 → pakai skill ini
- Kondisi 2 → pakai skill ini

## Kapan TIDAK dipakai

- Kondisi lain → pakai skill `<nama-skill-lain>` sebagai gantinya

## Prasyarat

- Autentikasi: (OAuth / API key / tidak perlu)
- Akses/izin yang dibutuhkan
- Cara cek status koneksi sebelum mulai

## Langkah kerja

1. **Verifikasi prasyarat** — jangan berjanji sebelum status koneksi jelas.
2. **Kumpulkan input** — apa yang harus diketahui sebelum bertindak (tanggal, jumlah, akun, dsb.).
3. **Eksekusi** — urutan operasi yang aman (baca dulu, tulis kemudian).
4. **Konfirmasi** — untuk aksi yang sulit dibatalkan: tunjukkan ringkasan, minta persetujuan eksplisit, baru jalankan.
5. **Laporkan** — hasil, bukti (ID/timestamp), dan apa yang belum terverifikasi.

## Batasan & edge case

- Rate limit: berhenti saat 429, jangan memutar lewat jalur lain.
- Kegagalan parsial: laporkan bagian yang berhasil & gagal secara terpisah.
- Data sensitif: hanya bawa yang dibutuhkan (prinsip need-to-know).

## Contoh pemakaian

```
Pengguna: "..."
Asisten: (langkah 1–5 di atas, ringkas)
```
