"""
Instructor management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Instructor

def get_instructor_by_id(db: Session, instructor_id: UUID) -> Optional[Instructor]:
    """Get instructor by UUID"""
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()


def get_all_instructors(db: Session, skip: int = 0, limit: int = 100) -> list[type[Instructor]]:
    """Get all instructors"""
    return db.query(Instructor).offset(skip).limit(limit).all()


def create_instructor(db: Session, name: str, designation: Optional[str] = None, 
                     image: Optional[str] = None) -> Instructor:
    """Create a new instructor"""
    try:
        instructor = Instructor(name=name, designation=designation, image=image)
        db.add(instructor)
        db.commit()
        db.refresh(instructor)
        return instructor
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create instructor") from e


def update_instructor(db: Session, instructor_id: UUID, **kwargs) -> Optional[Instructor]:
    """Update instructor by UUID"""
    instructor = get_instructor_by_id(db, instructor_id)
    if not instructor:
        return None
    
    allowed_fields = ['name', 'designation', 'image']
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
