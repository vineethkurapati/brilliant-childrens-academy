from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads/textbooks'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'ppt', 'pptx', 'xls', 'xlsx', 'mp4', 'mp3', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database initialization
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  user_type TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Textbooks table
    c.execute('''CREATE TABLE IF NOT EXISTS textbooks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT NOT NULL,
                  original_name TEXT NOT NULL,
                  grade INTEGER NOT NULL,
                  subject TEXT NOT NULL,
                  file_type TEXT NOT NULL,
                  file_size INTEGER NOT NULL,
                  uploaded_by TEXT NOT NULL,
                  upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create default admin user
    admin_hash = generate_password_hash('admin123')
    student_hash = generate_password_hash('student123')
    
    try:
        c.execute("INSERT INTO users (username, email, password_hash, user_type) VALUES (?, ?, ?, ?)",
                 ('admin', 'admin@school.com', admin_hash, 'admin'))
        c.execute("INSERT INTO users (username, email, password_hash, user_type) VALUES (?, ?, ?, ?)",
                 ('student', 'student@school.com', student_hash, 'student'))
    except sqlite3.IntegrityError:
        pass  # Users already exist
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND user_type = ?", (username, user_type))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_type'] = user[4]
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user_type = request.form['user_type']
        
        # In a real application, you would send an email
        flash(f'Password reset link sent to {email}', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/textbooks')
def textbooks():
    return render_template('textbooks.html')

@app.route('/textbooks/<int:grade>')
def grade_textbooks(grade):
    subjects = ['Mathematics', 'English', 'Science', 'Social Studies', 'Hindi', 'Computer Science', 'Art', 'Physical Education']
    
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    textbook_data = {}
    for subject in subjects:
        c.execute("SELECT * FROM textbooks WHERE grade = ? AND subject = ?", (grade, subject))
        textbook_data[subject] = c.fetchall()
    
    conn.close()
    return render_template('grade_textbooks.html', grade=grade, subjects=subjects, textbooks=textbook_data)

@app.route('/upload_textbook', methods=['POST'])
def upload_textbook():
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(request.referrer)
    
    file = request.files['file']
    grade = request.form['grade']
    subject = request.form['subject']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.referrer)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        unique_filename = timestamp + filename
        
        # Create grade/subject directory if it doesn't exist
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f'grade_{grade}', subject)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Save to database
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("INSERT INTO textbooks (filename, original_name, grade, subject, file_type, file_size, uploaded_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (unique_filename, filename, grade, subject, filename.rsplit('.', 1)[1].lower(), os.path.getsize(file_path), session['username']))
        conn.commit()
        conn.close()
        
        flash(f'File {filename} uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload PDF, DOC, DOCX, JPG, PNG, TXT, PPT, XLS, MP4, MP3, or ZIP files.', 'error')
    
    return redirect(request.referrer)

@app.route('/delete_textbook/<int:textbook_id>')
def delete_textbook(textbook_id):
    if 'user_type' not in session or session['user_type'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Get file info
    c.execute("SELECT * FROM textbooks WHERE id = ?", (textbook_id,))
    textbook = c.fetchone()
    
    if textbook:
        # Delete file from filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'grade_{textbook[3]}', textbook[4], textbook[1])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        c.execute("DELETE FROM textbooks WHERE id = ?", (textbook_id,))
        conn.commit()
        flash(f'File {textbook[2]} deleted successfully!', 'success')
    else:
        flash('File not found', 'error')
    
    conn.close()
    return redirect(request.referrer)

@app.route('/download_textbook/<int:textbook_id>')
def download_textbook(textbook_id):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT * FROM textbooks WHERE id = ?", (textbook_id,))
    textbook = c.fetchone()
    conn.close()
    
    if textbook:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'grade_{textbook[3]}', textbook[4], textbook[1])
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=textbook[2])
        else:
            flash('File not found', 'error')
    else:
        flash('File not found', 'error')
    
    return redirect(request.referrer)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
