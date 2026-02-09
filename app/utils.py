from functools import wraps
from flask import session, redirect, url_for
from app.db import SessionLocal
from app.services import get_user_by_id
from app.config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def format_duration(hours):
    """Convert hours to 'Xh Ym' format"""
    if not hours:
        return "0h"
    h = int(hours)
    m = int((hours - h) * 60)
    if m > 0:
        return f"{h}h {m}m"
    return f"{h}h"

def get_current_user_from_session():
    """Get the currently logged-in user from session"""
    user_id = session.get('user_id')
    if user_id:
        db = SessionLocal()
        try:
            return get_user_by_id(db, user_id)
        finally:
            db.close()
    return None

def auth_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.student_login'))
        return f(*args, **kwargs)
    return decorated_function
