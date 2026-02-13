"""
Database models for LJCourses platform
"""
from datetime import datetime
from app.db import Base
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, Float, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole:
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    HOD = 'hod'


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
    designation = Column(String(200), nullable=True)

    # Status fields
    is_active = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    enrollments = relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')
    courses = relationship('Course', back_populates='instructor')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'




class Category(Base):
    """Category model for course categorization"""
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    courses = relationship('Course', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name}>'


class Course(Base):
    """Course model for all courses on the platform"""
    __tablename__ = 'courses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    
    # Basic Information
    title = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    small_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    thumbnail = Column(String(500), nullable=True)
    
    # Course Details
    duration_hours = Column(Float, nullable=True)  # Duration in hours (e.g., 12.5 for 12h 30m)
    difficulty_level = Column(String(50), nullable=True)  # e.g., "Beginner to Pro", "Intermediate"
    rating = Column(Float, nullable=True, default=0.0)  # Rating out of 5
    
    # Extended Information
    course_purpose = Column(Text, nullable=True)
    learning_objectives = Column(ARRAY(Text), nullable=True)  # Array of learning objectives
    topics_covered = Column(ARRAY(String(200)), nullable=True)  # Array of topics
    
    # Timestamps
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    instructor = relationship('User', back_populates='courses')
    category = relationship('Category', back_populates='courses')
    lessons = relationship('Lesson', back_populates='course', cascade='all, delete-orphan', order_by='Lesson.order')
    enrollments = relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Course {self.title}>'


class Enrollment(Base):
    """Enrollment model linking students to courses"""
    __tablename__ = 'enrollments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
    )
    
    # Timestamps
    enrolled_at = Column(DateTime, default=datetime.now, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    last_accessed = Column(DateTime, nullable=True)

    # Relationships
    student = relationship('User', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
    lesson_progress = relationship('LessonProgress', back_populates='enrollment', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Enrollment student={self.student_id} course={self.course_id}>'


class Lesson(Base):
    """Lesson model for course lessons/videos"""
    __tablename__ = 'lessons'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    
    # Lesson Information
    order = Column(Integer, nullable=False)  # Order within the course
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    video_duration = Column(Integer, nullable=True)  # Duration in seconds
    video_url = Column(String(500), nullable=True)  # Video file/URL
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    course = relationship('Course', back_populates='lessons')
    lesson_progress = relationship('LessonProgress', back_populates='lesson', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Lesson {self.title}>'


class LessonProgress(Base):
    """Lesson progress model tracking student progress through lessons"""
    __tablename__ = 'lesson_progress'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrollment_id = Column(UUID(as_uuid=True), ForeignKey('enrollments.id'), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey('lessons.id'), nullable=False)
    
    # Progress Information
    is_completed = Column(Boolean, default=False)
    
    # Timestamps
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_accessed = Column(DateTime, nullable=True)

    # Relationships
    enrollment = relationship('Enrollment', back_populates='lesson_progress')
    lesson = relationship('Lesson', back_populates='lesson_progress')

    def __repr__(self):
        return f'<LessonProgress enrollment={self.enrollment_id} lesson={self.lesson_id}>'