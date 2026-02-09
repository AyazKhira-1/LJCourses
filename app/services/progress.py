"""
Lesson Progress management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import LessonProgress

def get_lesson_progress_by_id(db: Session, progress_id: UUID) -> Optional[LessonProgress]:
    """Get lesson progress by UUID"""
    return db.query(LessonProgress).options(
        joinedload(LessonProgress.lesson)
    ).filter(LessonProgress.id == progress_id).first()


def get_progress_by_enrollment(db: Session, enrollment_id: UUID) -> list[type[LessonProgress]]:
    """Get all lesson progress records for an enrollment"""
    return db.query(LessonProgress).options(
        joinedload(LessonProgress.lesson)
    ).filter(LessonProgress.enrollment_id == enrollment_id).all()


def get_progress_by_enrollment_and_lesson(db: Session, enrollment_id: UUID, 
                                          lesson_id: UUID) -> Optional[LessonProgress]:
    """Get specific lesson progress for an enrollment"""
    return db.query(LessonProgress).filter(
        LessonProgress.enrollment_id == enrollment_id,
        LessonProgress.lesson_id == lesson_id
    ).first()


def create_lesson_progress(db: Session, enrollment_id: UUID, lesson_id: UUID) -> LessonProgress:
    """Create or get lesson progress record"""
    # Check if progress already exists
    existing = get_progress_by_enrollment_and_lesson(db, enrollment_id, lesson_id)
    if existing:
        return existing
    
    try:
        progress = LessonProgress(
            enrollment_id=enrollment_id,
            lesson_id=lesson_id,
            started_at=datetime.now(),
            last_accessed=datetime.now()
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create lesson progress") from e


def update_lesson_progress(db: Session, progress_id: UUID, is_completed: bool = False) -> Optional[LessonProgress]:
    """Update lesson progress"""
    progress = get_lesson_progress_by_id(db, progress_id)
    if not progress:
        return None
    
    progress.is_completed = is_completed
    progress.last_accessed = datetime.now()
    
    if is_completed and not progress.completed_at:
        progress.completed_at = datetime.now()
    
    db.commit()
    db.refresh(progress)
    return progress
