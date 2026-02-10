"""
Database Initialization Script
Creates tables and populates with sample data for testing
"""

from app import app, db
from models import User, Course, CourseModule, Enrollment
from datetime import datetime, timedelta

def init_database():
    """Initialize database with schema and sample data"""
    
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating new tables...")
        db.create_all()
        
        print("Adding sample data...")
        
        # Create demo users
        users = []
        
        # Admin user
        admin = User(
            username='admin',
            email='admin@demo.com',
            role='admin',
            created_at=datetime.utcnow() - timedelta(days=180)
        )
        admin.set_password('password')
        users.append(admin)
        
        # Analyst user
        analyst = User(
            username='analyst',
            email='analyst@demo.com',
            role='analyst',
            created_at=datetime.utcnow() - timedelta(days=150)
        )
        analyst.set_password('password')
        users.append(analyst)
        
        # Instructor users
        instructor1 = User(
            username='Dr. Sarah Chen',
            email='instructor@demo.com',
            role='instructor',
            created_at=datetime.utcnow() - timedelta(days=120)
        )
        instructor1.set_password('password')
        users.append(instructor1)
        
        instructor2 = User(
            username='Prof. James Wilson',
            email='james.wilson@demo.com',
            role='instructor',
            created_at=datetime.utcnow() - timedelta(days=100)
        )
        instructor2.set_password('password')
        users.append(instructor2)
        
        # Student users
        students = [
            ('student', 'student@demo.com', 90),
            ('Alice Johnson', 'alice@demo.com', 80),
            ('Bob Smith', 'bob@demo.com', 70),
            ('Carol Davis', 'carol@demo.com', 60),
            ('David Brown', 'david@demo.com', 50),
        ]
        
        for username, email, days_ago in students:
            student = User(
                username=username,
                email=email,
                role='student',
                created_at=datetime.utcnow() - timedelta(days=days_ago)
            )
            student.set_password('password')
            users.append(student)
        
        # Add all users to session
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(users)} users")
        
        # Create sample courses
        courses_data = [
            {
                'title': 'Introduction to Python Programming',
                'description': 'Learn Python from scratch. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming. Perfect for beginners!',
                'category': 'Computer Science',
                'instructor': instructor1,
                'status': 'published'
            },
            {
                'title': 'Data Science with Python',
                'description': 'Master data analysis, visualization, and machine learning using Python. Learn pandas, numpy, matplotlib, and scikit-learn through hands-on projects.',
                'category': 'Data Science',
                'instructor': instructor1,
                'status': 'published'
            },
            {
                'title': 'Web Development Fundamentals',
                'description': 'Build modern websites with HTML, CSS, and JavaScript. Learn responsive design, DOM manipulation, and best practices for web development.',
                'category': 'Computer Science',
                'instructor': instructor2,
                'status': 'published'
            },
            {
                'title': 'Machine Learning Basics',
                'description': 'Introduction to machine learning algorithms and techniques. Covers supervised learning, unsupervised learning, and neural networks.',
                'category': 'Data Science',
                'instructor': instructor2,
                'status': 'published'
            },
            {
                'title': 'Database Design and SQL',
                'description': 'Learn relational database design, normalization, and SQL queries. Master PostgreSQL and database optimization techniques.',
                'category': 'Computer Science',
                'instructor': instructor1,
                'status': 'draft'
            },
        ]
        
        courses = []
        for course_data in courses_data:
            course = Course(
                title=course_data['title'],
                description=course_data['description'],
                category=course_data['category'],
                instructor_id=course_data['instructor'].id,
                status=course_data['status'],
                created_at=datetime.utcnow() - timedelta(days=60)
            )
            db.session.add(course)
            courses.append(course)
        
        db.session.commit()
        print(f"Created {len(courses)} courses")
        
        # Add modules to published courses
        python_course = courses[0]
        modules_python = [
            {
                'title': 'Week 1: Introduction to Python',
                'content_type': 'text',
                'content_body': '''<h2>Welcome to Python Programming!</h2>
                <p>Python is a versatile, high-level programming language known for its simplicity and readability. In this module, we'll cover:</p>
                <ul>
                    <li>What is Python and why learn it?</li>
                    <li>Installing Python and setting up your environment</li>
                    <li>Writing your first Python program</li>
                    <li>Basic syntax and structure</li>
                </ul>
                <p><strong>By the end of this week, you'll be able to:</strong></p>
                <ul>
                    <li>Install Python on your computer</li>
                    <li>Use the Python interpreter and IDE</li>
                    <li>Write and run simple Python programs</li>
                </ul>''',
                'sequence': 1
            },
            {
                'title': 'Week 2: Variables and Data Types',
                'content_type': 'video',
                'content_body': 'https://www.youtube.com/embed/rfscVS0vtbw',
                'sequence': 2
            },
            {
                'title': 'Week 3: Control Structures',
                'content_type': 'text',
                'content_body': '''<h2>Control Flow in Python</h2>
                <p>Control structures allow you to control the flow of your program's execution. This week covers:</p>
                <ul>
                    <li>If statements and conditional logic</li>
                    <li>For loops and while loops</li>
                    <li>Break and continue statements</li>
                    <li>Nested control structures</li>
                </ul>''',
                'sequence': 3
            },
        ]
        
        for module_data in modules_python:
            module = CourseModule(
                course_id=python_course.id,
                title=module_data['title'],
                content_type=module_data['content_type'],
                content_body=module_data['content_body'],
                sequence=module_data['sequence']
            )
            db.session.add(module)
        
        # Add modules to web dev course
        web_course = courses[2]
        modules_web = [
            {
                'title': 'Module 1: HTML Basics',
                'content_type': 'text',
                'content_body': '''<h2>Introduction to HTML</h2>
                <p>HTML (HyperText Markup Language) is the foundation of all web pages. Learn the essential tags and structure.</p>''',
                'sequence': 1
            },
            {
                'title': 'Module 2: CSS Styling',
                'content_type': 'text',
                'content_body': '''<h2>Styling with CSS</h2>
                <p>CSS (Cascading Style Sheets) makes websites beautiful. Master selectors, properties, and responsive design.</p>''',
                'sequence': 2
            },
        ]
        
        for module_data in modules_web:
            module = CourseModule(
                course_id=web_course.id,
                title=module_data['title'],
                content_type=module_data['content_type'],
                content_body=module_data['content_body'],
                sequence=module_data['sequence']
            )
            db.session.add(module)
        
        db.session.commit()
        print("Added course modules")
        
        # Create enrollments
        student_users = User.query.filter_by(role='student').all()
        published_courses = Course.query.filter_by(status='published').all()
        
        enrollments = []
        for i, student in enumerate(student_users):
            # Each student enrolls in 1-3 courses
            num_enrollments = min(i + 1, 3)
            for j in range(num_enrollments):
                if j < len(published_courses):
                    enrollment = Enrollment(
                        student_id=student.id,
                        course_id=published_courses[j].id,
                        enrolled_at=datetime.utcnow() - timedelta(days=30-i*5),
                        progress=(i+1) * 20 % 100,  # Varying progress
                        grade=85.5 + i * 2 if (i+1) * 20 % 100 == 0 else None
                    )
                    enrollments.append(enrollment)
                    db.session.add(enrollment)
        
        db.session.commit()
        print(f"Created {len(enrollments)} enrollments")
        
        print("\n✅ Database initialized successfully!")
        print("\n📝 Demo Account Credentials:")
        print("   Admin:      admin@demo.com / password")
        print("   Analyst:    analyst@demo.com / password")
        print("   Instructor: instructor@demo.com / password")
        print("   Student:    student@demo.com / password")
        print("\n🚀 Run 'python app.py' to start the server")


if __name__ == '__main__':
    init_database()
