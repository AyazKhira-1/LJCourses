from flask import Flask, render_template

app = Flask(__name__)


# Routes
@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')


@app.route('/student-login')
def student_login():
    """Student login page"""
    return render_template('student_login.html')


@app.route('/student-sign-up')
def student_sign_up():
    """Student sign up page"""
    return render_template('student_sign_up.html')


@app.route('/my-courses')
def my_courses():
    """My courses page"""
    return render_template('my_courses.html')


@app.route('/profile')
def profile():
    """Student profile page"""
    return render_template('profile.html')


@app.route('/browse-courses')
def browse_courses():
    """Browse available courses page"""
    return render_template('browse-courses.html')


@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')


@app.route('/lesson')
def lesson():
    """Individual lesson page"""
    return render_template('lesson.html')


@app.route('/course')
def course_overview():
    """Course overview page"""
    return render_template('course-overview.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
