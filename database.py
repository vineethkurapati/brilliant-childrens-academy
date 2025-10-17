import sqlite3
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

def init_database():
    """Initialize the SQLite database with tables and sample data"""
    
    # Create database connection
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL CHECK (user_type IN ('admin', 'student')),
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create textbooks table
    c.execute('''
        CREATE TABLE IF NOT EXISTS textbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 10),
            subject TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            uploaded_by TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (uploaded_by) REFERENCES users (username)
        )
    ''')
    
    # Create password reset tokens table
    c.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create activity log table
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert default admin user
    admin_hash = generate_password_hash('admin123')
    try:
        c.execute('''
            INSERT INTO users (username, email, password_hash, user_type, first_name, last_name) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin@brilliantacademy.edu', admin_hash, 'admin', 'Admin', 'User'))
        print("✓ Default admin user created: admin/admin123")
    except sqlite3.IntegrityError:
        print("✓ Admin user already exists")
    
    # Insert default student user
    student_hash = generate_password_hash('student123')
    try:
        c.execute('''
            INSERT INTO users (username, email, password_hash, user_type, first_name, last_name) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('student', 'student@brilliantacademy.edu', student_hash, 'student', 'Student', 'User'))
        print("✓ Default student user created: student/student123")
    except sqlite3.IntegrityError:
        print("✓ Student user already exists")
    
    # Insert sample textbooks
    sample_textbooks = [
        # Grade 1
        ('math_grade1_basics.pdf', 'Mathematics Basics - Grade 1', 1, 'Mathematics', 'pdf', 2048000, 'admin', 'Introduction to numbers and basic arithmetic'),
        ('english_grade1_reader.pdf', 'English Reader - Grade 1', 1, 'English', 'pdf', 1536000, 'admin', 'Basic reading and vocabulary'),
        ('science_grade1_nature.pdf', 'Science and Nature - Grade 1', 1, 'Science', 'pdf', 1792000, 'admin', 'Introduction to plants and animals'),
        
        # Grade 2
        ('math_grade2_addition.pdf', 'Mathematics Addition - Grade 2', 2, 'Mathematics', 'pdf', 2304000, 'admin', 'Addition and subtraction concepts'),
        ('english_grade2_stories.pdf', 'English Stories - Grade 2', 2, 'English', 'pdf', 1843200, 'admin', 'Short stories and comprehension'),
        
        # Grade 3
        ('math_grade3_multiplication.pdf', 'Mathematics Multiplication - Grade 3', 3, 'Mathematics', 'pdf', 2560000, 'admin', 'Multiplication tables and division'),
        ('science_grade3_experiments.pdf', 'Science Experiments - Grade 3', 3, 'Science', 'pdf', 2048000, 'admin', 'Simple science experiments'),
        
        # Grade 4
        ('social_studies_grade4.pdf', 'Social Studies - Grade 4', 4, 'Social Studies', 'pdf', 2816000, 'admin', 'Community and geography basics'),
        ('hindi_grade4_poems.pdf', 'Hindi Poems - Grade 4', 4, 'Hindi', 'pdf', 1536000, 'admin', 'Hindi poetry and literature'),
        
        # Grade 5
        ('computer_science_grade5.pdf', 'Computer Science - Grade 5', 5, 'Computer Science', 'pdf', 3072000, 'admin', 'Introduction to computers'),
        ('art_grade5_drawing.pdf', 'Art and Drawing - Grade 5', 5, 'Art', 'pdf', 4096000, 'admin', 'Basic drawing techniques'),
    ]
    
    for textbook in sample_textbooks:
        try:
            c.execute('''
                INSERT INTO textbooks (filename, original_name, grade, subject, file_type, file_size, uploaded_by, description) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', textbook)
        except sqlite3.IntegrityError:
            pass  # Textbook already exists
    
    print(f"✓ Sample textbooks added to database")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("✓ Database initialized successfully!")
    print("✓ Database file: school.db")
    

def get_database_stats():
    """Get statistics about the database"""
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Count users
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'admin'")
    admin_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE user_type = 'student'")
    student_count = c.fetchone()[0]
    
    # Count textbooks
    c.execute("SELECT COUNT(*) FROM textbooks")
    textbook_count = c.fetchone()[0]
    
    # Count textbooks by grade
    c.execute("SELECT grade, COUNT(*) FROM textbooks GROUP BY grade ORDER BY grade")
    grade_stats = c.fetchall()
    
    conn.close()
    
    return {
        'admin_count': admin_count,
        'student_count': student_count,
        'textbook_count': textbook_count,
        'grade_stats': grade_stats
    }

def create_sample_uploads_structure():
    """Create sample upload directory structure"""
    base_path = 'uploads/textbooks'
    subjects = ['Mathematics', 'English', 'Science', 'Social Studies', 'Hindi', 'Computer Science', 'Art', 'Physical Education']
    
    for grade in range(1, 11):
        for subject in subjects:
            dir_path = os.path.join(base_path, f'grade_{grade}', subject)
            os.makedirs(dir_path, exist_ok=True)
    
    print("✓ Upload directory structure created")

if __name__ == '__main__':
    print("Initializing Brilliant Childrens Academy Database...")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    # Create upload structure
    create_sample_uploads_structure()
    
    # Show statistics
    stats = get_database_stats()
    print("\nDatabase Statistics:")
    print(f"- Admin users: {stats['admin_count']}")
    print(f"- Student users: {stats['student_count']}")
    print(f"- Total textbooks: {stats['textbook_count']}")
    print("\nTextbooks by grade:")
    for grade, count in stats['grade_stats']:
        print(f"  Grade {grade}: {count} textbooks")
    
    print("\n✓ Setup complete! You can now run the Flask application.")
    print("✓ Run: python app.py")