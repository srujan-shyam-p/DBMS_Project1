-- =============================================
-- 1. DROP OLD TABLES (Clean Slate)
-- =============================================
DROP TABLE IF EXISTS admin_actions CASCADE;
DROP TABLE IF EXISTS attempt CASCADE;
DROP TABLE IF EXISTS teaches CASCADE;
DROP TABLE IF EXISTS has_module CASCADE;
DROP TABLE IF EXISTS review CASCADE;
DROP TABLE IF EXISTS quiz_questions CASCADE;
DROP TABLE IF EXISTS quiz CASCADE;
DROP TABLE IF EXISTS lectures CASCADE;
DROP TABLE IF EXISTS module_quizzes CASCADE;
DROP TABLE IF EXISTS module CASCADE;
DROP TABLE IF EXISTS course_material CASCADE;
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS payment CASCADE;
DROP TABLE IF EXISTS lesson_progress CASCADE;
DROP TABLE IF EXISTS enrolls_in CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS partner_university CASCADE;
DROP TABLE IF EXISTS data_analyst CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS instructor CASCADE;
DROP TABLE IF EXISTS administrator CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =============================================
-- 2. CREATE TABLE STRUCTURE
-- =============================================

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    phonenumber VARCHAR(20),
    email VARCHAR(50),
    password VARCHAR(255),
    nationality VARCHAR(50),
    age INTEGER
);

CREATE TABLE partner_university (
    university_id INTEGER PRIMARY KEY,
    university_name VARCHAR(50),
    accredation_details VARCHAR(200)
);

CREATE TABLE administrator (
    admin_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    salary NUMERIC(8,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE instructor (
    instructor_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    salary NUMERIC(8,2),
    experience INTEGER,
    avg_rating NUMERIC(2,1),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE data_analyst (
    analyst_id INTEGER PRIMARY KEY,
    salary NUMERIC(8,2),
    experience INTEGER,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name VARCHAR(50),
    creation_date DATE,
    category VARCHAR(20),
    price INTEGER,
    level VARCHAR(20),
    language VARCHAR(20),
    university_id INTEGER,
    FOREIGN KEY (university_id) REFERENCES partner_university(university_id)
);

CREATE TABLE enrolls_in (
    enrollment_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    user_id INTEGER,
    enrollment_date DATE,
    grade VARCHAR(2),
    completion_status VARCHAR(20),
    percent_completed INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE course_material (
    material_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    title VARCHAR(50),
    material_type VARCHAR(20),
    file_link VARCHAR(100),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE module (
    module_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    title VARCHAR(50),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE lectures (
    lecture_id INTEGER PRIMARY KEY,
    videos_link VARCHAR(100),
    duration INTERVAL,
    title VARCHAR(50),
    transcript VARCHAR(200),
    module_id INTEGER,
    FOREIGN KEY (module_id) REFERENCES module(module_id)
);

CREATE TABLE quiz (
    quiz_id INTEGER PRIMARY KEY,
    total_score NUMERIC(5,1),
    duration VARCHAR(20),
    completion_status VARCHAR(20)
);

CREATE TABLE quiz_questions (
    question_id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    question_text TEXT,
    correct_answer TEXT,
    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);

CREATE TABLE teaches (
    instructor_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (instructor_id, course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- =============================================
-- 3. INSERT MOCK DATA
-- =============================================

-- A. UNIVERSITY
INSERT INTO partner_university (university_id, university_name, accredation_details)
VALUES (1, 'OpenTech University', 'A+ Grade Accreditation');

-- B. USERS (Password will be overwritten by init_db.py)
INSERT INTO users (user_id, name, email, password, nationality, age, phonenumber) VALUES 
-- Core Roles
(1, 'Admin User', 'admin@demo.com', 'hashed_later', 'USA', 35, '123-456-7890'),
(2, 'Instructor User', 'instructor@demo.com', 'hashed_later', 'UK', 40, '123-456-7890'),
(3, 'Student User', 'student@demo.com', 'hashed_later', 'India', 21, '123-456-7890'),
(4, 'Analyst User', 'analyst@demo.com', 'hashed_later', 'Canada', 29, '123-456-7890'),

-- NEW INSTRUCTORS
(5, 'Dr. Sarah Connor', 'sarah@demo.com', 'hashed_later', 'USA', 42, '987-654-3210'),
(6, 'Prof. Alan Grant', 'alan@demo.com', 'hashed_later', 'Australia', 50, '555-0199-8888'),

-- NEW STUDENTS
(7, 'Alice Wonderland', 'alice@test.com', 'hashed_later', 'UK', 22, '111-222-3333'),
(8, 'Bob Builder', 'bob@test.com', 'hashed_later', 'Canada', 24, '444-555-6666'),
(9, 'Charlie Chaplin', 'charlie@test.com', 'hashed_later', 'India', 23, '777-888-9999');

-- C. ROLES

-- Admin
INSERT INTO administrator (admin_id, user_id, salary) VALUES (1, 1, 80000.00);

-- Instructors
INSERT INTO instructor (instructor_id, user_id, salary, experience, avg_rating) VALUES 
(1, 2, 60000.00, 10, 4.5),  -- Original Instructor
(2, 5, 75000.00, 8, 4.8),   -- Sarah (New)
(3, 6, 82000.00, 15, 4.6);  -- Alan (New)

-- Analysts
INSERT INTO data_analyst (analyst_id, salary, experience, user_id) VALUES (1, 55000.00, 5, 4);

-- Students
INSERT INTO student (student_id, user_id) VALUES 
(1, 3), -- Original Student
(2, 7), -- Alice
(3, 8), -- Bob
(4, 9); -- Charlie

-- D. COURSES

INSERT INTO courses (course_id, course_name, creation_date, category, price, level, language, university_id) VALUES 
(101, 'Generative AI Masterclass', '2026-01-10', 'AI', 0, 'Intermediate', 'English', 1),
(102, 'Advanced Database Management', '2026-01-15', 'DBMS', 0, 'Advanced', 'English', 1),
(103, 'Natural Language Processing', '2026-02-01', 'AI', 0, 'Advanced', 'English', 1),
-- New Courses
(104, 'Deep Learning with PyTorch', '2026-02-10', 'AI', 0, 'Advanced', 'English', 1),
(105, 'Computer Vision Basics', '2026-02-12', 'AI', 0, 'Beginner', 'English', 1),
(106, 'Algorithms & Complexity', '2026-02-15', 'CS', 0, 'Intermediate', 'English', 1);

-- E. TEACHES (Link Instructors to Courses)

INSERT INTO teaches (instructor_id, course_id) VALUES 
(1, 101), -- Original Instructor teaches GenAI
(1, 102), -- Original Instructor teaches DBMS
(2, 104), -- Sarah teaches Deep Learning
(2, 105), -- Sarah teaches Computer Vision
(3, 106), -- Alan teaches Algorithms
(3, 103); -- Alan teaches NLP

-- F. ENROLLMENTS (Populate Charts)

INSERT INTO enrolls_in (enrollment_id, course_id, user_id, enrollment_date, grade, completion_status, percent_completed) VALUES 
-- Original Student (ID 3)
(1, 101, 3, '2026-02-01', 'A', 'ongoing', 85),
(2, 102, 3, '2026-02-05', 'B+', 'ongoing', 45),
(3, 103, 3, '2026-02-08', 'A+', 'completed', 100),

-- Alice (ID 7) - Loves AI
(4, 101, 7, '2026-02-10', NULL, 'ongoing', 10),
(5, 104, 7, '2026-02-11', NULL, 'ongoing', 5),

-- Bob (ID 8) - Loves Coding
(6, 106, 8, '2026-02-12', NULL, 'ongoing', 20),
(7, 102, 8, '2026-02-12', NULL, 'ongoing', 15),

-- Charlie (ID 9) - The Overachiever
(8, 104, 9, '2026-02-13', NULL, 'ongoing', 0),
(9, 105, 9, '2026-02-13', NULL, 'ongoing', 0),
(10, 106, 9, '2026-02-14', NULL, 'ongoing', 0);