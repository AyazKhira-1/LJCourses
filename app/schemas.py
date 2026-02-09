"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ========== User schemas ==========
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    confirm_password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    major: Optional[str] = None


class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    full_name: str
    role: str
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    major: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None


class PasswordReset(BaseModel):
    """Schema for password reset/change requests"""
    email: EmailStr
    new_password: str = Field(..., min_length=8)
    confirm_password: str


# ========== Instructor schemas ==========
class InstructorBase(BaseModel):
    name: str = Field(..., max_length=100)
    designation: Optional[str] = Field(None, max_length=200)
    image: Optional[str] = None


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    designation: Optional[str] = Field(None, max_length=200)
    image: Optional[str] = None


class InstructorResponse(InstructorBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Category schemas ==========
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=100)


class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Course schemas ==========
class CourseBase(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=200)
    small_description: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration_hours: Optional[float] = None
    difficulty_level: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=5)
    course_purpose: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    topics_covered: Optional[List[str]] = None


class CourseCreate(CourseBase):
    instructor_id: UUID
    category_id: UUID


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    slug: Optional[str] = Field(None, max_length=200)
    small_description: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration_hours: Optional[float] = None
    difficulty_level: Optional[str] = Field(None, max_length=50)
    rating: Optional[float] = Field(None, ge=0, le=5)
    course_purpose: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    topics_covered: Optional[List[str]] = None
    instructor_id: Optional[UUID] = None
    category_id: Optional[UUID] = None


class CourseResponse(CourseBase):
    id: UUID
    instructor_id: UUID
    category_id: UUID
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Nested relationships
    instructor: Optional[InstructorResponse] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Lesson schemas ==========
class LessonBase(BaseModel):
    title: str = Field(..., max_length=200)
    order: int = Field(..., ge=1)
    description: Optional[str] = None
    video_duration: Optional[int] = None  # in seconds
    video_url: Optional[str] = None


class LessonCreate(LessonBase):
    course_id: UUID


class LessonUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    order: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None
    video_duration: Optional[int] = None
    video_url: Optional[str] = None


class LessonResponse(LessonBase):
    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Enrollment schemas ==========
class EnrollmentBase(BaseModel):
    pass


class EnrollmentCreate(BaseModel):
    course_id: UUID


class EnrollmentResponse(EnrollmentBase):
    id: UUID
    student_id: UUID
    course_id: UUID
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ========== Lesson Progress schemas ==========
class LessonProgressBase(BaseModel):
    is_completed: bool = False


class LessonProgressCreate(BaseModel):
    enrollment_id: UUID
    lesson_id: UUID


class LessonProgressUpdate(BaseModel):
    is_completed: Optional[bool] = None


class LessonProgressResponse(LessonProgressBase):
    id: UUID
    enrollment_id: UUID
    lesson_id: UUID
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
