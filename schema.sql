-- 1. DROP OLD TABLES (Clean Slate)
-- The 'CASCADE' keyword is important because it removes foreign key links automatically
-- DROP TABLE IF EXISTS admin_actions CASCADE;
-- DROP TABLE IF EXISTS attempt CASCADE;
-- DROP TABLE IF EXISTS teaches CASCADE;
-- DROP TABLE IF EXISTS has_module CASCADE;
-- DROP TABLE IF EXISTS review CASCADE;
-- DROP TABLE IF EXISTS quiz CASCADE;
-- DROP TABLE IF EXISTS lectures CASCADE;
-- DROP TABLE IF EXISTS module CASCADE;
-- DROP TABLE IF EXISTS course_material CASCADE;
-- DROP TABLE IF EXISTS certificates CASCADE;
-- DROP TABLE IF EXISTS payment CASCADE;
-- DROP TABLE IF EXISTS lesson_progress CASCADE;
-- DROP TABLE IF EXISTS enrolls_in CASCADE;
-- DROP TABLE IF EXISTS courses CASCADE;
-- DROP TABLE IF EXISTS partner_university CASCADE;
-- DROP TABLE IF EXISTS data_analyst CASCADE;
-- DROP TABLE IF EXISTS student CASCADE;
-- DROP TABLE IF EXISTS instructor CASCADE;
-- DROP TABLE IF EXISTS administrator CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

-- 2. CREATE PARENT TABLES
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

-- 3. CREATE CHILD TABLES
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

CREATE TABLE lesson_progress (
    progress_id INTEGER PRIMARY KEY,
    course_id INTEGER,
    enrollment_id INTEGER,
    time_spent INTERVAL,
    last_accessed TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (enrollment_id) REFERENCES enrolls_in(enrollment_id)
);

CREATE TABLE payment (
    transaction_id VARCHAR(20) PRIMARY KEY,
    invoice_no VARCHAR(20),
    user_id INTEGER,
    amount INTEGER,
    payment_mode VARCHAR(20),
    currency VARCHAR(20),
    date_pay DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE certificates (
    certificate_id INTEGER PRIMARY KEY,
    issue_date DATE,
    user_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
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
    total_score NUMERIC(2,1),
    duration INTERVAL,
    completion_status VARCHAR(20)
);

CREATE TABLE review (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    rating INTEGER,
    comments VARCHAR(100),
    course_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE has_module (
    module_id INTEGER,
    lecture_id INTEGER,
    PRIMARY KEY (module_id, lecture_id),
    FOREIGN KEY (module_id) REFERENCES module(module_id),
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id)
);

CREATE TABLE teaches (
    instructor_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (instructor_id, course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE attempt (
    student_id INTEGER,
    quiz_id INTEGER,
    PRIMARY KEY (student_id, quiz_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
);

CREATE TABLE admin_actions (
    action_id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    admin_id INTEGER,
    student_id INTEGER,
    action_type VARCHAR(10),
    action_time TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES administrator(admin_id)
);

-- =============================================
-- MOCK DATA GENERATION
-- Password for all users is: password
-- =============================================

-- 1. Create a Partner University (Required for Courses)
INSERT INTO partner_university (university_id, university_name, accredation_details)
VALUES (1, 'OpenTech University', 'A+ Grade Accreditation');

-- 2. Create Users (Parent Table)
-- We use a pre-generated hash for the password "password"
-- Hash: pbkdf2:sha256:600000$Y6... (This is a standard Werkzeug hash)

INSERT INTO users (user_id, name, email, password, nationality, age) VALUES 
(1, 'Admin User', 'admin@demo.com', 'pbkdf2:sha256:600000$2432d242$21232f297a57a5a743894a0e4a801fc3', 'USA', 35),
(2, 'Instructor User', 'instructor@demo.com', 'pbkdf2:sha256:600000$2432d242$21232f297a57a5a743894a0e4a801fc3', 'UK', 40),
(3, 'Student User', 'student@demo.com', 'pbkdf2:sha256:600000$2432d242$21232f297a57a5a743894a0e4a801fc3', 'India', 21),
(4, 'Analyst User', 'analyst@demo.com', 'pbkdf2:sha256:600000$2432d242$21232f297a57a5a743894a0e4a801fc3', 'Canada', 29);

-- 3. Assign Roles (Child Tables)

-- Admin (Links to User ID 1)
INSERT INTO administrator (admin_id, user_id, salary) 
VALUES (1, 1, 80000.00);

-- Instructor (Links to User ID 2)
INSERT INTO instructor (instructor_id, user_id, salary, experience, avg_rating) 
VALUES (1, 2, 60000.00, 10, 4.5);

-- Student (Links to User ID 3)
INSERT INTO student (student_id, user_id) 
VALUES (1, 3);

-- Analyst (Links to User ID 4)
INSERT INTO data_analyst (analyst_id, salary, experience, user_id) 
VALUES (1, 55000.00, 5, 4);

-- 1. Ensure a Partner University exists (Foreign Key requirement)
INSERT INTO partner_university (university_id, university_name, accredation_details)
VALUES (1, 'IIT Kharagpur', 'A++ National Ranking')
ON CONFLICT (university_id) DO NOTHING;

-- 2. Add sample courses
INSERT INTO courses (course_id, course_name, creation_date, category, price, level, language, university_id) VALUES 
(101, 'Generative AI Masterclass', '2026-01-10', 'AI', 0, 'Intermediate', 'English', 1),
(102, 'Advanced Database Management', '2026-01-15', 'DBMS', 0, 'Advanced', 'English', 1),
(103, 'Natural Language Processing', '2026-02-01', 'AI', 0, 'Advanced', 'English', 1);

-- 3. Enroll the "Student User" (User ID 3) into these courses
-- student_id is 1 (linked to user_id 3 in your schema)
INSERT INTO enrolls_in (enrollment_id, course_id, user_id, enrollment_date, grade, completion_status, percent_completed) VALUES 
(1, 101, 3, '2026-02-01', 'A', 'ongoing', 85),
(2, 102, 3, '2026-02-05', 'B+', 'ongoing', 45),
(3, 103, 3, '2026-02-08', 'A+', 'completed', 100);
-- -- 4. Create a Sample Course (Required so Instructor/Student dashboards aren't empty)
-- INSERT INTO courses (course_id, course_name, creation_date, category, price, level, language, university_id)
-- VALUES (1, 'Intro to Database Systems', '2023-01-15', 'Computer Science', 0, 'Beginner', 'English', 1);

-- -- 5. Link Instructor to Course (Teaches)
-- INSERT INTO teaches (instructor_id, course_id)
-- VALUES (1, 1);

-- -- 6. Link Student to Course (Enrolls_in)
-- INSERT INTO enrolls_in (enrollment_id, course_id, user_id, enrollment_date, grade, completion_status, percent_completed)
-- VALUES (1, 1, 3, '2023-02-01', 'A', 'ongoing', 45);