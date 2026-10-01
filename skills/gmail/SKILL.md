# Gmail

> Mengelola email pengguna: mencari, membaca, menulis, mengirim, dan merapikan inbox.

## Kapan dipakai

- Pengguna bertanya tentang isi email ("ada email dari X?", "ringkas thread ini")
- Pengguna minta kirim/balas/teruskan email
- Pengguna minta unsubscribe milis atau merapikan label

## Kapan TIDAK dipakai

- Butuh jadwal/acara → skill `scheduler` / kalender
- Butuh file dari Drive → integrasi penyimpanan file

## Prasyarat

- Autentikasi: OAuth akun Google pengguna
- Cek status koneksi dulu; kalau belum tersambung, kirim link koneksi dan berhenti — jangan berandai-andai

## Langkah kerja

1. **Cari dulu, baca kemudian.** Gunakan pencarian (dari, subjek, rentang tanggal) untuk menemukan thread, baru baca isinya.
2. **Draf sebelum kirim.** Tulis draf, tunjukkan ke pengguna untuk review. Kirim hanya setelah persetujuan eksplisit — atau jika pengguna sudah memintanya secara eksplisit.
3. **Lampiran:** baca/ekstrak hanya yang dibutuhkan tugas.
4. **Unsubscribe/bersih-bersih:** konfirmasi daftar milis/label yang akan diubah sebelum eksekusi massal.

## Batasan & edge case

- Jangan menebak alamat email — salin persis dari hasil pencarian/kontak.
- Email sensitif (keuangan, medis, hukum): ringkas dengan hati-hati, jangan forward tanpa izin.
- Kegagalan kirim: laporkan pesan error dengan bahasa sederhana + langkah berikutnya.

## Contoh pemakaian

```
Pengguna: "Tolong ringkas email dari HRD minggu ini"
Asisten: (cari dari:hrd rentang 7 hari → baca 3 thread → ringkasan 5 baris + tenggat yang disebut)
```
