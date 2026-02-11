"""
Database Utility Functions (Data Access Layer)
All raw SQL queries live here.
"""
from sqlalchemy import text
from datetime import datetime

# ================= USER & AUTH =================

def get_user_by_email(session, email):
    """Fetch user basic details by email."""
    # ALIAS: user_id -> id, name -> username
    query = text("SELECT user_id as id, name as username, email, password FROM users WHERE email = :email")
    return session.execute(query, {'email': email}).fetchone()

def get_user_role(session, user_id):
    """Check child tables to find the user's role."""
    if session.execute(text("SELECT 1 FROM student WHERE user_id = :id"), {'id': user_id}).fetchone(): return 'student'
    elif session.execute(text("SELECT 1 FROM instructor WHERE user_id = :id"), {'id': user_id}).fetchone(): return 'instructor'
    elif session.execute(text("SELECT 1 FROM administrator WHERE user_id = :id"), {'id': user_id}).fetchone(): return 'admin'
    elif session.execute(text("SELECT 1 FROM data_analyst WHERE user_id = :id"), {'id': user_id}).fetchone(): return 'analyst'
    return None

def check_email_exists(session, email):
    """Return True if email exists."""
    return session.execute(text("SELECT 1 FROM users WHERE email = :email"), {'email': email}).fetchone() is not None

def create_user(session, name, email, hashed_password, phonenumber=None):
    """Insert into parent users table."""
    # Get next ID
    uid = session.execute(text("SELECT COALESCE(MAX(user_id), 0) + 1 FROM users")).scalar()
    
    query = text("""
        INSERT INTO users (user_id, name, email, password, phonenumber, age) 
        VALUES (:uid, :name, :email, :pwd, :phone, 0)
    """)
    session.execute(query, {'uid': uid, 'name': name, 'email': email, 'pwd': hashed_password, 'phone': phonenumber})
    return uid

def assign_role(session, user_id, role):
    """Insert into appropriate child table."""
    if role == 'student':
        sid = session.execute(text("SELECT COALESCE(MAX(student_id), 0) + 1 FROM student")).scalar()
        session.execute(text("INSERT INTO student (student_id, user_id) VALUES (:sid, :uid)"), {'sid': sid, 'uid': user_id})
    elif role == 'instructor':
        iid = session.execute(text("SELECT COALESCE(MAX(instructor_id), 0) + 1 FROM instructor")).scalar()
        session.execute(text("INSERT INTO instructor (instructor_id, user_id, salary, experience, avg_rating) VALUES (:iid, :uid, 0, 0, 0.0)"), 
                       {'iid': iid, 'uid': user_id})
    # Add other roles as needed

# ================= COURSES (General) =================

def get_all_published_courses(session):
    """Get all courses for the catalog."""
    query = text("""
        SELECT course_id as id, course_name as title, category, 
               'No description available' as description, 'published' as status 
        FROM courses
    """)
    return session.execute(query).fetchall()

def get_course_by_id(session, course_id):
    """Get single course details."""
    query = text("SELECT course_id as id, course_name as title, category, 'No description' as description FROM courses WHERE course_id = :id")
    return session.execute(query, {'id': course_id}).fetchone()

# ================= STUDENT =================

def get_student_stats(session, user_id):
    """Calculate statistics for student dashboard."""
    # 1. Total Enrolled
    enrolled = session.execute(text("SELECT COUNT(*) FROM enrolls_in WHERE user_id = :uid"), {'uid': user_id}).scalar()
    
    # 2. Completed (status = 'completed')
    completed = session.execute(text("SELECT COUNT(*) FROM enrolls_in WHERE user_id = :uid AND completion_status = 'completed'"), {'uid': user_id}).scalar()
    
    # 3. Active (status = 'ongoing')
    active = session.execute(text("SELECT COUNT(*) FROM enrolls_in WHERE user_id = :uid AND completion_status = 'ongoing'"), {'uid': user_id}).scalar()
    
    return {
        'enrolled': enrolled,
        'completed': completed,
        'active': active
    }

def get_student_enrollments(session, user_id):
    """Get courses a student is enrolled in."""
    query = text("""
        SELECT e.enrollment_id, e.completion_status, e.grade, e.percent_completed,
               c.course_id as id, c.course_name as title, c.category,
               'No description available' as description
        FROM enrolls_in e
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def get_user_by_id(session, user_id):
    """Fetch user object by ID."""
    return session.execute(text("SELECT * FROM users WHERE user_id = :uid"), {'uid': user_id}).fetchone()

def check_enrollment(session, user_id, course_id):
    """Check if student is already enrolled."""
    return session.execute(text("SELECT 1 FROM enrolls_in WHERE user_id = :uid AND course_id = :cid"), 
                         {'uid': user_id, 'cid': course_id}).fetchone() is not None

def enroll_student(session, user_id, course_id):
    """Create a new enrollment record."""
    eid = session.execute(text("SELECT COALESCE(MAX(enrollment_id), 0) + 1 FROM enrolls_in")).scalar()
    query = text("""
        INSERT INTO enrolls_in (enrollment_id, course_id, user_id, enrollment_date, completion_status, percent_completed) 
        VALUES (:eid, :cid, :uid, :date, 'ongoing', 0)
    """)
    session.execute(query, {'eid': eid, 'cid': course_id, 'uid': user_id, 'date': datetime.now().date()})

def get_student_reviews(session, user_id):
    """Fetch all reviews made by the student."""
    query = text("""
        SELECT r.rating, r.comments, c.course_name 
        FROM review r
        JOIN courses c ON r.course_id = c.course_id
        WHERE r.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def get_student_quizzes(session, user_id):
    """Fetch quiz attempts for the student."""
    # Note: Schema has Attempt -> Quiz. Quiz doesn't link to Course.
    # We will just show Quiz ID and Score for now.
    query = text("""
        SELECT q.quiz_id, q.total_score, q.duration, q.completion_status
        FROM attempt a
        JOIN quiz q ON a.quiz_id = q.quiz_id
        WHERE a.student_id = (SELECT student_id FROM student WHERE user_id = :uid)
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def get_student_purchases(session, user_id):
    """Fetch payment history."""
    query = text("""
        SELECT transaction_id, invoice_no, amount, currency, date_pay, payment_mode
        FROM payment
        WHERE user_id = :uid
        ORDER BY date_pay DESC
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

# ================= INSTRUCTOR =================

def get_instructor_courses(session, user_id):
    """Get courses taught by this instructor."""
    query = text("""
        SELECT c.course_id as id, c.course_name as title, c.category, 
               'No description' as description,
        (SELECT COUNT(*) FROM enrolls_in e WHERE e.course_id = c.course_id) as enrollment_count
        FROM courses c
        JOIN teaches t ON c.course_id = t.course_id
        JOIN instructor i ON t.instructor_id = i.instructor_id
        WHERE i.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def create_course_with_instructor(session, user_id, title, category):
    """Create course and link to instructor."""
    # 1. Create Course
    cid = session.execute(text("SELECT COALESCE(MAX(course_id), 0) + 1 FROM courses")).scalar()
    session.execute(text("""
        INSERT INTO courses (course_id, course_name, category, creation_date, price, level, language, university_id) 
        VALUES (:cid, :name, :cat, :date, 0, 'Beginner', 'English', 1)
    """), {'cid': cid, 'name': title, 'cat': category, 'date': datetime.now().date()})

    # 2. Find Instructor ID
    iid = session.execute(text("SELECT instructor_id FROM instructor WHERE user_id = :uid"), {'uid': user_id}).scalar()
    
    # 3. Link (Teaches)
    if iid:
        session.execute(text("INSERT INTO teaches (instructor_id, course_id) VALUES (:iid, :cid)"), {'iid': iid, 'cid': cid})
    
    return cid

def get_instructor_stats(session, user_id):
    """Fetch overview stats for the instructor dashboard."""
    # Count courses taught by this instructor
    course_count = session.execute(text("""
        SELECT COUNT(*) FROM teaches t 
        JOIN instructor i ON t.instructor_id = i.instructor_id 
        WHERE i.user_id = :uid
    """), {'uid': user_id}).scalar()
    
    # Count total students across all their courses
    student_count = session.execute(text("""
        SELECT COUNT(e.user_id) FROM enrolls_in e
        JOIN teaches t ON e.course_id = t.course_id
        JOIN instructor i ON t.instructor_id = i.instructor_id
        WHERE i.user_id = :uid
    """), {'uid': user_id}).scalar()

    return {'course_count': course_count, 'student_count': student_count}

def get_instructor_courses(session, user_id):
    """Fetch courses with enrollment counts per course."""
    query = text("""
        SELECT c.course_id as id, c.course_name as title, c.category,
        (SELECT COUNT(*) FROM enrolls_in e WHERE e.course_id = c.course_id) as enrollment_count
        FROM courses c
        JOIN teaches t ON c.course_id = t.course_id
        JOIN instructor i ON t.instructor_id = i.instructor_id
        WHERE i.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def get_instructor_stats(session, user_id):
    """Fetch overview stats for the instructor dashboard."""
    # Count courses taught by this instructor
    course_count = session.execute(text("""
        SELECT COUNT(*) FROM teaches t 
        JOIN instructor i ON t.instructor_id = i.instructor_id 
        WHERE i.user_id = :uid
    """), {'uid': user_id}).scalar()
    
    # Count total students across all their courses
    student_count = session.execute(text("""
        SELECT COUNT(e.user_id) FROM enrolls_in e
        JOIN teaches t ON e.course_id = t.course_id
        JOIN instructor i ON t.instructor_id = i.instructor_id
        WHERE i.user_id = :uid
    """), {'uid': user_id}).scalar()

    return {'course_count': course_count, 'student_count': student_count}
def get_course_full_details(session, course_id):
    # 1. Fetch Course & Lectures (Existing)
    course = session.execute(text("SELECT * FROM courses WHERE course_id = :id"), {'id': course_id}).fetchone()
    rows = session.execute(text("""
        SELECT m.module_id, m.title as module_title, l.lecture_id, l.title as lecture_title, l.videos_link, l.duration
        FROM module m
        LEFT JOIN lectures l ON m.module_id = l.module_id
        WHERE m.course_id = :id ORDER BY m.module_id, l.lecture_id
    """), {'id': course_id}).fetchall()
    
    # 2. Fetch Materials
    materials = session.execute(text("SELECT * FROM course_material WHERE course_id = :id"), {'id': course_id}).fetchall()
    
    # 3. Fetch Quizzes
    quizzes = session.execute(text("SELECT * FROM quiz")).fetchall() 
    
    return course, rows, materials, quizzes

def add_module_to_course(session, course_id, title):
    """Insert a new module into the module table."""
    mid = session.execute(text("SELECT COALESCE(MAX(module_id), 0) + 1 FROM module")).scalar()
    session.execute(text("INSERT INTO module (module_id, course_id, title) VALUES (:mid, :cid, :title)"),
                   {'mid': mid, 'cid': course_id, 'title': title})

def add_lecture_to_module(session, module_id, title, video_link, duration):
    """Insert a new lecture linked to a specific module."""
    # Generate next ID
    lid = session.execute(text("SELECT COALESCE(MAX(lecture_id), 0) + 1 FROM lectures")).scalar()
    
    query = text("""
        INSERT INTO lectures (lecture_id, title, videos_link, duration, module_id) 
        VALUES (:lid, :title, :link, :dur, :mid)
    """)
    session.execute(query, {
        'lid': lid, 
        'title': title, 
        'link': video_link, 
        'dur': duration, 
        'mid': module_id
    })
def get_instructor_catalog(session, user_id):
    """Fetch only courses taught by the logged-in instructor."""
    query = text("""
        SELECT c.course_id as id, c.course_name as title, c.category, 
               'Owned by you' as description, 'published' as status 
        FROM courses c
        JOIN teaches t ON c.course_id = t.course_id
        JOIN instructor i ON t.instructor_id = i.instructor_id
        WHERE i.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchall()

def add_course_material(session, course_id, title, material_type, file_link):
    """Insert into course_material table (PDFs, Textbooks)."""
    mid = session.execute(text("SELECT COALESCE(MAX(material_id), 0) + 1 FROM course_material")).scalar()
    query = text("""
        INSERT INTO course_material (material_id, course_id, title, material_type, file_link)
        VALUES (:mid, :cid, :title, :mtype, :link)
    """)
    session.execute(query, {'mid': mid, 'cid': course_id, 'title': title, 'mtype': material_type, 'link': file_link})

def add_quiz_to_course(session, course_id, total_score, duration):
    """Insert into quiz table with course context."""
    qid = session.execute(text("SELECT COALESCE(MAX(quiz_id), 0) + 1 FROM quiz")).scalar()
    # If your schema links quizzes to courses, ensure course_id is used here
    query = text("""
        INSERT INTO quiz (quiz_id, total_score, duration, completion_status)
        VALUES (:qid, :score, :dur, 'published')
    """)
    session.execute(query, {'qid': qid, 'score': total_score, 'dur': duration})
    return qid

def add_question_to_quiz(session, quiz_id, question_text, correct_answer):
    """Insert a question into the quiz_questions table."""
    qid = session.execute(text("SELECT COALESCE(MAX(question_id), 0) + 1 FROM quiz_questions")).scalar()
    query = text("""
        INSERT INTO quiz_questions (question_id, quiz_id, question_text, correct_answer)
        VALUES (:qid, :quiz_id, :qtext, :answer)
    """)
    session.execute(query, {'qid': qid, 'quiz_id': quiz_id, 'qtext': question_text, 'answer': correct_answer})

def link_quiz_to_module(session, module_id, quiz_id):
    """Link a quiz to a specific module."""
    query = text("""
        INSERT INTO module_quizzes (module_id, quiz_id)
        VALUES (:mid, :qid)
    """)
    session.execute(query, {'mid': module_id, 'qid': quiz_id})

# ================= ADMIN =================

def get_all_students_with_enrollments(session):
    """
    Fetch all students and their active enrollments.
    Returns: List of rows with user details and course info (if enrolled).
    """
    query = text("""
        SELECT u.user_id, u.name, u.email, 
               e.enrollment_id, c.course_name, c.course_id
        FROM users u
        JOIN student s ON u.user_id = s.user_id
        LEFT JOIN enrolls_in e ON u.user_id = e.user_id
        LEFT JOIN courses c ON e.course_id = c.course_id
        ORDER BY u.name, c.course_name
    """)
    return session.execute(query).fetchall()


def get_all_instructors_details(session):
    """
    Fetch all instructors and the courses they teach.
    """
    # FIX: Changed GROUP_CONCAT to STRING_AGG for PostgreSQL compatibility
    query = text("""
        SELECT u.user_id, u.name, u.email, i.experience,
               STRING_AGG(c.course_name, ', ') as courses_taught
        FROM users u
        JOIN instructor i ON u.user_id = i.user_id
        LEFT JOIN teaches t ON i.instructor_id = t.instructor_id
        LEFT JOIN courses c ON t.course_id = c.course_id
        GROUP BY u.user_id, u.name, u.email, i.experience
    """)
    return session.execute(query).fetchall()
def delete_enrollment(session, enrollment_id):
    """
    Admin action: Unenroll a student from a course.
    """
    query = text("DELETE FROM enrolls_in WHERE enrollment_id = :eid")
    session.execute(query, {'eid': enrollment_id})
# ... (Keep existing code) ...

# ================= ADMIN HELPERS =================

def get_student_list(session):
    """Fetch distinct list of students for dropdowns."""
    query = text("SELECT u.user_id, u.name FROM users u JOIN student s ON u.user_id = s.user_id ORDER BY u.name")
    return session.execute(query).fetchall()

def get_course_list(session):
    """Fetch list of courses for dropdowns."""
    query = text("SELECT course_id, course_name FROM courses ORDER BY course_name")
    return session.execute(query).fetchall()

def get_all_analysts(session):
    """
    Fetch all data analysts.
    """
    query = text("""
        SELECT u.user_id, u.name, u.email, u.phonenumber
        FROM users u
        JOIN data_analyst da ON u.user_id = da.user_id
    """)
    return session.execute(query).fetchall()
def get_analyst_by_id(session, user_id):
    """Fetch full details for a specific data analyst."""
    query = text("""
        SELECT u.user_id, u.name, u.email, u.phonenumber, u.age, u.password,
               'Data Analyst' as role
        FROM users u
        JOIN data_analyst da ON u.user_id = da.user_id
        WHERE u.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchone()
def get_admin_details(session, user_id):
    """Fetch full details for the logged-in administrator."""
    query = text("""
        SELECT u.user_id, u.name, u.email, u.phonenumber, u.age,
               a.admin_id, a.salary
        FROM users u
        JOIN administrator a ON u.user_id = a.user_id
        WHERE u.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchone()
def get_admin_details(session, user_id):
    """Fetch full details for the logged-in administrator."""
    query = text("""
        SELECT u.user_id, u.name, u.email, u.phonenumber, u.age,
               a.admin_id, a.salary
        FROM users u
        JOIN administrator a ON u.user_id = a.user_id
        WHERE u.user_id = :uid
    """)
    return session.execute(query, {'uid': user_id}).fetchone()
