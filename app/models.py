"""
Database models for LJCourses platform
"""
from datetime import datetime
from app.db import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole:
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ADMIN = 'admin'

class DifficultyLevel:
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

class User(Base):
    """User model for students, instructors, and admins"""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.STUDENT)

    # Profile fields
    profile_image = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    major = Column(String(100), nullable=True)

    # Status fields
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    enrollments = relationship('Enrollment', back_populates='student', lazy='dynamic', cascade='all, delete-orphan')
    taught_courses = relationship('Course', back_populates='instructor', lazy='dynamic', foreign_keys='Course.instructor_id')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Category(Base):
    """Course category model"""
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Material icon name
    color = Column(String(7), nullable=True)  # Hex color code (e.g., #FF6B6B)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    courses = relationship('Course', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class Course(Base):
    """Course model"""
    __tablename__ = 'courses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    thumbnail = Column(String(255), nullable=True)  # Course thumbnail image URL
    duration_hours = Column(Integer, nullable=True)  # Estimated completion time in hours
    difficulty_level = Column(String(20), nullable=True)  # Beginner, Intermediate, Advanced
    
    # Foreign Keys
    instructor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    
    # Status fields
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Rating
    rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    published_at = Column(DateTime, nullable=True)

    # Relationships
    instructor = relationship('User', back_populates='taught_courses', foreign_keys=[instructor_id])
    category = relationship('Category', back_populates='courses')
    lessons = relationship('Lesson', back_populates='course', lazy='dynamic', cascade='all, delete-orphan', order_by='Lesson.order')
    enrollments = relationship('Enrollment', back_populates='course', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.title}>'


class Lesson(Base):
    """Lesson model - individual lessons/modules within a course"""
    __tablename__ = 'lessons'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Rich text lesson content (HTML)
    video_url = Column(String(255), nullable=True)  # Video resource URL
    video_duration = Column(Integer, nullable=True)  # Video duration in seconds
    resources_url = Column(String(255), nullable=True)  # Additional resources link
    order = Column(Integer, default=0)  # Display order in course
    is_free = Column(Boolean, default=False)  # Free preview lesson
    is_published = Column(Boolean, default=True)  # Publication status
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    course = relationship('Course', back_populates='lessons')
    lesson_progress = relationship('LessonProgress', back_populates='lesson', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Lesson {self.title}>'


class Enrollment(Base):
    """Enrollment model - tracks student enrollments in courses"""
    __tablename__ = 'enrollments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    is_active = Column(Boolean, default=True)  # Enrollment active status
    progress_percentage = Column(Float, default=0.0)  # Course completion (0-100)
    
    # Timestamps
    enrolled_at = Column(DateTime, default=datetime.now, nullable=False)
    completed_at = Column(DateTime, nullable=True)  # Course completion timestamp
    last_accessed = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    student = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
    lesson_progress = relationship('LessonProgress', back_populates='enrollment', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Enrollment student_id={self.student_id} course_id={self.course_id}>'


class LessonProgress(Base):
    """Lesson progress model - tracks individual lesson completion for each enrollment"""
    __tablename__ = 'lesson_progress'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.id'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    is_completed = Column(Boolean, default=False)  # Completion status
    watch_time = Column(Integer, default=0)  # Time watched in seconds
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.now, nullable=False)  # First access timestamp
    completed_at = Column(DateTime, nullable=True)  # Completion timestamp
    last_accessed = Column(DateTime, default=datetime.now, nullable=False)  # Last access timestamp

    # Relationships
    enrollment = relationship('Enrollment', back_populates='lesson_progress')
    lesson = relationship('Lesson', back_populates='lesson_progress')

    def __repr__(self):
        return f'<LessonProgress enrollment_id={self.enrollment_id} lesson_id={self.lesson_id}>'