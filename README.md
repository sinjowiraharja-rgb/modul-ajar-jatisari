# Modul Ajar Jatisari

Aplikasi web untuk membuat Modul Ajar, RPP, Prota, Promes, dan LKPD bagi guru SD Negeri Jatisari. Dibangun dengan Python (Flask), dilengkapi integrasi AI Google Gemini Pro untuk generate konten otomatis, dan dapat mengekspor dokumen ke format Word (.docx) serta PDF (.pdf).

## Fitur Utama

- **Autentikasi**: Role Admin (Kepala Sekolah/Operator) dan Guru.
- **Profil Sekolah**: Kelompok data sekolah yang nanti otomatis terisi dalam modul.
- **Kelola Guru**: Admin dapat menambahkan, mengedit, dan menghapus akun guru.
- **Referensi Mata Pelajaran**: Kelola elemen dan capaian pembelajaran per fase/kelas/mapel.
- **Pembuatan Modul Ajar**:
  - Pilihan jenis dokumen: Modul Ajar, RPP, Prota, Promes, LKPD.
  - Pilihan pendekatan pembelajaran: **Deep Learning** atau **S.T.E.A.M**.
  - Checklist **8 Dimensi Profil Pelajar Pancasila**.
  - Generate konten otomatis dengan AI Google Gemini Pro.
- **Export**: Word (.docx) dan PDF (.pdf).

## Persyaratan Sistem

- Python 3.11 atau lebih baru
- Koneksi internet (untuk fitur AI)
- Akun Google Gemini Pro dan API Key-nya

## Instalasi Lokal

1. Clone atau ekstrak folder `modul-ajar-jatisari`.

2. Buka terminal / command prompt di dalam folder tersebut.

3. Buat virtual environment (direkomendasikan):

```bash
python -m venv venv
```

4. Aktifkan virtual environment:

- Windows:
```bash
venv\Scripts\activate
```

- Linux/macOS:
```bash
source venv/bin/activate
```

5. Instal dependencies:

```bash
pip install -r requirements.txt
```

6. Salin file environment:

```bash
cp .env.example .env
```

Kemudian edit file `.env` dan isi:

```env
GEMINI_API_KEY=API_KEY_GEMINI_ANDA
SECRET_KEY=buat_kunci_rahasia_yang_acak
FLASK_ENV=development
```

7. Jalankan aplikasi:

```bash
python run.py
```

8. Buka browser dan akses: `http://127.0.0.1:5000`

9. Login dengan akun default:

- Username: `admin`
- Password: `admin123`

## Mendapatkan API Key Google Gemini Pro

1. Buka [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Login dengan akun Google Anda.
3. Klik **Create API Key**.
4. Salin API Key ke file `.env` pada variabel `GEMINI_API_KEY`.
5. Restart aplikasi.

## Struktur Dokumen Modul Ajar

Dokumen modul ajar yang dihasilkan mengikuti format baku:

### A. Informasi Umum
- Identitas Modul
- Kompetensi Awal
- Profil Pelajar Pancasila

### B. Komponen Inti
- Tujuan Pembelajaran
- Pemahaman Bermakna
- Pertanyaan Pemantik
- Persiapan Pembelajaran
- Langkah-langkah Pembelajaran (Deep Learning / S.T.E.A.M)
- Asesmen
- Pengayaan & Remedial

### C. Lampiran
- Lembar Kerja Peserta Didik (LKPD)
- Bahan Bacaan Guru dan Murid
- Glosarium
- Daftar Pustaka

## Deployment Online Gratis (Render.com)

1. Daftar akun di [Render](https://render.com/).
2. Buat **New Web Service**.
3. Hubungkan repository GitHub atau upload manual.
4. Isi konfigurasi:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Tambahkan Environment Variables:
   - `GEMINI_API_KEY`
   - `SECRET_KEY`
   - `FLASK_ENV=production`
6. Klik **Deploy**.

> Catatan: Pada layanan gratis, server akan "sleep" jika tidak aktif dalam beberapa menit. Akses pertama setelah sleep mungkin membutuhkan waktu beberapa detik.

## Lisensi

Aplikasi ini dibuat khusus untuk **SD Negeri Jatisari**. Silakan modifikasi sesuai kebutuhan sekolah.

## Dukungan

Jika menemukan kendala, silakan periksa:
- API Key Gemini sudah benar dan masih aktif.
- File `.env` sudah dibuat di folder root aplikasi.
- Folder `data/` memiliki izin tulis.
