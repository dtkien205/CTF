from flask import Flask, request, session, redirect, url_for, render_template, flash, send_file
from werkzeug.utils import secure_filename
import os, time, sqlite3, hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'database.db'
UPLOAD_DIR = 'uploads'
MAX_CONTENT_LENGTH = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'doc', 'docx', 'xlsx', 'pptx'
}

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
    print("Database initialized.")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        # ❌ SQLi: nối chuỗi trực tiếp
        user = conn.execute(
            'SELECT * FROM users WHERE username = "' + username + '" AND password = "' + hashed_password + '"'
        ).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html', error='Invalid credentials')

    message = request.args.get('message')
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html', error='Username and password are required.')

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login', message='Registration successful! Please log in.'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html', error='Username already exists. Please choose a different one.')
        except Exception as e:
            conn.close()
            flash(f'An unexpected error occurred: {e}', 'error')
            return render_template('register.html', error=f'An error occurred: {e}')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get('logged_in'):
        flash('Please log in to upload files.', 'error')
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('dashboard'))

    file = request.files['file']

    # Xóa thư mục uploads sau 5 phút kể từ mốc time.txt
    with open('time.txt', 'r') as f:
        start = f.read().strip()
    if time.time() - float(start) > 5 * 60:
        for filename in os.listdir(UPLOAD_DIR):
            filepath = os.path.join(UPLOAD_DIR, filename)
            os.remove(filepath)

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('dashboard'))

    if file and allowed_file(file.filename):
        # Kiểm tra kích thước file
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_CONTENT_LENGTH:
            flash(f'File size exceeds the limit of {MAX_CONTENT_LENGTH / (1024 * 1024)}MB.', 'error')
            return redirect(url_for('dashboard'))

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Tránh trùng tên
        timestamp = int(time.time())
        original_without_ext, ext = os.path.splitext(filepath)
        while os.path.exists(filepath):
            filepath = f"{original_without_ext}_{timestamp}{ext}"
            filename = os.path.basename(filepath)

        try:
            file.save(filepath)
            download_url = url_for('download_file', filename=filename, _external=True)
            flash(
                f'File "{filename}" uploaded successfully! You can download it <a href="{download_url}">here</a>.',
                'success'
            )
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error uploading file: {e}', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('File type not allowed or no file selected.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/download', methods=['GET'])
def download_file():
    if not session.get('logged_in'):
        flash('Please log in to download files.', 'error')
        return "Unauthorized: Please log in.", 401

    filename = request.args.get('filename')
    if not filename:
        flash("Missing 'filename' parameter for download.", 'error')
        return "Error: Missing filename parameter.", 400

    # ❗ Dễ bị Path Traversal vì không sanitize filename khi DOWNLOAD
    download_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(download_path) and os.path.isfile(download_path):
        try:
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            flash(f'Error serving file: {e}', 'error')
            return f"Error serving file: {e}", 500
    else:
        flash('File not found.', 'error')
        return "File not found.", 404

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    with open('time.txt', 'w') as f:
        f.write(str(time.time()))
    app.run(debug=False, host='0.0.0.0', port=5000)
