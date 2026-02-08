"""
Database service layer for user CRUD operations
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, UserRole
from uuid import UUID
from typing import Optional
from datetime import datetime


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """Get user by UUID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100, role: Optional[str] = None) -> list[type[User]]:
    """Get all users with optional filtering"""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.offset(skip).limit(limit).all()


def get_all_students(db: Session, skip: int = 0, limit: int = 100) -> list[type[User]]:
    """Get all students"""
    return get_all_users(db, skip, limit, role=UserRole.STUDENT)


def create_user(db: Session, email: str, password: str, full_name: str, 
                role: str = UserRole.STUDENT, **kwargs) -> User:
    """Create a new user"""
    try:
        # Create user instance
        user = User(
            email=email,
            full_name=full_name,
            role=role,
            **kwargs
        )
        
        # Set password hash
        user.set_password(password)
        
        # Add to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("User with this email or enrollment number already exists") from e


def update_user(db: Session, user_id: UUID, **kwargs) -> Optional[User]:
    """Update user by UUID"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    # Update allowed fields
    allowed_fields = ['full_name', 'bio', 'profile_image', 'major']

    for field, value in kwargs.items():
        if field in allowed_fields:
            # Special handling for profile_image removal - delete the file
            if field == 'profile_image' and value is None and user.profile_image:
                from pathlib import Path
                # Extract filename from URL path
                old_photo_path = user.profile_image.replace('/uploads/profile_photos/', '')
                # Build path to the file
                upload_dir = Path(__file__).parent.parent / 'static' / 'uploads' / 'profile_photos'
                old_file_path = upload_dir / old_photo_path
                
                # Delete old file if it exists
                if old_file_path.exists():
                    try:
                        old_file_path.unlink()
                        print(f"Deleted photo file: {old_photo_path}")
                    except Exception as e:
                        print(f"Failed to delete photo file: {e}")
            
            setattr(user, field, value)

    user.updated_at = datetime.now()

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Update failed: enrollment number may already exist") from e


def delete_user(db: Session, user_id: UUID) -> bool:
    """Delete user by UUID"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    # Delete user's profile photo if it exists
    if user.profile_image:
        from pathlib import Path
        try:
            # Extract filename from URL path
            old_photo_path = user.profile_image.replace('/uploads/profile_photos/', '')
            # Build path to the file
            upload_dir = Path(__file__).parent.parent / 'static' / 'uploads' / 'profile_photos'
            old_file_path = upload_dir / old_photo_path
            
            # Delete file if it exists
            if old_file_path.exists():
                old_file_path.unlink()
                print(f"Deleted profile photo: {old_photo_path}")
        except Exception as e:
            print(f"Failed to delete profile photo: {e}")

    db.delete(user)
    db.commit()
    return True

def update_last_login(db: Session, user_id: UUID) -> Optional[User]:
    """Update user's last login timestamp and set is_active to True"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    utcnow = datetime.now()
    user.last_login = utcnow
    user.is_active = True  # Reactivate user on login
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: UUID) -> Optional[User]:
    """Set user's is_active to False when they logout"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.is_active = False
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    if not user.check_password(password):
        return None
    
    return user


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets strength requirements:
    - At least 8 characters long
    - Include uppercase and lowercase letters
    - Include at least one number
    - Include at least one special character
    
    Returns: (is_valid, error_message)
    """
    import re
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must include at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must include at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must include at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must include at least one special character"
    
    return True, ""


def reset_user_password(db: Session, email: str, new_password: str) -> Optional[User]:
    """
    Reset user password by email
    Returns updated user or None if user not found
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    # Validate password strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        raise ValueError(error_msg)
    
    # Set new password
    user.set_password(new_password)
    user.updated_at = datetime.now()
    
    db.commit()
    db.refresh(user)
    return user
