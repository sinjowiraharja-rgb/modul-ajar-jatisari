"""
Script sederhana untuk menguji fungsi-fungsi dasar aplikasi Modul Ajar Jatisari.
"""
import os
import sys

# Inisialisasi database
from database import init_db, get_user_by_username, list_modul, create_modul
from docx_generator import generate_docx
from pdf_generator import generate_pdf

init_db()
print("[OK] Database diinisialisasi.")

# Cek user admin default
admin = get_user_by_username('admin')
if admin:
    print("[OK] User admin ditemukan: {} ({})".format(admin['nama_lengkap'], admin['role']))
else:
    print("[ERROR] User admin tidak ditemukan!")
    sys.exit(1)

# Buat modul uji
sample_modul = {
    'user_id': admin['id'],
    'jenis_dokumen': 'Modul Ajar',
    'nama_guru': 'Budi Santoso, S.Pd.',
    'nama_kepala_sekolah': 'Dra. Siti Aminah',
    'nama_sekolah': 'SD Negeri Jatisari',
    'fase': 'B',
    'kelas': '4',
    'mapel': 'Ilmu Pengetahuan Alam',
    'topik': 'Perkembangan Hewan',
    'alokasi_waktu': '2 x 35 menit',
    'minggu_pelaksanaan': 'Minggu ke-3',
    'kompetensi_awal': 'Siswa sudah mengenal ciri-ciri hewan.',
    'dimensi_pancasila': 'Bernalar Kritis, Mandiri, Bergotong Royong',
    'pendekatan': 'deep_learning',
    'sarana_prasarana': 'Gambar hewan, video perkembangan hewan, dan lembar kerja.',
    'target_peserta_didik': 'Siswa reguler kelas 4.',
    'model_pembelajaran': 'Tatap Muka',
    'tujuan_pembelajaran': 'Siswa mampu menjelaskan proses perkembangan hewan secara sederhana.',
    'pemahaman_bermakna': 'Memahami daur hidup membantu kita menghargai keberagaman makhluk hidup.',
    'pertanyaan_pemantik': 'Bagaimana seekor kupu-kupu bereproduksi?',
    'persiapan_pembelajaran': 'Menyiapkan media gambar dan video perkembangan hewan.',
    'langkah_pembelajaran': '1. Koneksi: Menanyakan pengalaman siswa melihat hewan.\n2. Obsesi: Menayangkan video perkembangan hewan.\n3. Refleksi: Siswa berdiskusi tentang perubahan bentuk hewan.\n4. Aktivasi: Siswa membuat poster daur hidup hewan.',
    'asesmen': 'Observasi lembar kerja dan penilaian poster.',
    'pengayaan': 'Siswa mencari contoh hewan yang mengalami metamorfosis sempurna.',
    'remedial': 'Guru memberikan penjelasan tambahan secara individu.',
    'lkpd': 'Lembar Kerja: Mengurutkan tahap daur hidup kupu-kupu.',
    'bahan_bacaan': 'Buku IPA Kelas 4.',
    'glosarium': 'Metamorfosis = perubahan bentuk hewan.',
    'daftar_pustaka': 'Kemendikbudristek. (2022). Buku IPA Kelas 4.'
}

modul_id = create_modul(sample_modul)
print("[OK] Modul uji dibuat dengan ID: {}".format(modul_id))

# Update with modul_id for exports if needed
sample_modul['id'] = modul_id

# Test export Word
output_docx = os.path.join('data', 'test_modul.docx')
generate_docx(sample_modul, output_docx)
print("[OK] File Word dibuat: {} ({} bytes)".format(output_docx, os.path.getsize(output_docx)))

# Test export PDF
output_pdf = os.path.join('data', 'test_modul.pdf')
pdf_result = generate_pdf(sample_modul, output_pdf)
if pdf_result and os.path.exists(output_pdf):
    print("[OK] File PDF dibuat: {} ({} bytes)".format(output_pdf, os.path.getsize(output_pdf)))
else:
    print("[WARNING] PDF tidak dapat dibuat. WeasyPrint membutuhkan GTK di Windows, tapi Word sudah berhasil dibuat.")

# Summary
print("\n=== RINGKASAN TEST ===")
print("User admin: admin / admin123")
print("Total modul di database: {}".format(len(list_modul(role='admin'))))
print("Aplikasi siap dijalankan dengan: python run.py")
