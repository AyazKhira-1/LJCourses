"""
Category management services
"""
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Category

def get_category_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    """Get category by UUID"""
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_slug(db: Session, slug: str) -> Optional[Category]:
    """Get category by slug"""
    return db.query(Category).filter(Category.slug == slug).first()


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> list[type[Category]]:
    """Get all categories"""
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, name: str, slug: str) -> Category:
    """Create a new category"""
    try:
        category = Category(name=name, slug=slug)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Category with this name or slug already exists") from e


def update_category(db: Session, category_id: UUID, **kwargs) -> Optional[Category]:
    """Update category by UUID"""
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    
    allowed_fields = ['name', 'slug']
    for field, value in kwargs.items():
        if field in allowed_fields and value is not None:
            setattr(category, field, value)
    
    category.updated_at = datetime.now()
    
    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Category with this slug already exists") from e


def delete_category(db: Session, category_id: UUID) -> bool:
    """Delete category by UUID"""
    category = get_category_by_id(db, category_id)
    if not category:
        return False
    
    db.delete(category)
    db.commit()
    return True
