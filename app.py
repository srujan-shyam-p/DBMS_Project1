"""
Main Flask Application - Final Version
Implements all roles: Student, Instructor, Admin, and Analyst.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Data Access Layer
import db_utils

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/opencourse')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session: return redirect(url_for('login'))
            if session.get('role') != required_role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db_utils.get_user_by_email(db.session, email)
        
        if user and check_password_hash(user.password, password):
            role = db_utils.get_user_role(db.session, user.id)
            if role:
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = role
                
                if role == 'student': return redirect(url_for('student_dashboard'))
                elif role == 'instructor': return redirect(url_for('instructor_dashboard'))
                elif role == 'admin': return redirect(url_for('admin_panel'))
                elif role == 'analyst': return redirect(url_for('analyst_dashboard'))
            else:
                flash('No role assigned.', 'danger')
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('full_name') or request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        role = request.form.get('role', 'student') 
        hashed_password = generate_password_hash(password)
        
        if db_utils.check_email_exists(db.session, email):
            flash('Email taken.', 'danger')
            return redirect(url_for('register'))
        
        try:
            uid = db_utils.create_user(db.session, name, email, hashed_password, phonenumber=phone)
            db_utils.assign_role(db.session, uid, role)
            db.session.commit()
            flash('Registered! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error registering.', 'danger')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    enrollments = db_utils.get_student_enrollments(db.session, session['user_id'])
    stats = db_utils.get_student_stats(db.session, session['user_id'])
    return render_template('user.html', enrollments=enrollments, stats=stats)

@app.route('/student/catalog')
@login_required
def student_catalog():
    user_role = session.get('role')
    user_id = session.get('user_id')
    
    if user_role == 'instructor':
        published_courses = db_utils.get_instructor_catalog(db.session, user_id)
    else:
        published_courses = db_utils.get_all_published_courses(db.session)
        
    return render_template('courses.html', courses=published_courses)

@app.route('/student/enroll/<int:course_id>', methods=['POST'])
@login_required
@role_required('student')
def enroll_course(course_id):
    user_id = session['user_id']
    if db_utils.check_enrollment(db.session, user_id, course_id):
        flash('Already enrolled.', 'info')
        return redirect(url_for('student_catalog'))
    
    db_utils.enroll_student(db.session, user_id, course_id)
    db.session.commit()
    flash('Enrolled!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/student/course/<int:course_id>')
@login_required
@role_required('student')
def view_course(course_id):
    # 1. Verify the student is actually enrolled in this course
    if not db_utils.check_enrollment(db.session, session['user_id'], course_id):
        flash('Not enrolled.', 'danger')
        return redirect(url_for('student_catalog'))
    
    # 2. Fetch the complete course package: Info, Curriculum, Materials, and Quizzes
    course, rows, materials, quizzes = db_utils.get_course_full_details(db.session, course_id)
    
    # 3. Safety check if the course ID is invalid
    if not course:
        flash("Course not found.", "danger")
        return redirect(url_for('student_catalog'))
    
    # 4. Render the Student-specific view (NOT the edit page)
    return render_template('course_detail.html', 
                           course=course, 
                           rows=rows, 
                           materials=materials, 
                           quizzes=quizzes)
# ==================== INSTRUCTOR ROUTES ====================

@app.route('/instructor/dashboard')
@login_required
@role_required('instructor')
def instructor_dashboard():
    courses_list = db_utils.get_instructor_courses(db.session, session['user_id'])
    stats = db_utils.get_instructor_stats(db.session, session['user_id'])
    return render_template('instructor.html', courses=courses_list, stats=stats)

@app.route('/instructor/course/create', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def create_course():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        db_utils.create_course_with_instructor(db.session, session['user_id'], title, category)
        db.session.commit()
        flash('Course created!', 'success')
        return redirect(url_for('instructor_dashboard'))
    return render_template('instructor.html')

@app.route('/instructor/course/manage/<int:course_id>', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def manage_course(course_id):
    if request.method == 'POST':
        # 1. Handle Module Addition
        if 'module_title' in request.form:
            db_utils.add_module_to_course(db.session, course_id, request.form.get('module_title'))
            flash('Module added!', 'success')
            
        # 2. Handle Lecture Addition
        elif 'lecture_title' in request.form:
            db_utils.add_lecture_to_module(db.session, request.form.get('module_id'), 
                                         request.form.get('lecture_title'), 
                                         request.form.get('video_link'), 
                                         request.form.get('duration'))
            flash('Lecture added!', 'success')

        # 3. Handle Materials & Textbooks (PDFs/Links)
        elif 'material_title' in request.form:
            db_utils.add_course_material(db.session, course_id, 
                                        request.form.get('material_title'),
                                        request.form.get('material_type'), # 'PDF' or 'Textbook'
                                        request.form.get('file_link'))
            flash('Resource added!', 'success')

        # 4. Handle Quiz Creation
        elif 'total_score' in request.form:
            db_utils.add_quiz_to_course(db.session, course_id,
                                       request.form.get('total_score'),
                                       request.form.get('quiz_duration'))
            flash('Quiz created!', 'success')

        db.session.commit()
        return redirect(url_for('manage_course', course_id=course_id))

    # Apply this change to BOTH manage_course and view_course
    course, rows, materials, quizzes = db_utils.get_course_full_details(db.session, course_id)
    return render_template('edit_course.html', course=course, rows=rows, materials=materials, quizzes=quizzes)
# ==================== ADMIN & ANALYST ROUTES ====================

@app.route('/admin/panel')
@login_required
@role_required('admin')
def admin_panel():
    from sqlalchemy import text
    users = db.session.execute(text("SELECT user_id as id, name as username, email FROM users ORDER BY user_id")).fetchall()
    courses = db.session.execute(text("SELECT course_id as id, course_name as title, category FROM courses ORDER BY course_id")).fetchall()
    return render_template('admin.html', users=users, courses=courses)

@app.route('/analyst/dashboard')
@login_required
@role_required('analyst')
def analyst_dashboard():
    # Use db_utils to get platform enrollment statistics [cite: 39, 43]
    stats = db_utils.get_platform_statistics(db.session)
    return render_template('analyst.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)