# OpenLearn - Course Management Platform (Windows Setup)

A Flask-based Course Management System built for Lab Assignment IV.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your Windows machine:

1.  **Python 3.8+**: [Download Here](https://www.python.org/downloads/windows/) (Make sure to check "Add Python to PATH" during installation).
2.  **PostgreSQL**: [Download Here](https://www.postgresql.org/download/windows/).
3.  **Git** (Optional): If cloning the repo.

---

## 🚀 Installation & Setup Guide

### Step 1: Set up the Database (PostgreSQL)

1.  Open **pgAdmin 4** (installed with PostgreSQL) or search for **SQL Shell (psql)** in the Windows Start menu.
2.  If using **SQL Shell**:
    * Press `Enter` for Server, Database, Port, and Username to accept defaults.
    * Enter the password you set during installation.
3.  Run the following SQL commands to create the database and a dedicated user:

    ```sql
    CREATE DATABASE opencourse;
    CREATE USER myuser WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE opencourse TO myuser;
    \q
    ```
    *(Note: You can replace `myuser` and `mypassword` with whatever you prefer).*

### Step 2: Configure the Project

1.  Open the folder `dbms_project1` in VS Code or File Explorer.
2.  Open `app.py` and find **Line 18**.
3.  Update the connection string with your database credentials from Step 1:

    ```python
    # CHANGE THIS LINE:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/opencourse'
    ```

### Step 3: Virtual Environment Setup

Open **Command Prompt (cmd)** or **PowerShell** in the project folder and run:

1.  **Create the virtual environment:**
    ```powershell
    python -m venv venv
    ```

2.  **Activate the environment:**
    * **Command Prompt:**
        ```cmd
        venv\Scripts\activate
        ```
    * **PowerShell:**
        ```powershell
        .\venv\Scripts\activate
        ```
    *(You should see `(venv)` appear at the start of your command line).*

3.  **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

### Step 4: Initialize the Database

Run the initialization script. This will create all the tables and insert sample data (Students, Instructors, Courses).

```powershell
python init_db.py