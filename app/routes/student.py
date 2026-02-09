from flask import Blueprint, render_template, request, session, current_app
from app.db import SessionLocal
from app.models import Course, Enrollment
from app.services import get_user_by_id, update_user
from sqlalchemy.orm import joinedload
from app.utils import auth_required, format_duration, allowed_file, get_current_user_from_session
import os
from datetime import datetime
from werkzeug.utils import secure_filename

bp = Blueprint('student', __name__)

@bp.route('/my-courses')
@auth_required
def my_courses():
    """My courses page - shows active enrolled courses for logged-in user"""
    db = SessionLocal()
    try:
        user = get_user_by_id(db, session['user_id'])
        
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


@bp.route('/completed-courses')
@auth_required
def completed_courses():
    """Completed courses page - shows finished courses for logged-in user"""
    db = SessionLocal()
    try:
        user = get_user_by_id(db, session['user_id'])
        
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


@bp.route('/profile')
@auth_required
def profile():
    """Student profile page"""
    db = SessionLocal()
    try:
        user = get_user_by_id(db, session['user_id'])
        
        # Calculate stats
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == user.id).all()
        enrolled_count = len(enrollments)
        completed_count = sum(1 for e in enrollments if e.completed_at is not None)
        remaining_count = enrolled_count - completed_count
        
        return render_template('profile.html', 
                             user=user, 
                             enrolled_count=enrolled_count, 
                             completed_count=completed_count,
                             remaining_count=remaining_count)
    finally:
        db.close()


@bp.route('/settings')
@auth_required
def settings():
    """Settings page"""
    user = get_current_user_from_session()
    return render_template('settings.html', user=user)


@bp.route('/api/upload/profile-photo', methods=['POST'])
def upload_profile_photo():
    """Upload profile photo"""
    if 'user_id' not in session:
        return {"detail": "Authentication required"}, 401
        
    if 'file' not in request.files:
        return {"detail": "No file part"}, 400
        
    file = request.files['file']
    if file.filename == '':
        return {"detail": "No selected file"}, 400
        
    if file and allowed_file(file.filename):
        db = SessionLocal()
        try:
            user = get_user_by_id(db, session['user_id'])
            
            # Delete old profile photo if it exists
            if user.profile_image:
                 try:
                    # Robust way to get filename regardless of path prefix
                    old_filename = os.path.basename(user.profile_image)
                    old_file = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
                    if os.path.exists(old_file):
                        os.remove(old_file)
                 except Exception:
                     pass # Ignore errors deleting old file
            
            # Save new file
            filename = secure_filename(file.filename)
            unique_filename = f"{user.id}_{int(datetime.now().timestamp())}.{filename.split('.')[-1]}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            
            # Update user profile with correct static path
            new_profile_image = f"/static/uploads/profile_photos/{unique_filename}"
            update_user(db, user.id, profile_image=new_profile_image)
            
            return {
                "message": "Profile photo uploaded successfully",
                "photo_url": new_profile_image
            }
        except Exception as e:
            return {"detail": str(e)}, 500
        finally:
            db.close()
            
    return {"detail": "Invalid file type"}, 400


@bp.route('/api/students/<user_id>', methods=['PUT'])
def update_student_profile(user_id):
    """Update student profile"""
    if 'user_id' not in session:
        return {"detail": "Authentication required"}, 401
    
    if str(user_id) != session['user_id']:
        return {"detail": "Unauthorized"}, 403
        
    data = request.get_json()
    
    # Filter keys that are actually present in the request to support partial updates
    updatable_fields = ['full_name', 'bio', 'major', 'profile_image']
    update_data = {k: v for k, v in data.items() if k in updatable_fields}
    
    db = SessionLocal()
    try:
        updated_user = update_user(db, user_id, **update_data)
        
        if updated_user:
            # Update session name just in case
            session['user_name'] = updated_user.full_name
            
            return {
                "id": str(updated_user.id),
                "full_name": updated_user.full_name,
                "bio": updated_user.bio,
                "major": updated_user.major,
                "profile_image": updated_user.profile_image
            }
        return {"detail": "Update failed"}, 400
    except Exception as e:
        return {"detail": str(e)}, 500
    finally:
        db.close()
