# Web Automation

> Mengoperasikan browser nyata: membuka situs, login, mengisi form, dan verifikasi live.

## Kapan dipakai

- Pengguna minta "buka/kunjungi situs ini", isi form, atau lakukan alur multi-langkah di website
- Butuh verifikasi live: harga saat ini, ketersediaan slot, status akun/pesanan, jam operasional

## Kapan TIDAK dipakai

- Informasi yang cukup dari teks halaman → cukup fetch teks biasa
- Riset multi-sumber → skill `researcher`

## Prasyarat

- Tugas mandiri: tujuan, pilihan yang sudah pasti, batasan, dan kriteria sukses
- Login: coba sesi tersimpan dulu; minta bantuan pengguna hanya jika dibutuhkan (takeover/manual)

## Langkah kerja

1. **Beri tugas yang mandiri** — browser tidak melihat chat ini. Sertakan: hasil yang diminta, tanggal/zona waktu, jumlah/varian, dan apa yang membuktikan sukses.
2. **Bedakan tahapnya** — cek/harga (aman) vs siapkan vs komitmen (booking/beli). Jangan lewati tahap tanpa izin.
3. **Verifikasi di sumbernya** — untuk tanggal, zona waktu, lokasi, jumlah, dan total biaya *termasuk* pajak/fee.
4. **Laporkan jujur** — apa yang dicek, sumbernya, dan apa yang belum terverifikasi. "Tidak ditemukan" dari satu pencarian ≠ tidak ada.

## Batasan & edge case

- CAPTCHA: ikuti preferensi pengguna (selesaikan sendiri / serahkan ke pengguna / tanya dulu). Bukan izin untuk tugas baru.
- Rate limit/blokir situs: berhenti, jelaskan, tawarkan alternatif yang tidak memutar blokir.
- Kredensial: lewat alur aman; kode OTP hanya untuk langkah yang memintanya.

## Contoh pemakaian

```
Pengguna: "Cek harga tiket kereta Jakarta–Bandung buat Sabtu depan"
Asisten: (tugas browser: cek situs resmi, tanggal X, 2 penumpang → laporkan harga + jam + sumber)
```
