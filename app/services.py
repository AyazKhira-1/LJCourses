"""
Database service layer for CRUD operations
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models import (
    User, UserRole, Instructor, Category, Course, 
    Lesson, Enrollment, LessonProgress
)
from uuid import UUID
from typing import Optional, List
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


# ==================== Instructor Services ====================

def get_instructor_by_id(db: Session, instructor_id: UUID) -> Optional[Instructor]:
    """Get instructor by UUID"""
    return db.query(Instructor).filter(Instructor.id == instructor_id).first()


def get_all_instructors(db: Session, skip: int = 0, limit: int = 100) -> List[Instructor]:
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


# ==================== Category Services ====================

def get_category_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    """Get category by UUID"""
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_slug(db: Session, slug: str) -> Optional[Category]:
    """Get category by slug"""
    return db.query(Category).filter(Category.slug == slug).first()


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
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


# ==================== Course Services ====================

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
                    difficulty_level: Optional[str] = None) -> List[Course]:
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


# ==================== Lesson Services ====================

def get_lesson_by_id(db: Session, lesson_id: UUID) -> Optional[Lesson]:
    """Get lesson by UUID"""
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def get_lessons_by_course(db: Session, course_id: UUID) -> List[Lesson]:
    """Get all lessons for a course, ordered by lesson order"""
    return db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()


def get_all_lessons(db: Session, skip: int = 0, limit: int = 100) -> List[Lesson]:
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


# ==================== Enrollment Services ====================

def get_enrollment_by_id(db: Session, enrollment_id: UUID) -> Optional[Enrollment]:
    """Get enrollment by UUID"""
    return db.query(Enrollment).options(
        joinedload(Enrollment.course).joinedload(Course.instructor),
        joinedload(Enrollment.course).joinedload(Course.category)
    ).filter(Enrollment.id == enrollment_id).first()


def get_enrollments_by_student(db: Session, student_id: UUID) -> List[Enrollment]:
    """Get all enrollments for a student"""
    return db.query(Enrollment).options(
        joinedload(Enrollment.course).joinedload(Course.instructor),
        joinedload(Enrollment.course).joinedload(Course.category)
    ).filter(Enrollment.student_id == student_id).all()


def get_enrollments_by_course(db: Session, course_id: UUID) -> List[Enrollment]:
    """Get all enrollments for a course"""
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()


def get_all_enrollments(db: Session, skip: int = 0, limit: int = 100) -> List[Enrollment]:
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


# ==================== Lesson Progress Services ====================

def get_lesson_progress_by_id(db: Session, progress_id: UUID) -> Optional[LessonProgress]:
    """Get lesson progress by UUID"""
    return db.query(LessonProgress).options(
        joinedload(LessonProgress.lesson)
    ).filter(LessonProgress.id == progress_id).first()


def get_progress_by_enrollment(db: Session, enrollment_id: UUID) -> List[LessonProgress]:
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
