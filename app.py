"""
Main Flask Application for Open Course Management Platform
Handles routing, authentication, and role-based access control
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from models import db, User, Course, CourseModule, Enrollment
from datetime import datetime
from sqlalchemy import func
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Thilok:thilok@localhost/opencourse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ==================== DECORATORS ====================

def login_required(f):
    """Require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """Require specific user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if user.role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Role-based redirect
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'instructor':
                return redirect(url_for('instructor_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_panel'))
            elif user.role == 'analyst':
                return redirect(url_for('analyst_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
            return redirect(url_for('register'))
        
        # Create new user (default role: student)
        user = User(username=username, email=email, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    """Student dashboard showing enrolled courses"""
    user = User.query.get(session['user_id'])
    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    return render_template('student_dashboard.html', enrollments=enrollments)


@app.route('/student/catalog')
@login_required
@role_required('student')
def student_catalog():
    """Course catalog for students"""
    courses = Course.query.filter_by(status='published').all()
    return render_template('student_catalog.html', courses=courses)


@app.route('/student/enroll/<int:course_id>', methods=['POST'])
@login_required
@role_required('student')
def enroll_course(course_id):
    """Enroll in a course"""
    user_id = session['user_id']
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if existing:
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('student_catalog'))
    
    enrollment = Enrollment(student_id=user_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    
    flash('Successfully enrolled in course!', 'success')
    return redirect(url_for('student_dashboard'))


@app.route('/student/course/<int:course_id>')
@login_required
@role_required('student')
def view_course(course_id):
    """View course content"""
    enrollment = Enrollment.query.filter_by(
        student_id=session['user_id'], 
        course_id=course_id
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'danger')
        return redirect(url_for('student_catalog'))
    
    course = Course.query.get(course_id)
    modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.sequence).all()
    
    return render_template('student_course_view.html', course=course, modules=modules, enrollment=enrollment)


# ==================== INSTRUCTOR ROUTES ====================

@app.route('/instructor/dashboard')
@login_required
@role_required('instructor')
def instructor_dashboard():
    """Instructor dashboard"""
    user = User.query.get(session['user_id'])
    courses = Course.query.filter_by(instructor_id=user.id).all()
    
    # Add enrollment count to each course
    for course in courses:
        course.enrollment_count = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('instructor_dashboard.html', courses=courses)


@app.route('/instructor/course/create', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def create_course():
    """Create new course"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        
        course = Course(
            title=title,
            description=description,
            category=category,
            instructor_id=session['user_id'],
            status='draft'
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Course created successfully!', 'success')
        return redirect(url_for('instructor_dashboard'))
    
    return render_template('instructor_create_course.html')


@app.route('/instructor/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def edit_course(course_id):
    """Edit course content"""
    course = Course.query.get_or_404(course_id)
    
    # Check ownership
    if course.instructor_id != session['user_id']:
        flash('You do not have permission to edit this course.', 'danger')
        return redirect(url_for('instructor_dashboard'))
    
    if request.method == 'POST':
        course.title = request.form.get('title')
        course.description = request.form.get('description')
        course.category = request.form.get('category')
        course.status = request.form.get('status')
        db.session.commit()
        
        flash('Course updated successfully!', 'success')
        return redirect(url_for('instructor_dashboard'))
    
    modules = CourseModule.query.filter_by(course_id=course_id).order_by(CourseModule.sequence).all()
    return render_template('instructor_edit_course.html', course=course, modules=modules)


@app.route('/instructor/course/<int:course_id>/module/add', methods=['POST'])
@login_required
@role_required('instructor')
def add_module(course_id):
    """Add module to course"""
    course = Course.query.get_or_404(course_id)
    
    if course.instructor_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    title = request.form.get('title')
    content_type = request.form.get('content_type')
    content_body = request.form.get('content_body')
    
    # Get next sequence number
    max_seq = db.session.query(func.max(CourseModule.sequence)).filter_by(course_id=course_id).scalar()
    sequence = (max_seq or 0) + 1
    
    module = CourseModule(
        course_id=course_id,
        title=title,
        content_type=content_type,
        content_body=content_body,
        sequence=sequence
    )
    db.session.add(module)
    db.session.commit()
    
    flash('Module added successfully!', 'success')
    return redirect(url_for('edit_course', course_id=course_id))


# ==================== ADMIN ROUTES ====================

@app.route('/admin/panel')
@login_required
@role_required('admin')
def admin_panel():
    """Admin control panel"""
    users = User.query.all()
    courses = Course.query.all()
    return render_template('admin_panel.html', users=users, courses=courses)


@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting self
    if user.id == session['user_id']:
        flash('You cannot delete yourself!', 'danger')
        return redirect(url_for('admin_panel'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} deleted successfully.', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/admin/user/<int:user_id>/role', methods=['POST'])
@login_required
@role_required('admin')
def change_role(user_id):
    """Change user role"""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role in ['student', 'instructor', 'admin', 'analyst']:
        user.role = new_role
        db.session.commit()
        flash(f'Role updated to {new_role} for {user.username}.', 'success')
    else:
        flash('Invalid role specified.', 'danger')
    
    return redirect(url_for('admin_panel'))


# ==================== ANALYST ROUTES ====================

@app.route('/analyst/dashboard')
@login_required
@role_required('analyst')
def analyst_dashboard():
    """Data analyst dashboard with statistics"""
    return render_template('analyst_dashboard.html')


@app.route('/api/stats')
@login_required
@role_required('analyst')
def get_stats():
    """API endpoint for statistics data"""
    
    # Total counts
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    # Enrollments by category
    category_stats = db.session.query(
        Course.category,
        func.count(Enrollment.id).label('count')
    ).join(Enrollment).group_by(Course.category).all()
    
    # Enrollment trends (by month)
    enrollment_trends = db.session.query(
        func.date_trunc('month', Enrollment.enrolled_at).label('month'),
        func.count(Enrollment.id).label('count')
    ).group_by('month').order_by('month').all()
    
    # User role distribution
    role_stats = db.session.query(
        User.role,
        func.count(User.id).label('count')
    ).group_by(User.role).all()
    
    return jsonify({
        'totals': {
            'users': total_users,
            'courses': total_courses,
            'enrollments': total_enrollments
        },
        'categories': [{'category': c, 'count': count} for c, count in category_stats],
        'trends': [{'month': str(m), 'count': count} for m, count in enrollment_trends],
        'roles': [{'role': r, 'count': count} for r, count in role_stats]
    })


# ==================== API ROUTES ====================

@app.route('/api/courses/search')
@login_required
def search_courses():
    """Search courses API"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    courses_query = Course.query.filter_by(status='published')
    
    if query:
        courses_query = courses_query.filter(
            Course.title.ilike(f'%{query}%') | 
            Course.description.ilike(f'%{query}%')
        )
    
    if category:
        courses_query = courses_query.filter_by(category=category)
    
    courses = courses_query.all()
    
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'category': c.category,
        'instructor': c.instructor.username
    } for c in courses])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
