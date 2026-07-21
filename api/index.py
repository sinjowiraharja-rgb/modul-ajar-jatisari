import sys
import os

# Tambahkan folder parent ke path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment untuk Vercel
os.environ['VERCEL'] = '1'

# Import aplikasi Flask dari app.py
from app import app

# Vercel akan menggunakan variabel 'app' sebagai WSGI handler
handler = app
