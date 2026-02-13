"""
Course management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import Course

def get_course_by_id(db: Session, course_id: UUID, include_relations: bool = False) -> Optional[Course]:
    """Get course by UUID with optional nested relationships"""
    query = db.query(Course)
    if include_relations:
        query = query.options(
            joinedload(Course.instructor),
            joinedload(Course.category),
            joinedload(Course.lessons)
        )
    return query.filter(Course.id == course_id).first()


def get_course_by_slug(db: Session, slug: str, include_relations: bool = False) -> Optional[Course]:
    """Get course by slug with optional nested relationships"""
    query = db.query(Course)
    if include_relations:
        query = query.options(
            joinedload(Course.instructor),
            joinedload(Course.category),
            joinedload(Course.lessons)
        )
    return query.filter(Course.slug == slug).first()


def get_all_courses(db: Session, skip: int = 0, limit: int = 100, 
                    category_id: Optional[UUID] = None,
                    instructor_id: Optional[UUID] = None,
                    difficulty_level: Optional[str] = None,
                    search: Optional[str] = None) -> list[type[Course]]:
    """Get all courses with optional filters"""
    query = db.query(Course).options(
        joinedload(Course.instructor),
        joinedload(Course.category)
    )
    
    if category_id:
        query = query.filter(Course.category_id == category_id)
    if instructor_id:
        query = query.filter(Course.instructor_id == instructor_id)
    if difficulty_level:
        query = query.filter(Course.difficulty_level == difficulty_level)
    if search:
        search_term = f"%{search}%"
        from sqlalchemy import or_
        from app.models import User
        query = query.join(Course.instructor).filter(
            or_(
                Course.title.ilike(search_term),
                Course.description.ilike(search_term),
                Course.small_description.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        )
    
    return query.offset(skip).limit(limit).all()


def create_course(db: Session, instructor_id: UUID, category_id: UUID, 
                 title: str, slug: str, **kwargs) -> Course:
    """Create a new course"""
    try:
        course = Course(
            instructor_id=instructor_id,
            category_id=category_id,
            title=title,
            slug=slug,
            **kwargs
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Course with this slug already exists") from e


def update_course(db: Session, course_id: UUID, **kwargs) -> Optional[Course]:
    """Update course by UUID"""
    course = get_course_by_id(db, course_id)
    if not course:
        return None
    
    allowed_fields = [
        'title', 'slug', 'small_description', 'description', 'thumbnail',
        'duration_hours', 'difficulty_level', 'rating', 'course_purpose',
        'learning_objectives', 'topics_covered', 'instructor_id', 'category_id',
        'published_at'
    ]
    
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(course, field, value)
    
    course.updated_at = datetime.now()
    
    try:
        db.commit()
        db.refresh(course)
        return course
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Course with this slug already exists") from e


def delete_course(db: Session, course_id: UUID) -> bool:
    """Delete course by UUID (cascades to lessons and enrollments)"""
    course = get_course_by_id(db, course_id)
    if not course:
        return False
    
    db.delete(course)
    db.commit()
    return True
