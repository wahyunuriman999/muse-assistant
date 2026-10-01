# 03 — Integrasi: Layanan Apa Saja yang Tersambung?

Setiap integrasi di bawah adalah **skill**: playbook mandiri berisi cara autentikasi, operasi yang didukung, dan batasannya. Pola umumnya sama — baca `skills/_template/SKILL.md` sebelum menambah yang baru.

> Catatan: daftar ini adalah *katalog referensi*. Implementasi nyata butuh kredensial/OAuth masing-masing layanan dan mengikuti syarat layanannya.

## Komunikasi & produktivitas

| Layanan | Kemampuan |
|---|---|
| **Gmail** | Cari, baca thread, tulis/kirim/balas/teruskan email, kelola label, buka lampiran, unsubscribe milis |
| **Google Calendar** | Lihat agenda, detail acara, buat/ubah/hapus jadwal |
| **Messenger** | Baca & cari percakapan/kontak, kirim/react/edit pesan, riwayat panggilan |
| **WhatsApp** | Side chat & koneksi chat (tergantung dukungan provider) |

## Media sosial & iklan

| Layanan | Kemampuan |
|---|---|
| **Instagram** | Baca profil/postingan/komentar/story/feed/saved, insight akun, terbitkan postingan/reel/story/carousel |
| **Threads** | Profil, postingan, feed, tren, pencarian, terbitkan postingan |
| **Facebook** | Postingan, grup, acara, Marketplace listing (baca & kelola milik sendiri) |
| **Meta Ads** | Kampanye, ad set, iklan, anggaran, laporan, audience, katalog produk, kebijakan iklan |

## Musik, kesehatan & keuangan

| Layanan | Kemampuan |
|---|---|
| **Spotify** | Cari musik/podcast, kelola playlist |
| **Apple HealthKit** | Metrik harian (langkah, jarak, kalori, detak jantung, HRV, VO2max), sesi tidur, workout |
| **Google Health Connect** | Sama seperti HealthKit, dari perangkat Android |
| **Plaid** | Saldo, transaksi, recurring, liabilitas, dan investasi dari rekening bank tertaut |

## Informasi & utilitas

| Layanan | Kemampuan |
|---|---|
| **FlightAware** | Status penerbangan spesifik: jadwal, delay, pembatalan (terverifikasi, bukan dari ingatan) |
| **Pencarian produk** | Temukan & bandingkan produk nyata: harga, gambar, URL halaman produk |
| **Pencarian tempat** | Restoran/toko/POI dengan peta, jam operasional terverifikasi |
| **Pencarian gambar** | URL gambar + halaman sumber dari query teks |
| **Media library** | Cari & periksa galeri foto pengguna untuk personalisasi |

## Pembayaran

| Layanan | Kemampuan |
|---|---|
| **Wallet (Shop Pay / Stripe Link)** | Cek status koneksi, ambil metode pembayaran & alamat tersimpan |
| **Checkout via browser** | Eksekusi pembelian dengan persetujuan eksplisit di setiap langkah |

Aturan pembayaran: agen mengoordinasikan pilihan & review, skill transaksi menentukan rute eksekusi, dan browser mengeksekusi di bawah persetujuan yang dipersyaratkan. Tidak ada pembelian diam-diam.

## Kreasi media

| Layanan | Kemampuan |
|---|---|
| **Text-to-speech (TTS)** | Ubah teks menjadi audio, satu/multi speaker |
| **Podcast generator** | Rangkai episode/briefing/narasi menjadi MP3 |
| **Image & video gen** | Buat/edit gambar dan video lewat pipeline media |

## Pola integrasi yang dipakai

1. **Status dulu, janji kemudian.** Sebelum menjanjikan sesuatu yang butuh layanan tersambung, cek status koneksinya. Kalau belum tersambung, kirim link koneksi — jangan berandai-andai.
2. **Skill dulu, akal-akalan kemudian.** Selalu cari skill yang relevan sebelum web scraping/manual. Skill membawa instruksi domain yang spesifik.
3. **Batasan layanan dihormati.** Rate limit (429), blokir akses (403), atau penolakan provider = berhenti di scope itu. Tidak memutar lewat endpoint lain, tidak retry diam-diam.
4. **Kredensial tidak pernah lewat chat.** Password/API key masuk lewat alur aman (vault/OAuth). Kode OTP satu-kali hanya dipakai untuk langkah yang memintanya, tidak disimpan.
5. **Data minimal.** Setiap panggilan ke layanan luar hanya membawa data yang dibutuhkan tugas itu — tidak lebih.
