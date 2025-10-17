import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

class User:
    """User model for handling admin and student users"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 user_type=None, first_name=None, last_name=None, 
                 created_at=None, last_login=None, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.user_type = user_type
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
        self.last_login = last_login
        self.is_active = is_active
    
    @staticmethod
    def create_user(username, email, password, user_type, first_name=None, last_name=None):
        """Create a new user"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        password_hash = generate_password_hash(password)
        
        try:
            c.execute('''
                INSERT INTO users (username, email, password_hash, user_type, first_name, last_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, user_type, first_name, last_name))
            
            user_id = c.lastrowid
            conn.commit()
            
            # Log the activity
            ActivityLog.log_activity(user_id, 'USER_CREATED', f'User {username} created with type {user_type}')
            
            conn.close()
            return user_id
        except sqlite3.IntegrityError as e:
            conn.close()
            raise ValueError(f"User creation failed: {str(e)}")
    
    @staticmethod
    def authenticate(username, password, user_type):
        """Authenticate user login"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, username, email, password_hash, user_type, first_name, last_name, 
                   created_at, last_login, is_active
            FROM users 
            WHERE username = ? AND user_type = ? AND is_active = 1
        ''', (username, user_type))
        
        user_data = c.fetchone()
        
        if user_data and check_password_hash(user_data[3], password):
            # Update last login
            c.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user_data[0],))
            conn.commit()
            
            # Log the activity
            ActivityLog.log_activity(user_data[0], 'LOGIN', f'User {username} logged in')
            
            conn.close()
            
            # Return User object
            return User(*user_data)
        
        conn.close()
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, username, email, password_hash, user_type, first_name, last_name, 
                   created_at, last_login, is_active
            FROM users WHERE id = ?
        ''', (user_id,))
        
        user_data = c.fetchone()
        conn.close()
        
        if user_data:
            return User(*user_data)
        return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, username, email, password_hash, user_type, first_name, last_name, 
                   created_at, last_login, is_active
            FROM users WHERE username = ?
        ''', (username,))
        
        user_data = c.fetchone()
        conn.close()
        
        if user_data:
            return User(*user_data)
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, username, email, password_hash, user_type, first_name, last_name, 
                   created_at, last_login, is_active
            FROM users WHERE email = ?
        ''', (email,))
        
        user_data = c.fetchone()
        conn.close()
        
        if user_data:
            return User(*user_data)
        return None
    
    def update_password(self, new_password):
        """Update user password"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        new_hash = generate_password_hash(new_password)
        c.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, self.id))
        conn.commit()
        
        # Log the activity
        ActivityLog.log_activity(self.id, 'PASSWORD_CHANGED', 'User changed password')
        
        conn.close()
        self.password_hash = new_hash
    
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type == 'admin'
    
    def is_student(self):
        """Check if user is student"""
        return self.user_type == 'student'
    
    def get_full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'created_at': self.created_at,
            'last_login': self.last_login,
            'is_active': self.is_active,
            'is_admin': self.is_admin(),
            'is_student': self.is_student()
        }

class Textbook:
    """Textbook model for managing educational materials"""
    
    def __init__(self, id=None, filename=None, original_name=None, grade=None, 
                 subject=None, file_type=None, file_size=None, uploaded_by=None, 
                 upload_date=None, description=None, is_active=True):
        self.id = id
        self.filename = filename
        self.original_name = original_name
        self.grade = grade
        self.subject = subject
        self.file_type = file_type
        self.file_size = file_size
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date
        self.description = description
        self.is_active = is_active
    
    @staticmethod
    def create_textbook(filename, original_name, grade, subject, file_type, 
                       file_size, uploaded_by, description=None):
        """Create a new textbook entry"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO textbooks (filename, original_name, grade, subject, file_type, 
                                 file_size, uploaded_by, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (filename, original_name, grade, subject, file_type, file_size, uploaded_by, description))
        
        textbook_id = c.lastrowid
        conn.commit()
        
        # Log the activity
        user = User.get_by_username(uploaded_by)
        if user:
            ActivityLog.log_activity(user.id, 'TEXTBOOK_UPLOADED', 
                                   f'Uploaded {original_name} for Grade {grade} - {subject}')
        
        conn.close()
        return textbook_id
    
    @staticmethod
    def get_by_grade_and_subject(grade, subject):
        """Get textbooks by grade and subject"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, filename, original_name, grade, subject, file_type, 
                   file_size, uploaded_by, upload_date, description, is_active
            FROM textbooks 
            WHERE grade = ? AND subject = ? AND is_active = 1
            ORDER BY upload_date DESC
        ''', (grade, subject))
        
        textbooks = []
        for row in c.fetchall():
            textbooks.append(Textbook(*row))
        
        conn.close()
        return textbooks
    
    @staticmethod
    def get_by_id(textbook_id):
        """Get textbook by ID"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, filename, original_name, grade, subject, file_type, 
                   file_size, uploaded_by, upload_date, description, is_active
            FROM textbooks WHERE id = ?
        ''', (textbook_id,))
        
        textbook_data = c.fetchone()
        conn.close()
        
        if textbook_data:
            return Textbook(*textbook_data)
        return None
    
    @staticmethod
    def get_all_by_grade(grade):
        """Get all textbooks for a specific grade"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, filename, original_name, grade, subject, file_type, 
                   file_size, uploaded_by, upload_date, description, is_active
            FROM textbooks 
            WHERE grade = ? AND is_active = 1
            ORDER BY subject, upload_date DESC
        ''', (grade,))
        
        textbooks = []
        for row in c.fetchall():
            textbooks.append(Textbook(*row))
        
        conn.close()
        return textbooks
    
    def delete(self):
        """Soft delete textbook"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('UPDATE textbooks SET is_active = 0 WHERE id = ?', (self.id,))
        conn.commit()
        
        # Log the activity
        user = User.get_by_username(self.uploaded_by)
        if user:
            ActivityLog.log_activity(user.id, 'TEXTBOOK_DELETED', 
                                   f'Deleted {self.original_name} for Grade {self.grade} - {self.subject}')
        
        conn.close()
        self.is_active = False
    
    def get_file_size_formatted(self):
        """Get formatted file size"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        elif self.file_size < 1024 * 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.file_size / (1024 * 1024 * 1024):.1f} GB"
    
    def to_dict(self):
        """Convert textbook to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'grade': self.grade,
            'subject': self.subject,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'file_size_formatted': self.get_file_size_formatted(),
            'uploaded_by': self.uploaded_by,
            'upload_date': self.upload_date,
            'description': self.description,
            'is_active': self.is_active
        }

class PasswordResetToken:
    """Password reset token model"""
    
    def __init__(self, id=None, user_id=None, token=None, created_at=None, 
                 expires_at=None, used=False):
        self.id = id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at
        self.expires_at = expires_at
        self.used = used
    
    @staticmethod
    def create_token(user_id, expires_in_hours=24):
        """Create a password reset token"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        c.execute('''
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, token, expires_at))
        
        token_id = c.lastrowid
        conn.commit()
        
        # Log the activity
        ActivityLog.log_activity(user_id, 'PASSWORD_RESET_REQUESTED', 'Password reset token created')
        
        conn.close()
        return token
    
    @staticmethod
    def get_valid_token(token):
        """Get valid (unused and not expired) token"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, user_id, token, created_at, expires_at, used
            FROM password_reset_tokens 
            WHERE token = ? AND used = 0 AND expires_at > CURRENT_TIMESTAMP
        ''', (token,))
        
        token_data = c.fetchone()
        conn.close()
        
        if token_data:
            return PasswordResetToken(*token_data)
        return None
    
    def mark_as_used(self):
        """Mark token as used"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('UPDATE password_reset_tokens SET used = 1 WHERE id = ?', (self.id,))
        conn.commit()
        
        # Log the activity
        ActivityLog.log_activity(self.user_id, 'PASSWORD_RESET_COMPLETED', 'Password reset token used')
        
        conn.close()
        self.used = True

class ActivityLog:
    """Activity logging model"""
    
    def __init__(self, id=None, user_id=None, action=None, details=None, 
                 ip_address=None, timestamp=None):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.details = details
        self.ip_address = ip_address
        self.timestamp = timestamp
    
    @staticmethod
    def log_activity(user_id, action, details=None, ip_address=None):
        """Log user activity"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO activity_log (user_id, action, details, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (user_id, action, details, ip_address))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_activities(user_id, limit=50):
        """Get user activities"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT id, user_id, action, details, ip_address, timestamp
            FROM activity_log 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        activities = []
        for row in c.fetchall():
            activities.append(ActivityLog(*row))
        
        conn.close()
        return activities
    
    @staticmethod
    def get_recent_activities(limit=100):
        """Get recent activities (admin only)"""
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT al.id, al.user_id, al.action, al.details, al.ip_address, al.timestamp,
                   u.username, u.user_type
            FROM activity_log al
            LEFT JOIN users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        activities = []
        for row in c.fetchall():
            activity = ActivityLog(row[0], row[1], row[2], row[3], row[4], row[5])
            activity.username = row[6]
            activity.user_type = row[7]
            activities.append(activity)
        
        conn.close()
        return activities

# Utility functions
def get_subjects():
    """Get list of all subjects"""
    return [
        'Mathematics',
        'English', 
        'Science',
        'Social Studies',
        'Hindi',
        'Computer Science',
        'Art',
        'Physical Education'
    ]

def get_grades():
    """Get list of all grades"""
    return list(range(1, 11))  # Grades 1-10

def get_textbook_stats():
    """Get textbook statistics"""
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Total textbooks
    c.execute('SELECT COUNT(*) FROM textbooks WHERE is_active = 1')
    total_textbooks = c.fetchone()[0]
    
    # Textbooks by grade
    c.execute('''
        SELECT grade, COUNT(*) 
        FROM textbooks 
        WHERE is_active = 1 
        GROUP BY grade 
        ORDER BY grade
    ''')
    by_grade = dict(c.fetchall())
    
    # Textbooks by subject
    c.execute('''
        SELECT subject, COUNT(*) 
        FROM textbooks 
        WHERE is_active = 1 
        GROUP BY subject 
        ORDER BY COUNT(*) DESC
    ''')
    by_subject = dict(c.fetchall())
    
    conn.close()
    
    return {
        'total': total_textbooks,
        'by_grade': by_grade,
        'by_subject': by_subject
    }

def get_user_stats():
    """Get user statistics"""
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Total users
    c.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
    total_users = c.fetchone()[0]
    
    # Users by type
    c.execute('''
        SELECT user_type, COUNT(*) 
        FROM users 
        WHERE is_active = 1 
        GROUP BY user_type
    ''')
    by_type = dict(c.fetchall())
    
    conn.close()
    
    return {
        'total': total_users,
        'by_type': by_type
    }