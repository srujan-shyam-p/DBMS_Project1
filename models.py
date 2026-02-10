"""
Database Models for Open Course Management Platform
Using SQLAlchemy ORM with PostgreSQL
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Central identity store for all users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, instructor, admin, analyst
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    enrolled_courses = db.relationship('Enrollment', back_populates='student', lazy=True)
    taught_courses = db.relationship('Course', back_populates='instructor', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Course(db.Model):
    """Course entity - represents educational products"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    thumbnail_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    instructor = db.relationship('User', back_populates='taught_courses')
    modules = db.relationship('CourseModule', back_populates='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.title}>'


class CourseModule(db.Model):
    """Course content modules - videos, text, etc."""
    __tablename__ = 'course_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    content_type = db.Column(db.String(10), nullable=False)  # video, text
    content_body = db.Column(db.Text)  # HTML text or Video URL
    sequence = db.Column(db.Integer, nullable=False)
    
    # Relationships
    course = db.relationship('Course', back_populates='modules')
    
    def __repr__(self):
        return f'<Module {self.title}>'


class Enrollment(db.Model):
    """Junction table linking students to courses"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)  # 0-100
    grade = db.Column(db.Numeric(5, 2))
    
    # Relationships
    student = db.relationship('User', back_populates='enrolled_courses')
    course = db.relationship('Course', back_populates='enrollments')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)
    
    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'
