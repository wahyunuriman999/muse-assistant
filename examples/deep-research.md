# Contoh: Deep Research Multi-Sumber

Skenario: pengguna minta investigasi mendalam tentang suatu topik.

## Alur kerja

### 1. Rumuskan & bagi
Ubah permintaan menjadi 3–5 sub-pertanyaan independen:

```
Topik: "Apakah langganan X worth it dibanding kompetitor?"
├─ Harga & paket tiap layanan (sumber: situs resmi)
├─ Fitur pembeda (sumber: dokumentasi & review)
├─ Pengalaman pengguna nyata (sumber: forum/komunitas)
└─ Biaya tersembunyi & syarat batal (sumber: ToS)
```

### 2. Delegasikan yang paralel
Sub-pertanyaan independen dikerjakan sub-agen secara paralel; yang dependen dikerjakan berurutan.

### 3. Triangulasi & susun
- Klaim penting: minimal 2 sumber independen.
- Pisahkan: **fakta** (dengan sumber + tanggal) vs **opini** vs **perkiraan**.
- Akhiri dengan: rekomendasi + "yang masih belum pasti".

## Template laporan

```markdown
## Ringkasan (3 baris)

## Temuan
1. ... — [sumber, tanggal]

## Perbandingan (tabel jika cocok)

## Ketidakpastian
- ...

## Rekomendasi
...
```

## Pelajaran desain

- **Paralelisasi** memangkas waktu riset drastis — tapi verifikasi akhirnya tetap di satu tempat.
- **Stempel tanggal** pada sumber lebih penting dari tanggal pencarian.
- Mengakui kebuntuan ("data 2026 belum tersedia publik") membangun kepercayaan, bukan menguranginya.
