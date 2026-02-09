from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db import SessionLocal
from app.services import get_user_by_email, create_user
from datetime import datetime
from app.utils import auth_required

bp = Blueprint('auth', __name__)

@bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    """Student login page"""
    if request.method == 'POST':
        # Check if request is JSON or Form data
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
        
        db = SessionLocal()
        try:
            user = get_user_by_email(db, email)
            if user and user.check_password(password):
                # Reactivate user if they were inactive
                user.is_active = True
                user.last_login = datetime.now()
                db.commit()
                
                session['user_id'] = str(user.id)
                session['user_name'] = user.full_name
                session['user_role'] = user.role
                
                # If JSON request, return JSON response
                if request.is_json or request.accept_mimetypes.accept_json:
                    return {"success": True, "redirect_url": url_for('student.my_courses')}
                
                return redirect(url_for('student.my_courses'))
            
            # Login failed
            if request.is_json or request.accept_mimetypes.accept_json:
                return {"detail": "Invalid email or password"}, 401
                
            return render_template('student_login.html', error='Invalid email or password')
        finally:
            db.close()
    
    return render_template('student_login.html')


@bp.route('/student-sign-up', methods=['GET', 'POST'])
def student_sign_up():
    """Student sign up page"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            full_name = data.get('full_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
        else:
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
             if request.is_json or request.accept_mimetypes.accept_json:
                 return {"detail": "Passwords do not match"}, 400
             return render_template('student_sign_up.html', error='Passwords do not match')

        db = SessionLocal()
        try:
            # Check if user exists
            if get_user_by_email(db, email):
                if request.is_json or request.accept_mimetypes.accept_json:
                    return {"detail": "Email already registered"}, 400
                return render_template('student_sign_up.html', error='Email already registered')
            
            # Create user
            new_user = create_user(db, email=email, password=password, full_name=full_name)
            
            # Log them in automatically
            session['user_id'] = str(new_user.id)
            session['user_name'] = new_user.full_name
            session['user_role'] = new_user.role
            
            if request.is_json or request.accept_mimetypes.accept_json:
                return {"success": True, "redirect_url": url_for('student.my_courses')}
            
            return redirect(url_for('student.my_courses'))
        except Exception as e:
            if request.is_json or request.accept_mimetypes.accept_json:
                return {"detail": str(e)}, 500
            return render_template('student_sign_up.html', error=str(e))
        finally:
            db.close()

    return render_template('student_sign_up.html')


@bp.route('/logout')
def logout():
    """Log out the current user"""
    from app.services import get_user_by_id  # Import locally to avoid circular imports if needed

    # Optional: set is_active to False on logout
    user_id = session.get('user_id')
    if user_id:
        db = SessionLocal()
        try:
            user = get_user_by_id(db, user_id)
            if user:
                user.is_active = False
                db.commit()
        finally:
            db.close()
            
    session.clear()
    return redirect(url_for('course.home'))


@bp.route('/change-password')
@auth_required
def change_password():
    """Change password page"""
    from app.utils import get_current_user_from_session
    user = get_current_user_from_session()
    return render_template('change_password.html', user=user)


@bp.route('/forgot-password')
def forgot_password():
    """Forgot password page"""
    return render_template('forgot_password.html')


# ==================== API Endpoints ====================

@bp.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    """Reset password API"""
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    if not email or not new_password or not confirm_password:
        return {"detail": "Missing required fields"}, 400
        
    if new_password != confirm_password:
        return {"detail": "Passwords do not match"}, 400
        
    db = SessionLocal()
    try:
        # Check if user exists
        user = get_user_by_email(db, email)
        if not user:
             return {"detail": "User with this email not found"}, 404
             
        user.set_password(new_password)
        db.commit()
        
        return {"message": "Password updated successfully"}
    except Exception as e:
        return {"detail": str(e)}, 500
    finally:
        db.close()


@bp.route('/api/auth/me', methods=['GET'])
def api_auth_me():
    """Get current logged-in user details"""
    from app.services import get_user_by_id

    if 'user_id' not in session:
         return {"detail": "Not authenticated"}, 401
    
    db = SessionLocal()
    try:
        user = get_user_by_id(db, session['user_id'])
        if not user:
             return {"detail": "User not found"}, 404
             
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "profile_image": user.profile_image,
            "bio": user.bio,
            "major": user.major,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    finally:
        db.close()
