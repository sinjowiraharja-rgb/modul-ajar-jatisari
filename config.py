import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel hanya bisa menulis ke /tmp
if os.environ.get('VERCEL') == '1':
    DATA_DIR = os.path.join('/tmp', 'data')
else:
    DATA_DIR = os.path.join(BASE_DIR, 'data')

DB_PATH = os.path.join(DATA_DIR, 'modul_ajar.db')

SECRET_KEY = os.environ.get('SECRET_KEY', 'modul-ajar-jatisari-default-secret')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Pastikan folder data ada
os.makedirs(DATA_DIR, exist_ok=True)

DIMENSI_PROFIL_PANCASILA = [
    "Beriman, Bertakwa kepada Tuhan Yang Maha Esa, dan Berakhlak Mulia",
    "Mandiri",
    "Bergotong Royong",
    "Kreatif",
    "Berkebhinekaan Global",
    "Bernalar Kritis",
    "Bernalar Kreatif",
    "Berkebinekaan"
]

MAPEL_SD = [
    "Pendidikan Agama dan Budi Pekerti",
    "Pendidikan Kewarganegaraan",
    "Bahasa Indonesia",
    "Matematika",
    "Ilmu Pengetahuan Alam",
    "Ilmu Pengetahuan Sosial",
    "Seni Budaya dan Prakarya",
    "Pendidikan Jasmani, Olahraga, dan Kesehatan",
    "Bahasa Inggris"
]

FASE_KELAS = {
    "A": ["1", "2"],
    "B": ["3", "4"],
    "C": ["5", "6"]
}

PENDEKATAN = [
    ("deep_learning", "Deep Learning"),
    ("steam", "S.T.E.A.M")
]
