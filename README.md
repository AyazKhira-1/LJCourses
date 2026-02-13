<p align="center">
  <img src="https://img.shields.io/badge/Flask-3.1-blue?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.14-green?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

# 🎓 LJCourses — University Learning Platform

**LJCourses** is a modern, full-stack online learning platform built for **LJ University** students. It provides a seamless experience for course discovery, enrollment, video-based learning, and progress tracking — all wrapped in a beautiful, responsive interface with dark mode support.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | Secure student login & sign-up with email validation (`{enrollment}@mail.ljku.edu.in`) |
| 📚 **Course Browsing** | Browse, search, and filter courses by category, difficulty, and rating |
| 🎬 **Video Lessons** | Embedded YouTube video player with lesson-by-lesson navigation |
| 📊 **Progress Tracking** | Real-time progress bars, lesson completion, and course completion status |
| 🏆 **Completed Courses** | Dedicated view for finished courses with certificate access |
| 👤 **Student Dashboard** | Personalized dashboard with enrolled courses and quick stats |
| ⚙️ **Settings** | Profile photo upload, bio editing, and theme preferences |
| 🌙 **Dark Mode** | Full dark/light theme toggle with persistent preference |
| 📱 **Responsive Design** | Mobile-first UI powered by Bootstrap 5 |

---

## 🏗️ Project Structure

```
LJCourses/
├── app/                         # Application package
│   ├── __init__.py              # App factory (create_app)
│   ├── config.py                # Environment-based configuration
│   ├── db.py                    # SQLAlchemy engine & session
│   ├── models.py                # Database models (6 tables)
│   ├── utils.py                 # Auth decorators & helpers
│   ├── routes/                  # Blueprint route handlers
│   │   ├── auth.py              #   ├─ Login, Sign-up, Password Reset
│   │   ├── course.py            #   ├─ Browse, Overview, Lessons, Enrollment
│   │   └── student.py           #   └─ Dashboard, Profile, Settings, API
│   └── services/                # Business logic layer
│       ├── users.py             #   ├─ User CRUD & authentication
│       ├── courses.py           #   ├─ Course queries & filtering
│       ├── categories.py        #   ├─ Category management
│       ├── enrollments.py       #   ├─ Enrollment operations
│       ├── lessons.py           #   ├─ Lesson retrieval
│       ├── progress.py          #   ├─ Lesson progress tracking
│       └── instructors.py       #   └─ Instructor queries
│
├── templates/                   # Jinja2 HTML templates (14 pages)
│   ├── base.html                #   ├─ Base layout with navbar
│   ├── home.html                #   ├─ Landing page
│   ├── student.html             #   ├─ Student dashboard layout
│   ├── student_login.html       #   ├─ Login page
│   ├── student_sign_up.html     #   ├─ Registration page
│   ├── browse-courses.html      #   ├─ Course catalog with filters
│   ├── course-overview.html     #   ├─ Course details & enrollment
│   ├── lesson.html              #   ├─ Video player & lesson content
│   ├── my_courses.html          #   ├─ Enrolled courses
│   ├── completed_courses.html   #   ├─ Completed courses
│   ├── profile.html             #   ├─ User profile
│   ├── settings.html            #   ├─ Account settings
│   ├── change_password.html     #   └─ Password change
│   └── forgot_password.html     #   └─ Password reset
│
├── static/
│   ├── css/                     # Stylesheets (8 files)
│   ├── js/                      # Client-side JavaScript (9 files)
│   ├── images/                  # Static assets
│   └── uploads/                 # User-uploaded files
│
├── run.py                       # Application entry point
├── seed_database.py             # Database seeder with sample data
├── pyproject.toml               # Python dependencies & metadata
└── database_schema.md           # Database schema documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.14+
- **PostgreSQL** 16+
- **uv** (recommended) or pip

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd LJCourses

# 2. Create virtual environment & install dependencies
uv sync
# Or with pip:
# python -m venv .venv && .venv\Scripts\activate && pip install -e .

# 3. Configure environment variables
# Create a .env file with:
#   DATABASE_URL=postgresql://user:password@localhost:5432/ljcourses
#   SECRET_KEY=your-secret-key

# 4. Seed the database with sample data
uv run python seed_database.py

# 5. Start the development server
uv run python run.py
```

The app will be available at **http://127.0.0.1:5001**

### 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| 👨‍🎓 Student | `24002170410016@mail.ljku.edu.in` | `Student@2024` |
| 👨‍🏫 Instructor | `instructor@mail.ljku.edu.in` | `Instructor@2024` |
| 🛡️ Admin | `admin@ljcourses.com` | `Admin@2024` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.1, SQLAlchemy 2.0 |
| **Database** | PostgreSQL with UUID primary keys |
| **Frontend** | HTML5, Vanilla CSS & JS, Bootstrap 5.3 |
| **Templating** | Jinja2 |
| **Auth** | Session-based with Werkzeug password hashing |
| **Package Manager** | uv (PEP 723) |

---

## 📖 Documentation

- [Database Schema](database_schema.md) — Full schema documentation with ER diagram

---

## 📄 License

This project is licensed under the **MIT License**.
