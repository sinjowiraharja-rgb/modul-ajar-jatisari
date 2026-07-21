import os
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify, abort

import database as db
from config import SECRET_KEY, DIMENSI_PROFIL_PANCASILA, MAPEL_SD, FASE_KELAS, PENDEKATAN
from gemini_client import generate_modul_content
from docx_generator import generate_docx
from pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Inisialisasi database sebelum request pertama
@app.before_request
def init_app():
    if not getattr(app, '_db_initialized', False):
        db.init_db()
        app._db_initialized = True


# ======================== DECORATORS ========================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Akses ditolak. Halaman ini hanya untuk admin.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ======================== AUTH ========================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = db.get_user_by_username(username)
        if user and db.verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['nama_lengkap'] = user['nama_lengkap']
            flash(f"Selamat datang, {user['nama_lengkap']}!")
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))


# ======================== DASHBOARD ========================

@app.route('/dashboard')
@login_required
def dashboard():
    if session['role'] == 'admin':
        total_guru = len(db.list_guru())
        total_modul = len(db.list_modul(role='admin'))
        profil = db.get_profil_sekolah()
        return render_template('dashboard_admin.html',
                               total_guru=total_guru,
                               total_modul=total_modul,
                               profil=profil)
    else:
        user_id = session['user_id']
        moduls = db.list_modul(user_id=user_id)
        return render_template('dashboard_guru.html', moduls=moduls)


# ======================== ADMIN: PROFIL SEKOLAH ========================

@app.route('/admin/sekolah', methods=['GET', 'POST'])
@login_required
@admin_required
def kelola_sekolah():
    profil = db.get_profil_sekolah()
    if request.method == 'POST':
        data = {
            'nama_sekolah': request.form.get('nama_sekolah', '').strip(),
            'npsn': request.form.get('npsn', '').strip(),
            'alamat': request.form.get('alamat', '').strip(),
            'nama_kepala_sekolah': request.form.get('nama_kepala_sekolah', '').strip(),
            'nip_kepala_sekolah': request.form.get('nip_kepala_sekolah', '').strip(),
            'semester': request.form.get('semester', '').strip(),
            'tahun_ajaran': request.form.get('tahun_ajaran', '').strip(),
        }
        db.save_profil_sekolah(data)
        flash('Profil sekolah berhasil disimpan.', 'success')
        return redirect(url_for('kelola_sekolah'))
    return render_template('kelola_sekolah.html', profil=profil)


# ======================== ADMIN: KELOLA GURU ========================

@app.route('/admin/guru', methods=['GET', 'POST'])
@login_required
@admin_required
def kelola_guru():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            nama_lengkap = request.form.get('nama_lengkap', '').strip()
            kelas_diampu = request.form.get('kelas_diampu', '').strip()
            mapel_diampu = request.form.get('mapel_diampu', '').strip()
            success, msg = db.create_user(username, password, nama_lengkap, 'guru', kelas_diampu, mapel_diampu)
            flash(msg, 'success' if success else 'danger')
        elif action == 'delete':
            user_id = request.form.get('user_id')
            if user_id:
                db.delete_user(int(user_id))
                flash('Guru berhasil dihapus.', 'success')
        return redirect(url_for('kelola_guru'))

    gurus = db.list_guru()
    return render_template('kelola_guru.html', gurus=gurus)


# ======================== ADMIN: REFERENSI ========================

@app.route('/admin/referensi', methods=['GET', 'POST'])
@login_required
@admin_required
def kelola_referensi():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            data = {
                'fase': request.form.get('fase', '').strip(),
                'kelas': request.form.get('kelas', '').strip(),
                'mapel': request.form.get('mapel', '').strip(),
                'elemen': request.form.get('elemen', '').strip(),
                'capaian_pembelajaran': request.form.get('capaian_pembelajaran', '').strip(),
            }
            success, msg = db.add_referensi_mapel(data)
            flash(msg, 'success' if success else 'danger')
        elif action == 'delete':
            ref_id = request.form.get('ref_id')
            if ref_id:
                db.delete_referensi_mapel(int(ref_id))
                flash('Referensi berhasil dihapus.', 'success')
        elif action == 'update':
            ref_id = request.form.get('ref_id')
            data = {
                'fase': request.form.get('fase', '').strip(),
                'kelas': request.form.get('kelas', '').strip(),
                'mapel': request.form.get('mapel', '').strip(),
                'elemen': request.form.get('elemen', '').strip(),
                'capaian_pembelajaran': request.form.get('capaian_pembelajaran', '').strip(),
            }
            if ref_id:
                db.update_referensi_mapel(int(ref_id), data)
                flash('Referensi berhasil diperbarui.', 'success')
        return redirect(url_for('kelola_referensi'))

    referensi = db.list_referensi_mapel()
    return render_template('kelola_referensi.html',
                           referensi=referensi,
                           fase_kelas=FASE_KELAS,
                           mapel_list=MAPEL_SD)


# ======================== MODUL AJAR ========================

def build_modul_data_from_form(user_id, modul=None):
    """Membentuk dict data modul dari form."""
    dimensi = request.form.getlist('dimensi_pancasila')
    data = {
        'user_id': user_id,
        'jenis_dokumen': request.form.get('jenis_dokumen', 'Modul Ajar').strip(),
        'nama_guru': request.form.get('nama_guru', '').strip(),
        'nama_kepala_sekolah': request.form.get('nama_kepala_sekolah', '').strip(),
        'nama_sekolah': request.form.get('nama_sekolah', '').strip(),
        'fase': request.form.get('fase', '').strip(),
        'kelas': request.form.get('kelas', '').strip(),
        'mapel': request.form.get('mapel', '').strip(),
        'topik': request.form.get('topik', '').strip(),
        'alokasi_waktu': request.form.get('alokasi_waktu', '').strip(),
        'minggu_pelaksanaan': request.form.get('minggu_pelaksanaan', '').strip(),
        'kompetensi_awal': request.form.get('kompetensi_awal', '').strip(),
        'dimensi_pancasila': ', '.join(dimensi),
        'pendekatan': request.form.get('pendekatan', 'deep_learning'),
        'sarana_prasarana': request.form.get('sarana_prasarana', '').strip(),
        'target_peserta_didik': request.form.get('target_peserta_didik', '').strip(),
        'model_pembelajaran': request.form.get('model_pembelajaran', '').strip(),
        'tujuan_pembelajaran': request.form.get('tujuan_pembelajaran', '').strip(),
        'pemahaman_bermakna': request.form.get('pemahaman_bermakna', '').strip(),
        'pertanyaan_pemantik': request.form.get('pertanyaan_pemantik', '').strip(),
        'persiapan_pembelajaran': request.form.get('persiapan_pembelajaran', '').strip(),
        'langkah_pembelajaran': request.form.get('langkah_pembelajaran', '').strip(),
        'asesmen': request.form.get('asesmen', '').strip(),
        'pengayaan': request.form.get('pengayaan', '').strip(),
        'remedial': request.form.get('remedial', '').strip(),
        'lkpd': request.form.get('lkpd', '').strip(),
        'bahan_bacaan': request.form.get('bahan_bacaan', '').strip(),
        'glosarium': request.form.get('glosarium', '').strip(),
        'daftar_pustaka': request.form.get('daftar_pustaka', '').strip(),
    }
    return data


@app.route('/modul/baru', methods=['GET', 'POST'])
@login_required
def modul_baru():
    user = db.get_user_by_id(session['user_id'])
    profil = db.get_profil_sekolah()

    if request.method == 'POST':
        data = build_modul_data_from_form(session['user_id'])
        modul_id = db.create_modul(data)
        flash('Modul ajar berhasil dibuat. Silakan generate konten atau langsung edit.', 'success')
        return redirect(url_for('preview_modul', modul_id=modul_id))

    return render_template('form_modul.html',
                           modul=None,
                           user=user,
                           profil=profil,
                           dimensi_list=DIMENSI_PROFIL_PANCASILA,
                           mapel_list=MAPEL_SD,
                           fase_kelas=FASE_KELAS,
                           pendekatan_list=PENDEKATAN)


@app.route('/modul/<int:modul_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_modul(modul_id):
    user_id = session['user_id']
    role = session['role']
    modul = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    if not modul:
        abort(404)

    user = db.get_user_by_id(user_id)
    profil = db.get_profil_sekolah()

    if request.method == 'POST':
        data = build_modul_data_from_form(user_id)
        db.update_modul(modul_id, data)
        flash('Modul ajar berhasil diperbarui.', 'success')
        return redirect(url_for('preview_modul', modul_id=modul_id))

    return render_template('form_modul.html',
                           modul=modul,
                           user=user,
                           profil=profil,
                           dimensi_list=DIMENSI_PROFIL_PANCASILA,
                           mapel_list=MAPEL_SD,
                           fase_kelas=FASE_KELAS,
                           pendekatan_list=PENDEKATAN)


@app.route('/modul/<int:modul_id>/preview')
@login_required
def preview_modul(modul_id):
    user_id = session['user_id']
    role = session['role']
    modul = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    if not modul:
        abort(404)
    return render_template('preview_modul.html', modul=modul)


@app.route('/modul/<int:modul_id>/generate-ai', methods=['POST'])
@login_required
def generate_ai(modul_id):
    """Generate atau regenerasi konten modul ajar dengan AI Gemini."""
    user_id = session['user_id']
    role = session['role']
    modul = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    if not modul:
        return jsonify({'success': False, 'message': 'Modul tidak ditemukan.'}), 404

    # Update data terlebih dahulu dari form saat ini
    data = build_modul_data_from_form(user_id)
    db.update_modul(modul_id, data)

    generated = generate_modul_content(data)
    if not generated:
        return jsonify({'success': False, 'message': 'Gagal generate konten AI. Pastikan API key Gemini sudah benar.'}), 500

    # Update modul dengan hasil generate
    current = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    for key in generated:
        if key in current:
            current[key] = generated[key]
    db.update_modul(modul_id, current)

    return jsonify({'success': True, 'message': 'Konten berhasil digenerate.', 'data': generated})


@app.route('/modul/riwayat')
@login_required
def riwayat_modul():
    user_id = session['user_id']
    role = session['role']
    moduls = db.list_modul(user_id=user_id if role == 'guru' else None, role=role)
    return render_template('riwayat.html', moduls=moduls)


@app.route('/modul/<int:modul_id>/delete', methods=['POST'])
@login_required
def delete_modul(modul_id):
    db.delete_modul(modul_id, user_id=session['user_id'], role=session['role'])
    flash('Modul ajar berhasil dihapus.', 'success')
    return redirect(url_for('riwayat_modul'))


# ======================== EXPORT ========================

@app.route('/modul/<int:modul_id>/export/word')
@login_required
def export_word(modul_id):
    user_id = session['user_id']
    role = session['role']
    modul = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    if not modul:
        abort(404)

    safe_topik = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modul['topik']).replace(' ', '_')
    filename = f"Modul_Ajar_{safe_topik}_Kelas_{modul['kelas']}.docx"
    output_path = os.path.join('data', filename)

    generate_docx(modul, output_path)
    return send_file(output_path, as_attachment=True, download_name=filename)


@app.route('/modul/<int:modul_id>/export/pdf')
@login_required
def export_pdf(modul_id):
    user_id = session['user_id']
    role = session['role']
    modul = db.get_modul_by_id(modul_id, user_id=user_id, role=role)
    if not modul:
        abort(404)

    safe_topik = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modul['topik']).replace(' ', '_')
    filename = f"Modul_Ajar_{safe_topik}_Kelas_{modul['kelas']}.pdf"
    output_path = os.path.join('data', filename)

    result = generate_pdf(modul, output_path)
    if result:
        return send_file(output_path, as_attachment=True, download_name=filename)
    else:
        flash('Export PDF belum tersedia. Silakan eksport Word terlebih dahulu.', 'warning')
        return redirect(url_for('preview_modul', modul_id=modul_id))


# ======================== API REFERENSI ========================

@app.route('/api/referensi')
@login_required
def api_referensi():
    fase = request.args.get('fase', '').strip()
    kelas = request.args.get('kelas', '').strip()
    mapel = request.args.get('mapel', '').strip()
    data = db.list_referensi_mapel(fase=fase, kelas=kelas, mapel=mapel)
    return jsonify([{
        'id': item['id'],
        'elemen': item['elemen'],
        'capaian_pembelajaran': item['capaian_pembelajaran']
    } for item in data])


# ======================== ERROR HANDLERS ========================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
