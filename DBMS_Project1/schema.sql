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


-- A. UNIVERSITY
INSERT INTO partner_university (university_id, university_name, accredation_details)
VALUES (1, 'OpenTech University', 'A+ Grade Accreditation');

-- B. USERS (Core Roles + New Instructors + New Students)
INSERT INTO users (user_id, name, email, password, nationality, age, phonenumber) VALUES 
-- Core Roles (1-4)
(1, 'Admin User', 'admin@demo.com', 'hashed_later', 'USA', 35, '123-456-7890'),
(2, 'Instructor User', 'instructor@demo.com', 'hashed_later', 'UK', 40, '123-456-7890'),
(3, 'Student User', 'student@demo.com', 'hashed_later', 'India', 21, '123-456-7890'),
(4, 'Analyst User', 'analyst@demo.com', 'hashed_later', 'Canada', 29, '123-456-7890'),

-- 5 NEW INSTRUCTORS (IDs 10-14)
(10, 'Dr. Emily Carter', 'emily@univ.edu', 'hashed_later', 'USA', 45, '555-0101'),
(11, 'Prof. Raj Patel', 'raj@univ.edu', 'hashed_later', 'India', 52, '555-0102'),
(12, 'Dr. Wei Chen', 'wei@univ.edu', 'hashed_later', 'China', 39, '555-0103'),
(13, 'Sofia Rodriguez', 'sofia@univ.edu', 'hashed_later', 'Spain', 34, '555-0104'),
(14, 'Hans Mueller', 'hans@univ.edu', 'hashed_later', 'Germany', 48, '555-0105'),

-- 10 NEW STUDENTS (IDs 20-29)
(20, 'Liam Johnson', 'liam@student.com', 'hashed_later', 'Canada', 22, '555-0201'),
(21, 'Emma Wilson', 'emma@student.com', 'hashed_later', 'Australia', 20, '555-0202'),
(22, 'Noah Brown', 'noah@student.com', 'hashed_later', 'USA', 23, '555-0203'),
(23, 'Olivia Martinez', 'olivia@student.com', 'hashed_later', 'Mexico', 21, '555-0204'),
(24, 'William Anderson', 'will@student.com', 'hashed_later', 'UK', 25, '555-0205'),
(25, 'Ava Thomas', 'ava@student.com', 'hashed_later', 'New Zealand', 19, '555-0206'),
(26, 'James Jackson', 'james@student.com', 'hashed_later', 'USA', 24, '555-0207'),
(27, 'Isabella White', 'bella@student.com', 'hashed_later', 'Italy', 22, '555-0208'),
(28, 'Lucas Harris', 'lucas@student.com', 'hashed_later', 'Brazil', 26, '555-0209'),
(29, 'Mia Martin', 'mia@student.com', 'hashed_later', 'France', 21, '555-0210');

-- C. ROLES

-- Admin
INSERT INTO administrator (admin_id, user_id, salary) VALUES (1, 1, 80000.00);

-- Instructors (Linking Users 2, 10-14)
INSERT INTO instructor (instructor_id, user_id, salary, experience, avg_rating) VALUES 
(1, 2, 60000.00, 10, 4.5),  -- Original
(2, 10, 95000.00, 15, 4.9), -- Dr. Emily
(3, 11, 88000.00, 20, 4.7), -- Prof. Raj
(4, 12, 72000.00, 8, 4.6),  -- Dr. Wei
(5, 13, 68000.00, 5, 4.8),  -- Sofia
(6, 14, 85000.00, 18, 4.4); -- Hans

-- Analysts
INSERT INTO data_analyst (analyst_id, salary, experience, user_id) VALUES (1, 55000.00, 5, 4);

-- Students (Linking Users 3, 20-29)
INSERT INTO student (student_id, user_id) VALUES 
(1, 3), (2, 20), (3, 21), (4, 22), (5, 23),
(6, 24), (7, 25), (8, 26), (9, 27), (10, 28), (11, 29);

-- D. COURSES (Original + 5 New)

INSERT INTO courses (course_id, course_name, creation_date, category, price, level, language, university_id) VALUES 
(101, 'Generative AI Masterclass', '2026-01-10', 'AI', 0, 'Intermediate', 'English', 1),
(102, 'Advanced DBMS', '2026-01-15', 'DBMS', 0, 'Advanced', 'English', 1),
(103, 'Natural Language Processing', '2026-02-01', 'AI', 0, 'Advanced', 'English', 1),
-- 5 NEW COURSES
(201, 'Cybersecurity Fundamentals', '2026-02-10', 'Security', 0, 'Beginner', 'English', 1),
(202, 'Full Stack Web Dev (React)', '2026-02-12', 'Web Dev', 0, 'Intermediate', 'English', 1),
(203, 'Financial Analysis 101', '2026-02-15', 'Finance', 0, 'Beginner', 'English', 1),
(204, 'Cloud Computing with AWS', '2026-02-18', 'Cloud', 0, 'Advanced', 'English', 1),
(205, 'Game Development with Unity', '2026-02-20', 'Game Dev', 0, 'Intermediate', 'English', 1);

-- E. TEACHES (Linking Instructors to Courses)

INSERT INTO teaches (instructor_id, course_id) VALUES 
(1, 101), (1, 102), -- Original Instructor
(2, 201), (2, 103), -- Dr. Emily (Security & AI)
(3, 204),           -- Prof. Raj (Cloud)
(4, 202),           -- Dr. Wei (Web Dev)
(5, 205),           -- Sofia (Game Dev)
(6, 203);           -- Hans (Finance)

-- F. ENROLLMENTS (Populate Charts for Analyst)

INSERT INTO enrolls_in (enrollment_id, course_id, user_id, enrollment_date, grade, completion_status, percent_completed) VALUES 
-- Original Student (ID 3)
(1, 101, 3, '2026-02-01', 'A', 'ongoing', 85),
(2, 102, 3, '2026-02-05', 'B+', 'ongoing', 45),
(3, 103, 3, '2026-02-08', 'A+', 'completed', 100),

-- New Enrollments (Students 20-29)
(10, 201, 20, '2026-02-10', NULL, 'ongoing', 15),  -- Liam in Cybersecurity
(11, 202, 21, '2026-02-11', 'A-', 'completed', 100), -- Emma in Web Dev
(12, 204, 22, '2026-02-12', NULL, 'ongoing', 30),  -- Noah in Cloud
(13, 203, 23, '2026-02-13', 'B', 'ongoing', 60),   -- Olivia in Finance
(14, 205, 24, '2026-02-14', NULL, 'ongoing', 10),  -- William in Game Dev
(15, 101, 25, '2026-02-15', NULL, 'ongoing', 20),  -- Ava in GenAI
(16, 102, 26, '2026-02-16', 'C+', 'ongoing', 40),  -- James in DBMS
(17, 201, 27, '2026-02-17', 'A', 'completed', 100),-- Isabella in Cybersecurity
(18, 202, 28, '2026-02-18', NULL, 'ongoing', 5),   -- Lucas in Web Dev
(19, 205, 29, '2026-02-19', NULL, 'ongoing', 50);  -- Mia in Game Dev