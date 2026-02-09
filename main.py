from flask import Flask, render_template, request, redirect, url_for, session
from app.db import SessionLocal
from app.models import User, Course, Category, Instructor, Enrollment, Lesson, LessonProgress
from sqlalchemy.orm import joinedload
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ljcourses-secret-key-2024')

def format_duration(hours):
    """Convert hours to 'Xh Ym' format"""
    if not hours:
        return "0h"
    h = int(hours)
    m = int((hours - h) * 60)
    if m > 0:
        return f"{h}h {m}m"
    return f"{h}h"

def get_current_user(db):
    """Get the currently logged-in user from session"""
    user_id = session.get('user_id')
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return None

# Routes
@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    """Student login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user and user.check_password(password):
                session['user_id'] = str(user.id)
                session['user_name'] = user.full_name
                session['user_role'] = user.role
                return redirect(url_for('my_courses'))
            return render_template('student_login.html', error='Invalid email or password')
        finally:
            db.close()
    
    return render_template('student_login.html')


@app.route('/student-sign-up', methods=['GET', 'POST'])
def student_sign_up():
    """Student sign up page"""
    return render_template('student_sign_up.html')


@app.route('/logout')
def logout():
    """Log out the current user"""
    session.clear()
    return redirect(url_for('home'))


@app.route('/my-courses')
def my_courses():
    """My courses page - shows active enrolled courses for logged-in user"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        
        if not user:
            # Redirect to login if not authenticated
            return redirect(url_for('student_login'))
        
        # Get ONLY active enrollments (not completed) for the current user
        enrollments = db.query(Enrollment).options(
            joinedload(Enrollment.course).joinedload(Course.instructor),
            joinedload(Enrollment.course).joinedload(Course.category),
            joinedload(Enrollment.lesson_progress)
        ).filter(
            Enrollment.student_id == user.id,
            Enrollment.completed_at == None
        ).all()
        
        return render_template('my_courses.html', 
                             enrollments=enrollments, 
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@app.route('/completed-courses')
def completed_courses():
    """Completed courses page - shows finished courses for logged-in user"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        
        if not user:
            return redirect(url_for('student_login'))
        
        # Get ONLY completed enrollments for the current user
        enrollments = db.query(Enrollment).options(
            joinedload(Enrollment.course).joinedload(Course.instructor),
            joinedload(Enrollment.course).joinedload(Course.category),
            joinedload(Enrollment.lesson_progress)
        ).filter(
            Enrollment.student_id == user.id,
            Enrollment.completed_at != None
        ).all()
        
        return render_template('completed_courses.html', 
                             enrollments=enrollments, 
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@app.route('/profile')
def profile():
    """Student profile page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        if not user:
            return redirect(url_for('student_login'))
        return render_template('profile.html', user=user)
    finally:
        db.close()


@app.route('/browse-courses')
def browse_courses():
    """Browse available courses page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        
        # Get filter parameters
        category_slug = request.args.get('category')
        
        # Get all categories for filter buttons
        categories = db.query(Category).all()
        
        # Get courses with optional category filter
        query = db.query(Course).options(
            joinedload(Course.instructor),
            joinedload(Course.category)
        )
        
        if category_slug and category_slug != 'all':
            category = db.query(Category).filter(Category.slug == category_slug).first()
            if category:
                query = query.filter(Course.category_id == category.id)
        
        courses = query.all()
        
        return render_template('browse-courses.html', 
                             courses=courses, 
                             categories=categories,
                             selected_category=category_slug or 'all',
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@app.route('/settings')
def settings():
    """Settings page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        if not user:
            return redirect(url_for('student_login'))
        return render_template('settings.html', user=user)
    finally:
        db.close()


@app.route('/lesson')
@app.route('/lesson/<lesson_id>')
def lesson(lesson_id=None):
    """Individual lesson page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        if not user:
            return redirect(url_for('student_login'))
        
        course_slug = request.args.get('course')
        
        if lesson_id:
            # Get specific lesson
            current_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        elif course_slug:
            # Get first lesson of specified course
            course = db.query(Course).filter(Course.slug == course_slug).first()
            if course:
                current_lesson = db.query(Lesson).filter(
                    Lesson.course_id == course.id
                ).order_by(Lesson.order).first()
            else:
                current_lesson = None
        else:
            # Get first lesson from first enrolled course
            enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == user.id
            ).first()
            if enrollment:
                current_lesson = db.query(Lesson).filter(
                    Lesson.course_id == enrollment.course_id
                ).order_by(Lesson.order).first()
            else:
                current_lesson = None
        
        if not current_lesson:
            return render_template('lesson.html', lesson=None, course=None, lessons=[], user=user)
        
        # Get the course and all its lessons
        course = db.query(Course).options(
            joinedload(Course.lessons),
            joinedload(Course.instructor),
            joinedload(Course.category)
        ).filter(Course.id == current_lesson.course_id).first()
        
        # Get ordered lessons for sidebar
        lessons = sorted(course.lessons, key=lambda l: l.order) if course else []
        
        # Get enrollment and progress for current user
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == user.id,
            Enrollment.course_id == course.id
        ).first()
        
        progress_map = {}
        if enrollment:
            progress_records = db.query(LessonProgress).filter(
                LessonProgress.enrollment_id == enrollment.id
            ).all()
            progress_map = {str(p.lesson_id): p for p in progress_records}
        
        # Calculate progress percentage
        completed_count = sum(1 for p in progress_map.values() if p.is_completed)
        total_lessons = len(lessons)
        progress_percent = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0
        
        return render_template('lesson.html', 
                             lesson=current_lesson, 
                             course=course, 
                             lessons=lessons,
                             enrollment=enrollment,
                             progress_map=progress_map,
                             progress_percent=progress_percent,
                             completed_count=completed_count,
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@app.route('/course')
@app.route('/course/<course_slug>')
def course_overview(course_slug=None):
    """Course overview page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        
        if course_slug:
            course = db.query(Course).options(
                joinedload(Course.instructor),
                joinedload(Course.category),
                joinedload(Course.lessons)
            ).filter(Course.slug == course_slug).first()
        else:
            # Get first course if no slug provided
            course = db.query(Course).options(
                joinedload(Course.instructor),
                joinedload(Course.category),
                joinedload(Course.lessons)
            ).first()
        
        if not course:
            return render_template('course-overview.html', course=None, user=user)
        
        # Check if current user is enrolled
        enrollment = None
        if user:
            enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == user.id,
                Enrollment.course_id == course.id
            ).first()
        
        # Sort lessons by order
        lessons = sorted(course.lessons, key=lambda l: l.order) if course.lessons else []
        
        return render_template('course-overview.html', 
                             course=course, 
                             lessons=lessons,
                             enrollment=enrollment,
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@app.route('/change-password')
def change_password():
    """Change password page"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        return render_template('change_password.html', user=user)
    finally:
        db.close()


@app.route('/forgot-password')
def forgot_password():
    """Forgot password page"""
    return render_template('forgot_password.html')

@app.route('/api/enrollments', methods=['POST'])
def enroll_course():
    """API to enroll a student in a course"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        if not user:
            return {"detail": "Authentication required"}, 401
        
        data = request.get_json()
        course_id = data.get('course_id')
        
        if not course_id:
            return {"detail": "Course ID is required"}, 400
            
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return {"detail": "Course not found"}, 404
            
        # Check if already enrolled
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == user.id,
            Enrollment.course_id == course_id
        ).first()
        
        if not existing_enrollment:
            enrollment = Enrollment(
                student_id=user.id,
                course_id=course_id
            )
            db.add(enrollment)
            db.commit()
        
        # Get first lesson to redirect to
        first_lesson = db.query(Lesson).filter(
            Lesson.course_id == course_id
        ).order_by(Lesson.order).first()
        
        if first_lesson:
            redirect_url = url_for('lesson', lesson_id=first_lesson.id)
        else:
            redirect_url = url_for('lesson') + f"?course={course.slug}"
            
        return {"success": True, "redirect_url": redirect_url}
        
    except Exception as e:
        db.rollback()
        return {"detail": str(e)}, 500
    finally:
        db.close()

@app.route('/api/complete-lesson/<lesson_id>', methods=['POST'])
def complete_lesson(lesson_id):
    """API to mark a lesson as complete"""
    db = SessionLocal()
    try:
        user = get_current_user(db)
        if not user:
            return {"success": False, "error": "Unauthorized"}, 401

        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return {"success": False, "error": "Lesson not found"}, 404

        # Find or create enrollment
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == user.id,
            Enrollment.course_id == lesson.course_id
        ).first()

        if not enrollment:
            enrollment = Enrollment(
                student_id=user.id,
                course_id=lesson.course_id
            )
            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)

        # Find or create lesson progress
        progress = db.query(LessonProgress).filter(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.lesson_id == lesson_id
        ).first()

        if not progress:
            progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson_id,
                is_completed=True
            )
            db.add(progress)
        else:
            progress.is_completed = True
        
        db.commit()

        # Find next lesson
        next_lesson = db.query(Lesson).filter(
            Lesson.course_id == lesson.course_id,
            Lesson.order > lesson.order
        ).order_by(Lesson.order).first()
        
        # Check if course is completed (all lessons finished)
        if not next_lesson:
            # Check if there are any incomplete lessons in the course
            # We need to get all lessons and check strict completion
            total_lessons = db.query(Lesson).filter(Lesson.course_id == lesson.course_id).count()
            completed_lessons = db.query(LessonProgress).filter(
                LessonProgress.enrollment_id == enrollment.id,
                LessonProgress.is_completed == True
            ).count()
            
            # If this was the last lesson and all are marked complete
            if completed_lessons >= total_lessons:
                enrollment.completed_at = datetime.now()
                db.commit()
        
        next_lesson_url = url_for('lesson', lesson_id=next_lesson.id) if next_lesson else None

        return {
            "success": True, 
            "next_lesson_url": next_lesson_url,
            "course_completed": True if not next_lesson else False
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}, 500
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')
