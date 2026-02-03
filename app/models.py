"""
Database models for LJCourses platform
"""
from datetime import datetime
from app.db import Base
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole:
    STUDENT = 'student'
    # INSTRUCTOR = 'instructor'
    # ADMIN = 'admin'

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
    major = Column(String(30), nullable=True)

    # Status fields
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    # enrolled_courses = relationship('Enrollment', back_populates='student', lazy='dynamic')
    # taught_courses = relationship('Course', back_populates='instructor', lazy='dynamic')
    # submissions = relationship('AssignmentSubmission', back_populates='student', lazy='dynamic')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'