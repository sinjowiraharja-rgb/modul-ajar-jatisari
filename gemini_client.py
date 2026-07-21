import json
import os
import google.generativeai as genai
from config import GEMINI_API_KEY


def configure_gemini():
    """Konfigurasi API key Gemini."""
    if not GEMINI_API_KEY:
        return False
    genai.configure(api_key=GEMINI_API_KEY)
    return True


def get_model():
    """Pilih model Gemini yang tersedia."""
    model_names = ["gemini-1.5-pro", "gemini-1.5-pro-latest", "gemini-pro"]
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            return model
        except Exception:
            continue
    return genai.GenerativeModel("gemini-1.5-pro")


def generate_modul_content(inputs):
    """
    Generate konten modul ajar menggunakan Gemini Pro.

    inputs: dict berisi semua data form input.
    Returns: dict dengan hasil generate AI, atau None jika gagal.
    """
    if not configure_gemini():
        return None

    model = get_model()

    dimensi = inputs.get('dimensi_pancasila', [])
    if isinstance(dimensi, str):
        dimensi = [d.strip() for d in dimensi.split(',') if d.strip()]

    pendekatan = inputs.get('pendekatan', 'deep_learning')
    pendekatan_label = 'Deep Learning' if pendekatan == 'deep_learning' else 'S.T.E.A.M'

    prompt = f"""
Kamu adalah asisten ahli Kurikulum Merdeka untuk SD di Indonesia. Susunlah komponen pembelajaran yang lengkap, rapi, dan sesuai struktur Modul Ajar Kurikulum Merdeka dengan pendekatan {pendekatan_label}.

Berikut data yang dimasukkan guru:
- Jenis Dokumen: {inputs.get('jenis_dokumen', 'Modul Ajar')}
- Satuan Pendidikan: {inputs.get('nama_sekolah', 'SD Negeri Jatisari')}
- Fase/Kelas: {inputs.get('fase', '')} / {inputs.get('kelas', '')}
- Mata Pelajaran: {inputs.get('mapel', '')}
- Topik/Materi: {inputs.get('topik', '')}
- Alokasi Waktu: {inputs.get('alokasi_waktu', '')}
- Model Pembelajaran: {inputs.get('model_pembelajaran', 'Tatap Muka')}
- Kompetensi Awal: {inputs.get('kompetensi_awal', '')}
- Dimensi Profil Pelajar Pancasila: {', '.join(dimensi) if dimensi else 'Tidak spesifik'}
- Sarana/Prasarana: {inputs.get('sarana_prasarana', '')}
- Target Peserta Didik: {inputs.get('target_peserta_didik', '')}

Jika pendekatannya Deep Learning, susun langkah pembelajaran dengan tahapan:
1. Membuat koneksi
2. Mengamati dengan penuh obsesi/mata heran
3. Merefleksikan/berkaca diri
4. Memperluas ide
5. Menyempurnakan ide
6. Mengaktivasi pengetahuan

Jika pendekatannya S.T.E.A.M, susun langkah pembelajaran yang mengintegrasikan:
- Science
- Technology
- Engineering
- Arts
- Mathematics
dalam satu project/tugas terpadu.

HASILKAN dalam format JSON murni, tanpa markdown atau penjelasan di luar JSON. Gunakan struktur:
{{
  "tujuan_pembelajaran": "isi...",
  "pemahaman_bermakna": "isi...",
  "pertanyaan_pemantik": "isi...",
  "persiapan_pembelajaran": "isi...",
  "langkah_pembelajaran": "isi dengan tahapan...",
  "asesmen": "isi...",
  "pengayaan": "isi...",
  "remedial": "isi...",
  "lkpd": "isi...",
  "bahan_bacaan": "isi...",
  "glosarium": "isi...",
  "daftar_pustaka": "isi..."
}}

Pastikan semua teks dalam Bahasa Indonesia yang baik dan benar, relevan untuk SD, dan praktis digunakan oleh guru.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Bersihkan markdown code block jika ada
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        data = json.loads(text)
        return data
    except Exception as e:
        print("Error Gemini:", e)
        return None
