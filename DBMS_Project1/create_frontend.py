# import os

# # Define the folder structure
# folders = ['templates', 'static', 'static/css', 'static/js']

# # CSS Content (Teal & Slate Theme)
# css_content = """
# :root {
#     --primary: #008080; /* Teal */
#     --secondary: #2D3E50; /* Slate */
#     --accent: #20B2AA;
#     --light: #F4F7F6;
#     --dark: #1A252F;
#     --success: #27ae60;
#     --warning: #f39c12;
#     --danger: #c0392b;
#     --white: #ffffff;
#     --shadow: 0 4px 6px rgba(0,0,0,0.1);
#     --font-main: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# }

# * { box-sizing: border-box; margin: 0; padding: 0; }
# body { font-family: var(--font-main); background-color: var(--light); color: var(--dark); line-height: 1.6; }

# /* Navigation */
# .navbar { background-color: var(--secondary); color: var(--white); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
# .navbar-brand { font-size: 1.5rem; font-weight: bold; color: var(--white); text-decoration: none; }
# .nav-links a { color: var(--white); text-decoration: none; margin-left: 1.5rem; transition: color 0.3s; }
# .nav-links a:hover { color: var(--accent); }

# /* Containers */
# .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
# .card { background: var(--white); border-radius: 8px; box-shadow: var(--shadow); padding: 1.5rem; margin-bottom: 1.5rem; transition: transform 0.2s; }
# .card:hover { transform: translateY(-2px); }

# /* Grid Layouts */
# .grid-3 { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
# .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }

# /* Forms & Buttons */
# .form-group { margin-bottom: 1rem; }
# .form-group label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
# .form-control { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }
# .btn { display: inline-block; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; text-decoration: none; text-align: center; transition: background 0.3s; }
# .btn-primary { background-color: var(--primary); color: var(--white); }
# .btn-primary:hover { background-color: #006666; }
# .btn-danger { background-color: var(--danger); color: var(--white); }
# .btn-sm { padding: 0.4rem 0.8rem; font-size: 0.9rem; }
# .btn-block { display: block; width: 100%; }

# /* Dashboard Specifics */
# .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
# .stat-card { background: var(--secondary); color: var(--white); text-align: center; padding: 2rem; border-radius: 8px; }
# .stat-number { font-size: 2.5rem; font-weight: bold; display: block; }
# .progress-bar-bg { background: #eee; height: 10px; border-radius: 5px; overflow: hidden; margin-top: 10px; }
# .progress-bar-fill { background: var(--primary); height: 100%; }

# /* Utilities */
# .text-center { text-align: center; }
# .mt-2 { margin-top: 2rem; }
# .alert { padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
# .alert-success { background: #d4edda; color: #155724; }
# .alert-danger { background: #f8d7da; color: #721c24; }
# .badge { padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.8rem; }
# .badge-published { background: var(--success); color: white; }
# .badge-draft { background: var(--warning); color: black; }

# /* Responsive */
# @media (max-width: 768px) {
#     .grid-2, .grid-3, .stats-grid { grid-template-columns: 1fr; }
#     .navbar { flex-direction: column; }
#     .nav-links { margin-top: 1rem; }
# }
# """

# # HTML Templates Data
# templates = {
#     'base.html': """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>OpenLearn | Course Management</title>
#     <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> </head>
# <body>
#     <nav class="navbar">
#         <a href="{{ url_for('index') }}" class="navbar-brand">OpenLearn</a>
#         <div class="nav-links">
#             {% if session.user_id %}
#                 {% if session.role == 'student' %}
#                     <a href="{{ url_for('student_dashboard') }}">My Dashboard</a>
#                     <a href="{{ url_for('student_catalog') }}">Catalog</a>
#                 {% elif session.role == 'instructor' %}
#                     <a href="{{ url_for('instructor_dashboard') }}">Instructor Studio</a>
#                 {% elif session.role == 'admin' %}
#                     <a href="{{ url_for('admin_panel') }}">Admin Panel</a>
#                 {% elif session.role == 'analyst' %}
#                     <a href="{{ url_for('analyst_dashboard') }}">Analytics</a>
#                 {% endif %}
#                 <span style="margin-left: 20px; font-size: 0.9rem; opacity: 0.8;">{{ session.username }} ({{ session.role }})</span>
#                 <a href="{{ url_for('logout') }}" style="border: 1px solid white; padding: 5px 10px; border-radius: 4px;">Logout</a>
#             {% else %}
#                 <a href="{{ url_for('login') }}">Login</a>
#                 <a href="{{ url_for('register') }}">Register</a>
#             {% endif %}
#         </div>
#     </nav>

#     <div class="container">
#         {% with messages = get_flashed_messages(with_categories=true) %}
#             {% if messages %}
#                 {% for category, message in messages %}
#                     <div class="alert alert-{{ category }}">{{ message }}</div>
#                 {% endfor %}
#             {% endif %}
#         {% endwith %}

#         {% block content %}{% endblock %}
#     </div>
# </body>
# </html>""",

#     'index.html': """{% extends "base.html" %}
# {% block content %}
# <div class="text-center mt-2">
#     <h1 style="font-size: 3rem; color: var(--secondary);">Master New Skills</h1>
#     <p style="font-size: 1.2rem; margin: 1rem 0 2rem;">Join our global learning community. Access top-tier courses created by industry experts.</p>
    
#     {% if not session.user_id %}
#     <div style="margin-top: 2rem;">
#         <a href="{{ url_for('register') }}" class="btn btn-primary" style="padding: 1rem 2rem; font-size: 1.2rem;">Get Started For Free</a>
#         <a href="{{ url_for('login') }}" class="btn" style="background: #ddd; margin-left: 1rem;">Log In</a>
#     </div>
#     {% else %}
#         <a href="{{ url_for('student_catalog') }}" class="btn btn-primary">Browse Courses</a>
#     {% endif %}
# </div>

# <div class="grid-3 mt-2">
#     <div class="card text-center">
#         <h3>For Students</h3>
#         <p>Learn at your own pace with lifetime access to courses.</p>
#     </div>
#     <div class="card text-center">
#         <h3>For Instructors</h3>
#         <p>Create and publish courses to reach millions of students.</p>
#     </div>
#     <div class="card text-center">
#         <h3>Data Driven</h3>
#         <p>Powered by robust analytics to improve learning outcomes.</p>
#     </div>
# </div>
# {% endblock %}""",

#     'login.html': """{% extends "base.html" %}
# {% block content %}
# <div style="max-width: 400px; margin: 4rem auto;">
#     <div class="card">
#         <h2 class="text-center">Welcome Back</h2>
#         <form method="POST" action="{{ url_for('login') }}">
#             <div class="form-group">
#                 <label>Email Address</label>
#                 <input type="email" name="email" class="form-control" required>
#             </div>
#             <div class="form-group">
#                 <label>Password</label>
#                 <input type="password" name="password" class="form-control" required>
#             </div>
#             <button type="submit" class="btn btn-primary btn-block">Login</button>
#         </form>
#         <p class="text-center" style="margin-top: 1rem;">
#             Don't have an account? <a href="{{ url_for('register') }}">Register</a>
#         </p>
#     </div>
# </div>
# {% endblock %}""",

#     'register.html': """{% extends "base.html" %}
# {% block content %}
# <div style="max-width: 400px; margin: 4rem auto;">
#     <div class="card">
#         <h2 class="text-center">Create Account</h2>
#         <form method="POST" action="{{ url_for('register') }}">
#             <div class="form-group">
#                 <label>Username</label>
#                 <input type="text" name="username" class="form-control" required>
#             </div>
#             <div class="form-group">
#                 <label>Email Address</label>
#                 <input type="email" name="email" class="form-control" required>
#             </div>
#             <div class="form-group">
#                 <label>Password</label>
#                 <input type="password" name="password" class="form-control" required>
#             </div>
#             <button type="submit" class="btn btn-primary btn-block">Register</button>
#         </form>
#     </div>
# </div>
# {% endblock %}""",

#     'student_dashboard.html': """{% extends "base.html" %}
# {% block content %}
# <h2>My Learning Dashboard</h2>
# {% if enrollments %}
#     <div class="grid-3">
#         {% for enrollment in enrollments %}
#         <div class="card">
#             <h3>{{ enrollment.course.title }}</h3>
#             <p style="color: #666; font-size: 0.9rem;">Instructor: {{ enrollment.course.instructor.username }}</p>
#             <div class="progress-bar-bg">
#                 <div class="progress-bar-fill" style="width: {{ enrollment.progress }}%"></div>
#             </div>
#             <p style="text-align: right; font-size: 0.8rem; margin-top: 5px;">{{ enrollment.progress }}% Complete</p>
#             <a href="{{ url_for('view_course', course_id=enrollment.course.id) }}" class="btn btn-primary btn-block" style="margin-top: 1rem;">Continue Learning</a>
#         </div>
#         {% endfor %}
#     </div>
# {% else %}
#     <div class="text-center mt-2">
#         <p>You haven't enrolled in any courses yet.</p>
#         <a href="{{ url_for('student_catalog') }}" class="btn btn-primary">Browse Catalog</a>
#     </div>
# {% endif %}
# {% endblock %}""",

#     'student_catalog.html': """{% extends "base.html" %}
# {% block content %}
# <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
#     <h2>Course Catalog</h2>
#     <input type="text" id="searchInput" placeholder="Search courses..." class="form-control" style="width: 300px;">
# </div>

# <div class="grid-3" id="courseGrid">
#     {% for course in courses %}
#     <div class="card course-card" data-title="{{ course.title.lower() }}" data-category="{{ course.category.lower() }}">
#         <div style="background: #eee; height: 150px; margin: -1.5rem -1.5rem 1rem -1.5rem; display: flex; align-items: center; justify-content: center; color: #999;">
#             Thumbnail
#         </div>
#         <h3>{{ course.title }}</h3>
#         <span class="badge" style="background: #e0e0e0; color: #333;">{{ course.category }}</span>
#         <p style="margin-top: 1rem; color: #555;">{{ course.description[:100] }}...</p>
#         <form action="{{ url_for('enroll_course', course_id=course.id) }}" method="POST">
#             <button type="submit" class="btn btn-primary btn-block" style="margin-top: 1rem;">Enroll Now</button>
#         </form>
#     </div>
#     {% endfor %}
# </div>

# <script>
#     // AJAX-like search implementation (Client-side filtering for simplicity)
#     document.getElementById('searchInput').addEventListener('keyup', function(e) {
#         const term = e.target.value.toLowerCase();
#         const cards = document.querySelectorAll('.course-card');
        
#         cards.forEach(card => {
#             const title = card.getAttribute('data-title');
#             const category = card.getAttribute('data-category');
#             if (title.includes(term) || category.includes(term)) {
#                 card.style.display = 'block';
#             } else {
#                 card.style.display = 'none';
#             }
#         });
#     });
# </script>
# {% endblock %}""",

#     'student_course_view.html': """{% extends "base.html" %}
# {% block content %}
# <div class="grid-2" style="grid-template-columns: 300px 1fr;">
#     <div class="card">
#         <h3>{{ course.title }}</h3>
#         <hr style="margin: 1rem 0; border: 0; border-top: 1px solid #eee;">
#         <div style="display: flex; flex-direction: column; gap: 0.5rem;">
#             {% for module in modules %}
#             <div style="padding: 10px; background: #f8f9fa; border-radius: 4px; cursor: pointer;">
#                 <strong>Mod {{ module.sequence }}:</strong> {{ module.title }}
#                 <span style="font-size: 0.8rem; color: #666; float: right;">{{ module.content_type }}</span>
#             </div>
#             {% endfor %}
#         </div>
#     </div>

#     <div class="card">
#         <h2>Course Content</h2>
#         <p>Select a module from the left to view content.</p>
#         <div style="margin-top: 2rem; padding: 2rem; background: #f9f9f9; border-radius: 8px; text-align: center;">
#             <p><em>(Content viewer placeholder - Click modules on sidebar to load)</em></p>
#             {% if modules %}
#                 <div style="text-align: left; margin-top: 2rem;">
#                     <h3>{{ modules[0].title }}</h3>
#                     {% if modules[0].content_type == 'video' %}
#                         <iframe width="100%" height="400" src="{{ modules[0].content_body }}" frameborder="0" allowfullscreen></iframe>
#                     {% else %}
#                         <div>{{ modules[0].content_body|safe }}</div>
#                     {% endif %}
#                 </div>
#             {% endif %}
#         </div>
#     </div>
# </div>
# {% endblock %}""",

#     'instructor_dashboard.html': """{% extends "base.html" %}
# {% block content %}
# <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
#     <h2>Instructor Studio</h2>
#     <a href="{{ url_for('create_course') }}" class="btn btn-primary">+ Create New Course</a>
# </div>

# <div class="card">
#     <table style="width: 100%; border-collapse: collapse;">
#         <thead>
#             <tr style="text-align: left; border-bottom: 2px solid #eee;">
#                 <th style="padding: 1rem;">Course Title</th>
#                 <th>Category</th>
#                 <th>Enrollments</th>
#                 <th>Status</th>
#                 <th>Actions</th>
#             </tr>
#         </thead>
#         <tbody>
#             {% for course in courses %}
#             <tr style="border-bottom: 1px solid #eee;">
#                 <td style="padding: 1rem;">{{ course.title }}</td>
#                 <td>{{ course.category }}</td>
#                 <td>{{ course.enrollment_count }}</td>
#                 <td>
#                     <span class="badge badge-{{ course.status }}">{{ course.status }}</span>
#                 </td>
#                 <td>
#                     <a href="{{ url_for('edit_course', course_id=course.id) }}" class="btn btn-sm" style="background: #e0e0e0;">Edit</a>
#                 </td>
#             </tr>
#             {% else %}
#             <tr><td colspan="5" class="text-center" style="padding: 2rem;">No courses created yet.</td></tr>
#             {% endfor %}
#         </tbody>
#     </table>
# </div>
# {% endblock %}""",

#     'instructor_create_course.html': """{% extends "base.html" %}
# {% block content %}
# <div style="max-width: 800px; margin: 0 auto;">
#     <h2>Create New Course</h2>
#     <div class="card">
#         <form method="POST">
#             <div class="form-group">
#                 <label>Course Title</label>
#                 <input type="text" name="title" class="form-control" required>
#             </div>
#             <div class="form-group">
#                 <label>Category</label>
#                 <select name="category" class="form-control">
#                     <option>Computer Science</option>
#                     <option>Data Science</option>
#                     <option>Business</option>
#                     <option>Arts</option>
#                 </select>
#             </div>
#             <div class="form-group">
#                 <label>Description</label>
#                 <textarea name="description" class="form-control" rows="5" required></textarea>
#             </div>
#             <div style="display: flex; gap: 1rem; margin-top: 1rem;">
#                 <button type="submit" class="btn btn-primary">Create Draft</button>
#                 <a href="{{ url_for('instructor_dashboard') }}" class="btn" style="background: #ddd;">Cancel</a>
#             </div>
#         </form>
#     </div>
# </div>
# {% endblock %}""",

#     'instructor_edit_course.html': """{% extends "base.html" %}
# {% block content %}
# <div class="grid-2">
#     <div>
#         <h3>Edit Course Details</h3>
#         <div class="card">
#             <form method="POST">
#                 <div class="form-group">
#                     <label>Title</label>
#                     <input type="text" name="title" value="{{ course.title }}" class="form-control">
#                 </div>
#                 <div class="form-group">
#                     <label>Status</label>
#                     <select name="status" class="form-control">
#                         <option value="draft" {% if course.status == 'draft' %}selected{% endif %}>Draft</option>
#                         <option value="published" {% if course.status == 'published' %}selected{% endif %}>Published</option>
#                     </select>
#                 </div>
#                 <button type="submit" class="btn btn-primary btn-block">Save Changes</button>
#             </form>
#         </div>
#     </div>

#     <div>
#         <h3>Course Modules</h3>
#         <div class="card">
#             {% for module in modules %}
#             <div style="padding: 0.5rem; border-bottom: 1px solid #eee;">
#                 <strong>{{ module.sequence }}.</strong> {{ module.title }}
#                 <span class="badge" style="float: right;">{{ module.content_type }}</span>
#             </div>
#             {% endfor %}
            
#             <hr style="margin: 1rem 0;">
#             <h4>Add New Module</h4>
#             <form action="{{ url_for('add_module', course_id=course.id) }}" method="POST">
#                 <div class="form-group">
#                     <input type="text" name="title" placeholder="Module Title" class="form-control" required>
#                 </div>
#                 <div class="form-group">
#                     <select name="content_type" class="form-control">
#                         <option value="text">Text / HTML</option>
#                         <option value="video">Video Embed URL</option>
#                     </select>
#                 </div>
#                 <div class="form-group">
#                     <textarea name="content_body" placeholder="Content (HTML or URL)" class="form-control" rows="3" required></textarea>
#                 </div>
#                 <button type="submit" class="btn btn-primary btn-sm">Add Module</button>
#             </form>
#         </div>
#     </div>
# </div>
# {% endblock %}""",

#     'admin_panel.html': """{% extends "base.html" %}
# {% block content %}
# <h2>System Administration</h2>
# <div class="card mt-2">
#     <h3>User Management</h3>
#     <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
#         <thead>
#             <tr style="text-align: left; background: #f8f9fa;">
#                 <th style="padding: 10px;">Username</th>
#                 <th>Email</th>
#                 <th>Current Role</th>
#                 <th>Actions</th>
#             </tr>
#         </thead>
#         <tbody>
#             {% for user in users %}
#             <tr style="border-bottom: 1px solid #eee;">
#                 <td style="padding: 10px;">{{ user.username }}</td>
#                 <td>{{ user.email }}</td>
#                 <td><span class="badge" style="background: #333; color: white;">{{ user.role }}</span></td>
#                 <td style="display: flex; gap: 0.5rem; padding: 10px;">
#                     <form action="{{ url_for('change_role', user_id=user.id) }}" method="POST" style="display: flex;">
#                         <select name="role" style="padding: 5px;">
#                             <option value="student">Student</option>
#                             <option value="instructor">Instructor</option>
#                             <option value="analyst">Analyst</option>
#                             <option value="admin">Admin</option>
#                         </select>
#                         <button type="submit" class="btn btn-sm btn-primary">Update</button>
#                     </form>
#                     {% if user.id != session.user_id %}
#                     <form action="{{ url_for('delete_user', user_id=user.id) }}" method="POST" onsubmit="return confirm('Delete this user?');">
#                         <button type="submit" class="btn btn-sm btn-danger">Delete</button>
#                     </form>
#                     {% endif %}
#                 </td>
#             </tr>
#             {% endfor %}
#         </tbody>
#     </table>
# </div>
# {% endblock %}""",

#     'analyst_dashboard.html': """{% extends "base.html" %}
# {% block content %}
# <h2>Analytics Dashboard</h2>

# <div class="stats-grid" id="kpiContainer">
#     <div class="stat-card">
#         <span class="stat-number" id="totalUsers">-</span>
#         Total Users
#     </div>
#     <div class="stat-card">
#         <span class="stat-number" id="totalCourses">-</span>
#         Active Courses
#     </div>
#     <div class="stat-card">
#         <span class="stat-number" id="totalEnrollments">-</span>
#         Total Enrollments
#     </div>
# </div>

# <div class="grid-2">
#     <div class="card">
#         <h3>Enrollments by Category</h3>
#         <canvas id="categoryChart"></canvas>
#     </div>
#     <div class="card">
#         <h3>User Role Distribution</h3>
#         <canvas id="roleChart"></canvas>
#     </div>
# </div>

# <script>
#     // Fetch data from Flask API
#     fetch('/api/stats')
#         .then(response => response.json())
#         .then(data => {
#             // Update KPIs
#             document.getElementById('totalUsers').innerText = data.totals.users;
#             document.getElementById('totalCourses').innerText = data.totals.courses;
#             document.getElementById('totalEnrollments').innerText = data.totals.enrollments;

#             // Render Category Chart
#             new Chart(document.getElementById('categoryChart'), {
#                 type: 'doughnut',
#                 data: {
#                     labels: data.categories.map(c => c.category),
#                     datasets: [{
#                         data: data.categories.map(c => c.count),
#                         backgroundColor: ['#008080', '#20B2AA', '#48D1CC', '#2D3E50']
#                     }]
#                 }
#             });

#             // Render Role Chart
#             new Chart(document.getElementById('roleChart'), {
#                 type: 'bar',
#                 data: {
#                     labels: data.roles.map(r => r.role),
#                     datasets: [{
#                         label: 'Users',
#                         data: data.roles.map(r => r.count),
#                         backgroundColor: '#2D3E50'
#                     }]
#                 }
#             });
#         });
# </script>
# {% endblock %}"""
# }

# def create_files():
#     print("🚀 Initializing OpenLearn Frontend...")
    
#     # 1. Create Directories
#     for folder in folders:
#         if not os.path.exists(folder):
#             os.makedirs(folder)
#             print(f"   Created directory: {folder}/")

#     # 2. Write CSS File
#     with open('static/css/style.css', 'w', encoding='utf-8') as f:
#         f.write(css_content)
#     print("   Created static/css/style.css")

#     # 3. Write HTML Templates
#     for filename, content in templates.items():
#         path = os.path.join('templates', filename)
#         with open(path, 'w', encoding='utf-8') as f:
#             f.write(content)
#         print(f"   Created templates/{filename}")

#     print("\n✅ Frontend setup complete! You can now run 'python app.py'")

# if __name__ == "__main__":
#     create_files()