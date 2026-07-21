import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    return conn


def init_db():
    """Inisialisasi tabel dan data awal."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabel pengguna (admin & guru)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nama_lengkap TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'guru')),
            kelas_diampu TEXT,
            mapel_diampu TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    # Tabel profil sekolah
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profil_sekolah (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_sekolah TEXT NOT NULL,
            npsn TEXT,
            alamat TEXT,
            nama_kepala_sekolah TEXT,
            nip_kepala_sekolah TEXT,
            semester TEXT,
            tahun_ajaran TEXT,
            updated_at TEXT NOT NULL
        )
    ''')

    # Tabel referensi mata pelajaran per fase/kelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referensi_mapel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase TEXT NOT NULL,
            kelas TEXT NOT NULL,
            mapel TEXT NOT NULL,
            elemen TEXT,
            capaian_pembelajaran TEXT,
            UNIQUE(fase, kelas, mapel)
        )
    ''')

    # Tabel modul ajar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modul_ajar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            jenis_dokumen TEXT NOT NULL,
            nama_guru TEXT NOT NULL,
            nama_kepala_sekolah TEXT,
            nama_sekolah TEXT NOT NULL,
            fase TEXT NOT NULL,
            kelas TEXT NOT NULL,
            mapel TEXT NOT NULL,
            topik TEXT NOT NULL,
            alokasi_waktu TEXT NOT NULL,
            minggu_pelaksanaan TEXT,
            kompetensi_awal TEXT,
            dimensi_pancasila TEXT,
            pendekatan TEXT NOT NULL,
            sarana_prasarana TEXT,
            target_peserta_didik TEXT,
            model_pembelajaran TEXT,
            tujuan_pembelajaran TEXT,
            pemahaman_bermakna TEXT,
            pertanyaan_pemantik TEXT,
            persiapan_pembelajaran TEXT,
            langkah_pembelajaran TEXT,
            asesmen TEXT,
            pengayaan TEXT,
            remedial TEXT,
            lkpd TEXT,
            bahan_bacaan TEXT,
            glosarium TEXT,
            daftar_pustaka TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Seed user admin
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, password_hash, nama_lengkap, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', hashed, 'Administrator', 'admin', datetime.now().isoformat()))

    conn.commit()
    conn.close()


# ======================== USERS ========================

def create_user(username, password, nama_lengkap, role, kelas_diampu=None, mapel_diampu=None):
    conn = get_db_connection()
    try:
        hashed = generate_password_hash(password)
        conn.execute('''
            INSERT INTO users (username, password_hash, nama_lengkap, role, kelas_diampu, mapel_diampu, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, hashed, nama_lengkap, role, kelas_diampu, mapel_diampu, datetime.now().isoformat()))
        conn.commit()
        return True, "User berhasil dibuat"
    except sqlite3.IntegrityError:
        return False, "Username sudah digunakan"
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)


def update_password(user_id, new_password):
    conn = get_db_connection()
    hashed = generate_password_hash(new_password)
    conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, user_id))
    conn.commit()
    conn.close()


def list_guru():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM users WHERE role = 'guru' ORDER BY nama_lengkap").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


# ======================== PROFIL SEKOLAH ========================

def save_profil_sekolah(data):
    conn = get_db_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute("SELECT id FROM profil_sekolah LIMIT 1")
    existing = cursor.fetchone()
    if existing:
        conn.execute('''
            UPDATE profil_sekolah SET
                nama_sekolah = ?, npsn = ?, alamat = ?, nama_kepala_sekolah = ?,
                nip_kepala_sekolah = ?, semester = ?, tahun_ajaran = ?, updated_at = ?
            WHERE id = ?
        ''', (
            data['nama_sekolah'], data['npsn'], data['alamat'], data['nama_kepala_sekolah'],
            data['nip_kepala_sekolah'], data['semester'], data['tahun_ajaran'], now, existing['id']
        ))
    else:
        conn.execute('''
            INSERT INTO profil_sekolah
            (nama_sekolah, npsn, alamat, nama_kepala_sekolah, nip_kepala_sekolah,
             semester, tahun_ajaran, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nama_sekolah'], data['npsn'], data['alamat'], data['nama_kepala_sekolah'],
            data['nip_kepala_sekolah'], data['semester'], data['tahun_ajaran'], now
        ))
    conn.commit()
    conn.close()
    return get_profil_sekolah()


def get_profil_sekolah():
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM profil_sekolah LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else None


# ======================== REFERENSI MAPEL ========================

def add_referensi_mapel(data):
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO referensi_mapel (fase, kelas, mapel, elemen, capaian_pembelajaran)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['fase'], data['kelas'], data['mapel'], data.get('elemen', ''),
            data.get('capaian_pembelajaran', '')
        ))
        conn.commit()
        return True, "Referensi berhasil ditambahkan"
    except sqlite3.IntegrityError:
        return False, "Referensi sudah ada"
    except Exception as e:
        return False, f"Gagal menyimpan: {str(e)}"
    finally:
        conn.close()


def update_referensi_mapel(ref_id, data):
    conn = get_db_connection()
    conn.execute('''
        UPDATE referensi_mapel SET fase = ?, kelas = ?, mapel = ?, elemen = ?, capaian_pembelajaran = ?
        WHERE id = ?
    ''', (data['fase'], data['kelas'], data['mapel'], data.get('elemen', ''),
          data.get('capaian_pembelajaran', ''), ref_id))
    conn.commit()
    conn.close()


def delete_referensi_mapel(ref_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM referensi_mapel WHERE id = ?", (ref_id,))
    conn.commit()
    conn.close()


def list_referensi_mapel(fase=None, kelas=None, mapel=None):
    conn = get_db_connection()
    query = "SELECT * FROM referensi_mapel WHERE 1=1"
    params = []
    if fase:
        query += " AND fase = ?"
        params.append(fase)
    if kelas:
        query += " AND kelas = ?"
        params.append(kelas)
    if mapel:
        query += " AND mapel = ?"
        params.append(mapel)
    query += " ORDER BY fase, kelas, mapel"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_referensi_by_id(ref_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM referensi_mapel WHERE id = ?", (ref_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ======================== MODUL AJAR ========================

def create_modul(data):
    conn = get_db_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute('''
        INSERT INTO modul_ajar (
            user_id, jenis_dokumen, nama_guru, nama_kepala_sekolah, nama_sekolah,
            fase, kelas, mapel, topik, alokasi_waktu, minggu_pelaksanaan,
            kompetensi_awal, dimensi_pancasila, pendekatan, sarana_prasarana,
            target_peserta_didik, model_pembelajaran, tujuan_pembelajaran,
            pemahaman_bermakna, pertanyaan_pemantik, persiapan_pembelajaran,
            langkah_pembelajaran, asesmen, pengayaan, remedial, lkpd,
            bahan_bacaan, glosarium, daftar_pustaka, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['user_id'], data['jenis_dokumen'], data['nama_guru'], data.get('nama_kepala_sekolah', ''),
        data['nama_sekolah'], data['fase'], data['kelas'], data['mapel'], data['topik'],
        data['alokasi_waktu'], data.get('minggu_pelaksanaan', ''), data.get('kompetensi_awal', ''),
        data.get('dimensi_pancasila', ''), data['pendekatan'], data.get('sarana_prasarana', ''),
        data.get('target_peserta_didik', ''), data.get('model_pembelajaran', ''),
        data.get('tujuan_pembelajaran', ''), data.get('pemahaman_bermakna', ''),
        data.get('pertanyaan_pemantik', ''), data.get('persiapan_pembelajaran', ''),
        data.get('langkah_pembelajaran', ''), data.get('asesmen', ''), data.get('pengayaan', ''),
        data.get('remedial', ''), data.get('lkpd', ''), data.get('bahan_bacaan', ''),
        data.get('glosarium', ''), data.get('daftar_pustaka', ''), now, now
    ))
    modul_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return modul_id


def update_modul(modul_id, data):
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute('''
        UPDATE modul_ajar SET
            jenis_dokumen = ?, nama_guru = ?, nama_kepala_sekolah = ?, nama_sekolah = ?,
            fase = ?, kelas = ?, mapel = ?, topik = ?, alokasi_waktu = ?, minggu_pelaksanaan = ?,
            kompetensi_awal = ?, dimensi_pancasila = ?, pendekatan = ?, sarana_prasarana = ?,
            target_peserta_didik = ?, model_pembelajaran = ?, tujuan_pembelajaran = ?,
            pemahaman_bermakna = ?, pertanyaan_pemantik = ?, persiapan_pembelajaran = ?,
            langkah_pembelajaran = ?, asesmen = ?, pengayaan = ?, remedial = ?, lkpd = ?,
            bahan_bacaan = ?, glosarium = ?, daftar_pustaka = ?, updated_at = ?
        WHERE id = ?
    ''', (
        data['jenis_dokumen'], data['nama_guru'], data.get('nama_kepala_sekolah', ''),
        data['nama_sekolah'], data['fase'], data['kelas'], data['mapel'], data['topik'],
        data['alokasi_waktu'], data.get('minggu_pelaksanaan', ''), data.get('kompetensi_awal', ''),
        data.get('dimensi_pancasila', ''), data['pendekatan'], data.get('sarana_prasarana', ''),
        data.get('target_peserta_didik', ''), data.get('model_pembelajaran', ''),
        data.get('tujuan_pembelajaran', ''), data.get('pemahaman_bermakna', ''),
        data.get('pertanyaan_pemantik', ''), data.get('persiapan_pembelajaran', ''),
        data.get('langkah_pembelajaran', ''), data.get('asesmen', ''), data.get('pengayaan', ''),
        data.get('remedial', ''), data.get('lkpd', ''), data.get('bahan_bacaan', ''),
        data.get('glosarium', ''), data.get('daftar_pustaka', ''), now, modul_id
    ))
    conn.commit()
    conn.close()


def get_modul_by_id(modul_id, user_id=None, role='guru'):
    conn = get_db_connection()
    query = "SELECT * FROM modul_ajar WHERE id = ?"
    params = [modul_id]
    if role == 'guru':
        query += " AND user_id = ?"
        params.append(user_id)
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None


def list_modul(user_id=None, role='guru'):
    conn = get_db_connection()
    if role == 'admin':
        query = "SELECT * FROM modul_ajar ORDER BY created_at DESC"
        params = []
    else:
        query = "SELECT * FROM modul_ajar WHERE user_id = ? ORDER BY created_at DESC"
        params = [user_id]
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_modul(modul_id, user_id=None, role='guru'):
    conn = get_db_connection()
    if role == 'admin':
        conn.execute("DELETE FROM modul_ajar WHERE id = ?", (modul_id,))
    else:
        conn.execute("DELETE FROM modul_ajar WHERE id = ? AND user_id = ?", (modul_id, user_id))
    conn.commit()
    conn.close()
