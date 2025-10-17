# Brilliant Childrens Academy - Complete School Website

![School Website](https://img.shields.io/badge/Status-Complete-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

## 🏫 Overview

A comprehensive school website for **Brilliant Childrens Academy** built with Flask, featuring a complete learning management system with dual authentication, textbook management, and administrative controls.

## ✨ Features

### 🔐 **Dual Authentication System**
- **Admin Login**: Full administrative access with upload/delete capabilities
- **Student Login**: Student access to textbooks and resources
- **Password Reset**: Forgot password functionality for both user types
- **Secure Sessions**: Session management with password hashing

### 📚 **Textbook Management System**
- **Grades 1-10**: Complete coverage of all grade levels
- **8 Subjects per Grade**: Mathematics, English, Science, Social Studies, Hindi, Computer Science, Art, Physical Education
- **Multi-format Support**: PDF, DOC, DOCX, JPG, PNG, TXT, XLS, XLSX files
- **File Upload**: Admin can upload textbooks up to 500MB
- **File Management**: Admin can delete textbooks
- **Organized Structure**: Easy navigation by grade and subject

### 🎨 **Beautiful User Interface**
- **Responsive Design**: Works on all devices (desktop, tablet, mobile)
- **Modern Styling**: Bootstrap 5 with custom CSS
- **Animated Elements**: Smooth transitions and hover effects
- **Professional Layout**: Clean and intuitive design

### 🖼️ **Photo Gallery**
- **School Activities**: Animated display of school events
- **Random Movement**: Dynamic photo presentation
- **Activity Categories**: Music Concert, Drama Performance, Field Trip, Science Lab, Sports Day, Art Exhibition

### 📄 **Additional Pages**
- **About Page**: School information and mission
- **Contact Us**: Contact details and inquiry form
- **Location**: School address and map information

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone https://github.com/vineethkurapati/brilliant-childrens-academy.git
cd brilliant-childrens-academy
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python database.py
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## 👥 Default Login Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **Capabilities**: Upload/delete textbooks, full system access

### Student Access
- **Username**: `student`
- **Password**: `student123`
- **Capabilities**: View textbooks, access learning materials

## 📁 Project Structure

```
brilliant-childrens-academy/
├── app.py                 # Main Flask application
├── database.py           # Database initialization
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js      # JavaScript functionality
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── login.html       # Login page
│   ├── textbooks.html   # Textbook listing
│   ├── grade_textbooks.html # Grade-specific textbooks
│   ├── about.html       # About page
│   ├── contact.html     # Contact page
│   ├── location.html    # Location page
│   └── reset_password.html # Password reset
└── uploads/             # Uploaded textbook files
```

## 🛠️ Technologies Used

- **Backend**: Flask 2.3.3 (Python web framework)
- **Database**: SQLite (lightweight database)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5.3, Font Awesome icons
- **Security**: Werkzeug password hashing
- **File Handling**: Secure file upload with validation

## 🔧 Configuration

### File Upload Settings
- **Maximum File Size**: 500MB
- **Allowed Extensions**: PDF, DOC, DOCX, JPG, JPEG, PNG, TXT, XLS, XLSX
- **Upload Directory**: `uploads/textbooks/`

### Security Features
- Password hashing using Werkzeug
- Session management
- File type validation
- SQL injection protection
- XSS protection

## 📱 Responsive Design

The website is fully responsive and works seamlessly on:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface for smartphones

## 🎯 Key Functionalities

1. **User Authentication**: Secure login system with role-based access
2. **File Management**: Upload, download, and delete textbooks
3. **Grade Organization**: Structured content by grade levels (1-10)
4. **Subject Categories**: 8 subjects per grade level
5. **Admin Controls**: Administrative interface for content management
6. **Password Recovery**: Reset password functionality
7. **Activity Gallery**: Visual showcase of school activities

## 🚀 Deployment

For production deployment, consider:

1. **Environment Variables**: Set up production configuration
2. **Database**: Migrate to PostgreSQL or MySQL for production
3. **Web Server**: Use Gunicorn with Nginx
4. **SSL Certificate**: Enable HTTPS for security
5. **File Storage**: Consider cloud storage for uploaded files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Vineeth Kurapati**
- GitHub: [@vineethkurapati](https://github.com/vineethkurapati)

## 🙏 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Font Awesome for the beautiful icons
- Flask community for the amazing web framework
- SQLite for the reliable database engine

---

**🎓 Empowering young minds through quality education and innovative learning experiences**