"""
Instructor management services (using User model with role='instructor')
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, UserRole

def get_instructor_by_id(db: Session, instructor_id: UUID) -> Optional[User]:
    """Get instructor by UUID"""
    return db.query(User).filter(User.id == instructor_id, User.role == UserRole.INSTRUCTOR).first()


def get_all_instructors(db: Session, skip: int = 0, limit: int = 100) -> list[type[User]]:
    """Get all instructors"""
    return db.query(User).filter(User.role == UserRole.INSTRUCTOR).offset(skip).limit(limit).all()


def create_instructor(db: Session, full_name: str, email: str, password: str,
                     designation: Optional[str] = None, 
                     profile_image: Optional[str] = None) -> User:
    """Create a new instructor user"""
    try:
        instructor = User(
            full_name=full_name,
            email=email,
            role=UserRole.INSTRUCTOR,
            designation=designation,
            profile_image=profile_image
        )
        instructor.set_password(password)
        db.add(instructor)
        db.commit()
        db.refresh(instructor)
        return instructor
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create instructor") from e


def update_instructor(db: Session, instructor_id: UUID, **kwargs) -> Optional[User]:
    """Update instructor by UUID"""
    instructor = get_instructor_by_id(db, instructor_id)
    if not instructor:
        return None
    
    allowed_fields = ['full_name', 'designation', 'profile_image', 'bio', 'email']
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(instructor, field, value)
    
    instructor.updated_at = datetime.now()
    db.commit()
    db.refresh(instructor)
    return instructor


def delete_instructor(db: Session, instructor_id: UUID) -> bool:
    """Delete instructor by UUID"""
    instructor = get_instructor_by_id(db, instructor_id)
    if not instructor:
        return False
    
    db.delete(instructor)
    db.commit()
    return True
