"""
Lesson management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Lesson

def get_lesson_by_id(db: Session, lesson_id: UUID) -> Optional[Lesson]:
    """Get lesson by UUID"""
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def get_lessons_by_course(db: Session, course_id: UUID) -> list[type[Lesson]]:
    """Get all lessons for a course, ordered by lesson order"""
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()


def get_all_lessons(db: Session, skip: int = 0, limit: int = 100) -> list[type[Lesson]]:
    """Get all lessons"""
    return db.query(Lesson).offset(skip).limit(limit).all()


def create_lesson(db: Session, course_id: UUID, title: str, order: int, **kwargs) -> Lesson:
    """Create a new lesson"""
    try:
        lesson = Lesson(course_id=course_id, title=title, order=order, **kwargs)
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create lesson") from e


def update_lesson(db: Session, lesson_id: UUID, **kwargs) -> Optional[Lesson]:
    """Update lesson by UUID"""
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        return None
    
    allowed_fields = ['title', 'order', 'description', 'video_duration', 'video_url']
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(lesson, field, value)
    
    lesson.updated_at = datetime.now()
    db.commit()
    db.refresh(lesson)
    return lesson


def delete_lesson(db: Session, lesson_id: UUID) -> bool:
    """Delete lesson by UUID"""
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        return False
    
    db.delete(lesson)
    db.commit()
    return True
