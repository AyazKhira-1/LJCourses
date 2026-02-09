"""
Enrollment management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import Enrollment, Course

def get_enrollment_by_id(db: Session, enrollment_id: UUID) -> Optional[Enrollment]:
    """Get enrollment by UUID"""
    return db.query(Enrollment).options(
        joinedload(Enrollment.course).joinedload(Course.instructor),
        joinedload(Enrollment.course).joinedload(Course.category)
    ).filter(Enrollment.id == enrollment_id).first()


def get_enrollments_by_student(db: Session, student_id: UUID) -> list[type[Enrollment]]:
    """Get all enrollments for a student"""
    return db.query(Enrollment).options(
        joinedload(Enrollment.course).joinedload(Course.instructor),
        joinedload(Enrollment.course).joinedload(Course.category)
    ).filter(Enrollment.student_id == student_id).all()


def get_enrollments_by_course(db: Session, course_id: UUID) -> list[type[Enrollment]]:
    """Get all enrollments for a course"""
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()


def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100) -> list[type[Enrollment]]:
    """Get all enrollments"""
    return db.query(Enrollment).offset(skip).limit(limit).all()


def create_enrollment(db: Session, student_id: UUID, course_id: UUID) -> Enrollment:
    """Create a new enrollment"""
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()
    
    if existing:
        raise ValueError("Student is already enrolled in this course")
    
    try:
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create enrollment") from e


def update_enrollment_access(db: Session, enrollment_id: UUID) -> Optional[Enrollment]:
    """Update enrollment's last_accessed timestamp"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return None
    
    enrollment.last_accessed = datetime.now()
    db.commit()
    db.refresh(enrollment)
    return enrollment


def complete_enrollment(db: Session, enrollment_id: UUID) -> Optional[Enrollment]:
    """Mark enrollment as completed"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return None
    
    enrollment.completed_at = datetime.now()
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment_id: UUID) -> bool:
    """Delete enrollment by UUID (unenroll)"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return False
    
    db.delete(enrollment)
    db.commit()
    return True
