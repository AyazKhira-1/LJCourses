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
    allowed_fields = ['full_name', 'bio', 'profile_image', 'major', 'enrollment_number', 'is_active', 'email_verified']

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

    db.delete(user)
    db.commit()
    return True


def update_last_login(db: Session, user_id: UUID) -> Optional[User]:
    """Update user's last login timestamp"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    utcnow = datetime.now()
    user.last_login = utcnow
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
