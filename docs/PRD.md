# PRD: Modul Ajar Jatisari

## 1. Informasi Produk

| Item | Keterangan |
|------|------------|
| Nama Aplikasi | Modul Ajar Jatisari |
| Pemilik | SD Negeri Jatisari |
| Pengguna Utama | Kepala Sekolah/Operator (Admin) dan Guru SD kelas 1-6 |
| Platform | Web App (Flask + Python) |
| Hosting | Online gratis (disarankan Render.com free tier) |
| Integrasi AI | Google Gemini Pro (API Key milik sekolah) |
| Bahasa | Indonesia |

## 2. Tujuan Produk

Membantu guru SD Negeri Jatisari menyusun administrasi pembelajaran Kurikulum Merdeka secara cepat, rapi, dan konsisten, dengan pilihan pendekatan pembelajaran **Deep Learning** atau **S.T.E.A.M**, serta memanfaatkan AI Google Gemini Pro untuk generate konten otomatis.

## 3. Jenis Dokumen yang Dapat Dibuat

1. Modul Ajar Kurikulum Merdeka (format utama)
2. RPP (Rencana Pelaksanaan Pembelajaran)
3. Prota (Program Tahunan)
4. Promes (Program Semester)
5. LKPD (Lembar Kerja Peserta Didik)

## 4. Struktur Dokumen Modul Ajar

Aplikasi menghasilkan modul ajar sesuai format baku berikut:

### A. Informasi Umum
- Identitas Modul:
  - Nama Penyusun (Guru)
  - Nama Kepala Sekolah
  - Satuan Pendidikan
  - Fase/Kelas
  - Mata Pelajaran
  - Alokasi Waktu
- Kompetensi Awal
- Profil Pelajar Pancasila (maksimal 8 dimensi, checklist)

### B. Komponen Inti
- Tujuan Pembelajaran
- Pemahaman Bermakna
- Pertanyaan Pemantik
- Persiapan Pembelajaran (media, asesmen awal)
- Langkah-langkah Pembelajaran berdasarkan pilihan pendekatan:
  - **Deep Learning**:
    - Koneksi (Connection)
    - Pengamatan obsesi (Obsession)
    - Berkaca diri (Reflection)
    - Perluasan idea (Expansion)
    -尼斯 (Refinement)
    - Aktivasi (Activation)
  - **S.T.E.A.M**:
    - Science
    - Technology
    - Engineering
    - Arts
    - Mathematics
- Asesmen (rubrik, instrumen, pedoman penskoran)
- Pengayaan & Remedial

### C. Lampiran
- Lembar Kerja Peserta Didik (LKPD)
- Bahan Bacaan Guru dan Murid
- Glosarium
- Daftar Pustaka

## 5. Dimensi Profil Pelajar Pancasila

Aplikasi menyediakan checklist 8 dimensi yang dapat dipilih guru:

1. Beriman, Bertakwa kepada Tuhan Yang Maha Esa, dan Berakhlak Mulia
2. Mandiri
3. Bergotong Royong
4. Kreatif
5. Berkebhinekaan Global
6. Bernalar Kritis
7. Bernalar Kreatif
8. Berkebinekaan (Sesuai KI-KD terbaru)

## 6. Pilihan Pendekatan Pembelajaran

Saat membuat modul ajar, guru memilih salah satu pendekatan:

- **Deep Learning**: Fokus pada pemahaman mendalam, refleksi, koneksi antar konsep, dan aktivasi pengetahuan.
- **S.T.E.A.M**: Fokus pada integrasi ilmu pengetahuan, teknologi, teknik, seni, dan matematika dalam satu project-based learning.

AI akan menyusun langkah-langkah pembelajaran sesuai pendekatan yang dipilih.

## 7. Alur Penggunaan

### Admin
1. Login ke dashboard Admin.
2. Mengisi profil sekolah: nama sekolah, NPSN, alamat, nama kepala sekolah, semester, tahun ajaran.
3. Mengelola data guru: tambah, edit, hapus.
4. Mengelola referensi: mata pelajaran, fase/kelas, elemen, capaian pembelajaran.
5. Melihat rekapan modul ajar yang telah dibuat guru.

### Guru
1. Login menggunakan akun yang dibuatkan admin.
2. Memilih jenis dokumen yang ingin dibuat.
3. Mengisi form input modul ajar.
4. Memilih pendekatan: Deep Learning atau S.T.E.A.M.
5. Memilih dimensi Profil Pelajar Pancasila.
6. Klik "Generate dengan AI".
7. Mereview preview hasil generate.
8. Mengedit hasil jika diperlukan.
9. Export ke Word (.docx) dan PDF (.pdf).
10. Menyimpan dan mengelola riwayat modul ajar.

## 8. Form Input Modul Ajar

### Identitas Modul
- Nama Penyusun (auto-fill dari nama guru login)
- Nama Kepala Sekolah (auto-fill dari profil sekolah)
- Satuan Pendidikan (auto-fill)
- Fase/Kelas (pilihan)
- Mata Pelajaran (pilihan)
- Materi/Topik
- Alokasi Waktu
- Bulan/Minggu Pelaksanaan
- Elemen/Capaian Pembelajaran

### Konten
- Kompetensi Awal
- Profil Pelajar Pancasila (checkbox 8 dimensi)
- Pendekatan (radio: Deep Learning / S.T.E.A.M)
- Sarana/Prasarana
- Target Peserta Didik
- Model Pembelajaran (Tatap Muka / Daring / Campuran)

### Output Generate AI
- Tujuan Pembelajaran
- Pemahaman Bermakna
- Pertanyaan Pemantik
- Persiapan Pembelajaran
- Langkah-langkah Pembelajaran sesuai pendekatan
- Asesmen
- Pengayaan & Remedial
- LKPD
- Bahan Bacaan Guru & Murid
- Glosarium
- Daftar Pustaka

## 9. Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python 3.11+ dengan Flask |
| Frontend | HTML, Bootstrap 5, JavaScript |
| Database | SQLite |
| AI | Google Gemini Pro via `google-generativeai` |
| Export Word | `python-docx` |
| Export PDF | `docx2pdf` di Windows, `LibreOffice headless` di Linux (Render), atau fallback HTML to PDF |
| Hosting gratis | Render.com free tier |

## 10. Keamanan

- Sistem login menggunakan session Flask.
- Password di-hash dengan Werkzeug.
- API Key Gemini disimpan di environment variable (`.env`), bukan di kode.
- Admin memiliki akses penuh, guru hanya bisa mengakses modul miliknya.

## 11. Panduan Konfigurasi API Key Gemini

1. Buka https://aistudio.google.com/app/apikey
2. Login dengan akun Google yang memiliki Gemini Pro.
3. Buat API Key baru.
4. Salin API Key ke file `.env` pada baris: `GEMINI_API_KEY=isi_api_key_di_sini`
5. Restart aplikasi.

## 12. Daftar Pengguna Awal (Seed Data)

Aplikasi akan otomatis membuat akun admin default saat pertama kali dijalankan:
- Username: `admin`
- Password: `admin123`

Disarankan untuk mengganti password admin segera setelah login pertama.

## 13. Deployment Online Gratis

Rekomendasi utama: **Render.com**.
- Free tier dengan auto-sleep setelah periode tidak aktif.
- Dukungan deploy langsung dari GitHub atau upload manual.
- Alternatif: PythonAnywhere free tier.

## 14. Catatan Penting

- Aplikasi ini berjalan membutuhkan koneksi internet untuk fitur generate AI.
- Export PDF membutuhkan konversi dari Word ke PDF; di Windows menggunakan docx2pdf, di server Linux menggunakan LibreOffice.
- Semua data disimpan di SQLite, file database bernama `data/modul_ajar.db`.
