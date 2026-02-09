# LJCourses Platform

LJCourses is a comprehensive online learning platform connecting students with expert instructors. It provides a seamless experience for course discovery, enrollment, and progress tracking.

## Features

-   **User Authentication**: Secure login and signup for students and instructors.
-   **Course Management**: Robust system for creating and managing courses, including lessons and video content.
-   **Student Dashboard**: Personalized dashboard for tracking enrolled courses and progress.
-   **Interactive Learning**: Video players, lesson tracking, and progress indicators.
-   **Search Functionality**: Real-time course search with suggestions.
-   **Responsive Design**: Mobile-friendly interface with support for dark mode.

## Project Structure

```
LJCourses/
├── app/
│   ├── routes/          # Route handlers (auth, course, student)
│   ├── services/        # Business logic and database operations
│   ├── models.py        # Database models
│   ├── db.py            # Database connection and session management
│   ├── utils.py         # Utility functions
│   ├── config.py        # Application configuration
│   └── __init__.py      # App factory
├── static/
│   ├── css/             # Custom stylesheets
│   └── js/              # Client-side JavaScript
├── templates/           # HTML templates (Jinja2)
├── run.py               # Entry point
├── seed_database.py     # Database population script
└── requirements.txt     # Python dependencies
```

## Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd LJCourses
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database**:
    ```bash
    # Create tables and seed data
    python seed_database.py
    ```

5.  **Run the application**:
    ```bash
    python run.py
    ```
    Access the app at `http://127.0.0.1:5000`.

6.  **Login Credentials**:
    *   **Student**: `24002170410016@mail.ljku.edu.in` / `Student@2024`
    *   **Instructor**: `instructor@mail.ljku.edu.in` / `Instructor@2024`
    *   **Admin**: `admin@ljcourses.com` / `Admin@2024`

## Technologies Used

-   **Backend**: Flask (Python), SQLAlchemy (ORM)
-   **Frontend**: HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla)
-   **Database**: PostgreSQL
-   **Deployment**: Ready for cloud deployment

## License

This project is licensed under the MIT License.
