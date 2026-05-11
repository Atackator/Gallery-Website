import os
import re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads/')
app.config['THUMBNAIL_SIZE'] = (200, 200)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def sanitize_filename(filename):
    # Remove special characters
    filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
    return filename

def create_thumbnail(image_path):
    img = Image.open(image_path)
    img.thumbnail(app.config['THUMBNAIL_SIZE'])
    base, ext = os.path.splitext(image_path)
    thumbnail_path = f"{base}.thumb{ext}"
    img.save(thumbnail_path)
    return thumbnail_path

@app.route('/')
def index():
    categories = os.listdir(app.config['UPLOAD_FOLDER'])
    images = {category: os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], category)) for category in categories}
    return render_template('index.html', images=images)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], category), exist_ok=True)

        file = request.files['image']
        if 'name' in request.form and request.form['name'].strip():
            filename = sanitize_filename(request.form['name']) + os.path.splitext(file.filename)[1]
        else:
            filename = secure_filename(file.filename)
            filename = sanitize_filename(filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], category, filename)
        file.save(filepath)

        create_thumbnail(filepath)

        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    category = request.form['category']
    filename = request.form['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], category, filename)
    thumb_path = os.path.splitext(file_path)[0] + '.thumb' + os.path.splitext(file_path)[1]

    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
