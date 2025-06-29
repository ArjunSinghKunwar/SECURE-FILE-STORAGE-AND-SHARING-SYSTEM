from flask import Flask, request, session, redirect, send_from_directory, render_template, url_for, send_file, flash
import os
from auth import login_user  # Make sure you have this import
from crypto import encrypt_file, decrypt_file

UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Required for sessions

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = login_user(username, password)
        if role:
            session['username'] = username
            session['role'] = role
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Failed. Invalid username or password.', 'danger')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/upload', methods=['POST'])
def upload():
    if 'role' not in session or session['role'] != 'Admin':
        return "Only Admins can upload", 403
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if not file or not file.filename:
        return "No selected file", 400

    # Read keys from keys.txt
    with open('keys.txt', 'rb') as f:
        aes_key = f.read(32)
        hmac_key = f.read(32)

    file_data = file.read()
    encrypted_data = encrypt_file(file_data, aes_key, hmac_key)

    filepath = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")
    with open(filepath, 'wb') as f:
        f.write(encrypted_data)

    flash('File uploaded and encrypted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/files')
def files():
    if 'username' not in session:
        return redirect(url_for('index'))
    files = os.listdir(ENCRYPTED_FOLDER)
    return render_template('files.html', files=files, role=session['role'])

@app.route('/download/<filename>')
def download(filename):
    if 'role' not in session:
        return "Not logged in", 401
    if session['role'] == 'Viewer':
        return "Viewers cannot download files", 403
    
    # Read keys from keys.txt
    with open('keys.txt', 'rb') as f:
        aes_key = f.read(32)
        hmac_key = f.read(32)

    filepath = os.path.join(ENCRYPTED_FOLDER, filename)
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data, aes_key, hmac_key)
    
    # Writing decrypted data to a temporary file in memory
    from io import BytesIO
    return send_file(BytesIO(decrypted_data), as_attachment=True, download_name=filename.removesuffix('.enc'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if 'role' not in session or session['role'] != 'Admin':
        return "Only Admins can delete files", 403
    filepath = os.path.join(ENCRYPTED_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'File "{filename}" has been deleted.', 'success')
        return redirect(url_for('files'))
    else:
        return "File not found", 404

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

