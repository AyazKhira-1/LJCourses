from flask import Blueprint, render_template, request, url_for, session
from app.db import SessionLocal
from app.models import Course, Enrollment, Lesson
from app.services import (
    get_all_courses, get_course_by_slug, get_course_by_id,
    get_all_categories, get_category_by_slug, create_enrollment,
    get_lesson_by_id, get_lessons_by_course,
    create_lesson_progress, update_lesson_progress, get_progress_by_enrollment,
    get_user_by_id
)
from app.utils import format_duration, get_current_user_from_session, auth_required
from sqlalchemy.orm import joinedload
from datetime import datetime

bp = Blueprint('course', __name__)

@bp.route('/')
def home():
    """Home page"""
    return render_template('home.html')


@bp.route('/browse-courses')
def browse_courses():
    """Browse available courses page"""
    db = SessionLocal()
    try:
        user = get_current_user_from_session()
        
        # Get filter parameters
        category_slug = request.args.get('category')
        
        # Get all categories for filter buttons
        categories = get_all_categories(db)
        
        # Get courses with optional category filter
        category_id = None
        if category_slug and category_slug != 'all':
            category = get_category_by_slug(db, category_slug)
            if category:
                category_id = category.id
        
        courses = get_all_courses(db, category_id=category_id)
        
        return render_template('browse-courses.html', 
                             courses=courses, 
                             categories=categories,
                             selected_category=category_slug or 'all',
                             user=user,
                             format_duration=format_duration)
    finally:
        db.close()


@bp.route('/course')
@bp.route('/course/<course_slug>')
def course_overview(course_slug=None):
    """Course overview page"""
    db = SessionLocal()
    try:
        user = get_current_user_from_session()
        
        if course_slug:
            course = get_course_by_slug(db, course_slug, include_relations=True)
        else:
            # Get first course if no slug provided (fallback)
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


@bp.route('/lesson')
@bp.route('/lesson/<lesson_id>')
@auth_required
def lesson(lesson_id=None):
    """Individual lesson page"""
    db = SessionLocal()
    try:
        user = get_user_by_id(db, session['user_id'])
        
        course_slug = request.args.get('course')
        current_lesson = None
        
        if lesson_id:
            # Get specific lesson
            current_lesson = get_lesson_by_id(db, lesson_id)
        elif course_slug:
            # Get first lesson of specified course
            course = get_course_by_slug(db, course_slug)
            if course:
                current_lesson = db.query(Lesson).filter(
                    Lesson.course_id == course.id
                ).order_by(Lesson.order).first()
        else:
            # Get first lesson from first enrolled course
            enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == user.id
            ).first()
            if enrollment:
                current_lesson = db.query(Lesson).filter(
                    Lesson.course_id == enrollment.course_id
                ).order_by(Lesson.order).first()
        
        if not current_lesson:
            return render_template('lesson.html', lesson=None, course=None, lessons=[], user=user)
        
        # Get the course and all its lessons
        course = get_course_by_id(db, current_lesson.course_id, include_relations=True)
        
        # Get ordered lessons for sidebar
        lessons = sorted(course.lessons, key=lambda l: l.order) if course else []
        
        # Get enrollment and progress for current user
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == user.id,
            Enrollment.course_id == course.id
        ).first()
        
        progress_map = {}
        if enrollment:
            # Update last accessed
            enrollment.last_accessed = datetime.now()
            db.commit()

            progress_records = get_progress_by_enrollment(db, enrollment.id)
            progress_map = {str(p.lesson_id): p for p in progress_records}
            
            # Start tracking this lesson if not already
            if str(current_lesson.id) not in progress_map:
                create_lesson_progress(db, enrollment.id, current_lesson.id)
                # Refresh map
                progress_records = get_progress_by_enrollment(db, enrollment.id)
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


@bp.route('/api/enrollments', methods=['POST'])
def enroll_course():
    """API to enroll a student in a course"""
    if 'user_id' not in session:
        return {"detail": "Authentication required"}, 401
        
    db = SessionLocal()
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        
        if not course_id:
            return {"detail": "Course ID is required"}, 400
            
        # Check if course exists
        course = get_course_by_id(db, course_id)
        if not course:
            return {"detail": "Course not found"}, 404
            
        try:
            create_enrollment(db, session['user_id'], course_id)
        except ValueError as e:
            # Already enrolled is acceptable, just redirect
            pass
        
        # Get first lesson to redirect to
        first_lesson = db.query(Lesson).filter(
            Lesson.course_id == course_id
        ).order_by(Lesson.order).first()
        
        if first_lesson:
            redirect_url = url_for('course.lesson', lesson_id=first_lesson.id)
        else:
            redirect_url = url_for('course.lesson') + f"?course={course.slug}"
            
        return {"success": True, "redirect_url": redirect_url}
        
    except Exception as e:
        return {"detail": str(e)}, 500
    finally:
        db.close()


@bp.route('/api/complete-lesson/<lesson_id>', methods=['POST'])
def complete_lesson(lesson_id):
    """API to mark a lesson as complete"""
    if 'user_id' not in session:
        return {"success": False, "error": "Unauthorized"}, 401
        
    db = SessionLocal()
    try:
        user_id = session['user_id']
        
        # Get lesson
        lesson = get_lesson_by_id(db, lesson_id)
        if not lesson:
            return {"success": False, "error": "Lesson not found"}, 404
            
        # Get enrollment
        enrollment = db.query(Enrollment).filter(
            Enrollment.student_id == user_id,
            Enrollment.course_id == lesson.course_id
        ).first()
        
        if not enrollment:
             # Auto enroll if not enrolled (edge case)
             enrollment = create_enrollment(db, user_id, lesson.course_id)

        # Mark progress complete
        progress = create_lesson_progress(db, enrollment.id, lesson_id)
        update_lesson_progress(db, progress.id, is_completed=True)
        
        # Check course completion
        lessons = get_lessons_by_course(db, lesson.course_id)
        all_progress = get_progress_by_enrollment(db, enrollment.id)
        
        completed_lesson_ids = {str(p.lesson_id) for p in all_progress if p.is_completed}
        
        all_complete = True
        for l in lessons:
            if str(l.id) not in completed_lesson_ids:
                all_complete = False
                break
        
        if all_complete:
            enrollment.completed_at = datetime.now()
            db.commit()

        # Find next lesson
        next_lesson = db.query(Lesson).filter(
            Lesson.course_id == lesson.course_id,
            Lesson.order > lesson.order
        ).order_by(Lesson.order).first()
        
        next_lesson_url = url_for('course.lesson', lesson_id=next_lesson.id) if next_lesson else None

        return {
            "success": True, 
            "next_lesson_url": next_lesson_url,
            "course_completed": all_complete
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}, 500
    finally:
        db.close()
