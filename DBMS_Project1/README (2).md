# OpenLearn - Online Course Management Platform

A comprehensive web-based course management system built for **Lab Assignment IV - Database Management Systems**

## 🎯 Overview

OpenLearn is a full-featured MOOC (Massive Open Online Course) platform with four distinct user roles:
- **Students** - Browse, enroll, and learn from courses
- **Instructors** - Create and manage courses with multimedia content
- **Administrators** - Manage users and oversee platform operations
- **Data Analysts** - View comprehensive analytics and generate reports

## 🛠 Technology Stack

As per the assignment requirements (QueryCraft_Assignment_4.pdf):

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (NO frameworks)
- **Backend**: Python Flask (Connectivity Server)
- **Database**: PostgreSQL (with SQLAlchemy ORM)

## ✨ Key Features

### For Students
- Browse course catalog with real-time search and filtering
- Enroll in published courses
- Track learning progress with visual progress bars
- View course content (videos and text modules)
- Sequential module navigation

### For Instructors
- Create and edit courses
- Add multimedia modules (video links, text content)
- Manage course status (draft, published, archived)
- View enrollment statistics
- Track student engagement

### For Administrators
- User management (view, delete, change roles)
- Course oversight and moderation
- Platform statistics dashboard
- Role-based access control

### For Data Analysts
- Interactive analytics dashboard with Chart.js
- Enrollment trends visualization
- Category distribution analysis
- User role statistics
- KPI tracking

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL 12+** installed and running
3. **Git** (for cloning the repository)

## 🚀 Installation & Setup

### Step 1: Database Setup

1. Install PostgreSQL if not already installed:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # macOS (using Homebrew)
   brew install postgresql
   brew services start postgresql
   ```

2. Create a new PostgreSQL database and user:
   ```bash
   # Login to PostgreSQL
   sudo -u postgres psql
   
   # Create database and user
   CREATE DATABASE opencourse;
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE opencourse TO your_username;
   
   # Exit
   \q
   ```

### Step 2: Project Setup

1. Navigate to the project directory:
   ```bash
   cd opencourse
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Update database credentials in `app.py`:
   ```python
   # Line 18 in app.py
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/opencourse'
   ```

### Step 3: Initialize Database

Run the initialization script to create tables and populate with sample data:

```bash
python init_db.py
```

This will:
- Drop existing tables (if any)
- Create all required tables
- Populate with demo users and courses
- Create sample enrollments and modules

### Step 4: Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## 👥 Demo Accounts

After running `init_db.py`, you can login with these credentials:

| Role | Email | Password |
|------|-------|----------|
| Student | student@demo.com | password |
| Instructor | instructor@demo.com | password |
| Administrator | admin@demo.com | password |
| Data Analyst | analyst@demo.com | password |

## 📊 Database Schema

### Tables

1. **users** - Stores all user accounts
   - id, username, email, password_hash, role, created_at, last_login

2. **courses** - Course information
   - id, title, description, instructor_id, category, status, thumbnail_url, created_at

3. **course_modules** - Course content (videos, text)
   - id, course_id, title, content_type, content_body, sequence

4. **enrollments** - Student course enrollments
   - id, student_id, course_id, enrolled_at, progress, grade

### Relationships
- One Instructor → Many Courses
- One Course → Many Modules
- Many Students ↔ Many Courses (through Enrollments)

## 🎨 Design Features

Following the "Simple and Elegant" design philosophy from the architectural specification:

- **Color Palette**: Teal (#008080) and Slate (#2D3E50)
- **Typography**: Playfair Display (headings) + Source Sans Pro (body)
- **Layout**: Card-based UI with CSS Grid and Flexbox
- **Animations**: Smooth transitions and progress animations
- **Responsive**: Mobile-friendly design with breakpoints

## 🔒 Security Features

- Password hashing using Werkzeug's security module
- Session-based authentication
- Role-based access control decorators
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection ready (Flask-WTF can be added)
- Delete confirmation modals

## 📁 Project Structure

```
opencourse/
├── app.py                 # Main Flask application
├── models.py             # SQLAlchemy database models
├── init_db.py            # Database initialization script
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── script.js    # JavaScript functionality
└── templates/
    ├── base.html                      # Base template
    ├── index.html                     # Landing page
    ├── login.html                     # Login page
    ├── register.html                  # Registration page
    ├── student_dashboard.html         # Student dashboard
    ├── student_catalog.html           # Course catalog
    ├── student_course_view.html       # Course viewing
    ├── instructor_dashboard.html      # Instructor dashboard
    ├── instructor_create_course.html  # Course creation
    ├── instructor_edit_course.html    # Course editing
    ├── admin_panel.html              # Admin panel
    └── analyst_dashboard.html        # Analytics dashboard
```

## 🔧 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Student Routes
- `GET /student/dashboard` - View enrolled courses
- `GET /student/catalog` - Browse available courses
- `POST /student/enroll/<course_id>` - Enroll in course
- `GET /student/course/<course_id>` - View course content

### Instructor Routes
- `GET /instructor/dashboard` - View created courses
- `GET/POST /instructor/course/create` - Create new course
- `GET/POST /instructor/course/<course_id>/edit` - Edit course
- `POST /instructor/course/<course_id>/module/add` - Add module

### Admin Routes
- `GET /admin/panel` - Admin control panel
- `POST /admin/user/<user_id>/delete` - Delete user
- `POST /admin/user/<user_id>/role` - Change user role

### Analyst Routes
- `GET /analyst/dashboard` - Analytics dashboard
- `GET /api/stats` - Get statistics data (JSON)

### API Routes
- `GET /api/courses/search?q=<query>&category=<category>` - Search courses

## 🎯 Functional Requirements (from Lab Assignment)

✅ **Entry Page**: Role-based menu display after login  
✅ **Student Features**: View, search, and register for courses  
✅ **Instructor Features**: Add content to courses  
✅ **Admin Features**: Add teachers, manage students  
✅ **Analyst Features**: View course statistics and analytics  

## 🚨 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running: `sudo service postgresql status`
- Check credentials in `app.py`
- Ensure database exists: `psql -l`

### Module Import Error
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change port in `app.py`: `app.run(debug=True, port=5001)`
- Or kill existing process: `lsof -ti:5000 | xargs kill -9`

## 📝 Additional Notes

### For Assignment Submission

This project fulfills all requirements of **Lab Assignment IV**:

1. **ER Diagram**: See submitted QueryCraft_Assignment_4.pdf
2. **Table Schema**: Implemented in `models.py`
3. **Functionalities**: All four user roles implemented
4. **Frontend Tools**: HTML5, CSS3, Vanilla JavaScript
5. **Backend**: Python Flask
6. **Database**: PostgreSQL with SQLAlchemy

### Future Enhancements
- PDF report generation for analysts
- Email notifications
- Assignment/quiz system
- Discussion forums
- Certificate generation
- Advanced search filters

## 👨‍💻 Development Team

**Group Members** (as per QueryCraft_Assignment_4.pdf):
- Srujan Shyam Perumalla (23CS10053)
- Thummala Thilok (23CS10073)
- Rajaboina Naveen (23CS10058)
- Banothu Venu (23CS30012)
- Nikitha Lenka (23CS10038)

## 📄 License

This project is created for educational purposes as part of the Database Management Systems lab course.

---

**Built with ❤️ for Lab Assignment IV - DBMS**
