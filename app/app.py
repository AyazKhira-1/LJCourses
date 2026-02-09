"""
FastAPI application with student authentication and CRUD endpoints
"""
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import uvicorn
import os
from pathlib import Path
import shutil
from datetime import datetime as dt

from app.db import get_db, Base, engine
from app.models import User, UserRole
from app.schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, Token, PasswordReset,
    InstructorCreate, InstructorUpdate, InstructorResponse,
    CategoryCreate, CategoryUpdate, CategoryResponse,
    CourseCreate, CourseUpdate, CourseResponse,
    LessonCreate, LessonUpdate, LessonResponse,
    EnrollmentCreate, EnrollmentResponse,
    LessonProgressCreate, LessonProgressUpdate, LessonProgressResponse
)
from app.services import (
    # User services
    create_user, authenticate_user, get_user_by_id, get_user_by_email,
    get_all_students, update_last_login, update_user, delete_user,
    reset_user_password, deactivate_user,
    # Instructor services
    get_instructor_by_id, get_all_instructors, create_instructor,
    update_instructor, delete_instructor,
    # Category services
    get_category_by_id, get_category_by_slug, get_all_categories,
    create_category, update_category, delete_category,
    # Course services
    get_course_by_id, get_course_by_slug, get_all_courses,
    create_course, update_course, delete_course,
    # Lesson services
    get_lesson_by_id, get_lessons_by_course, get_all_lessons,
    create_lesson, update_lesson, delete_lesson,
    # Enrollment services
    get_enrollment_by_id, get_enrollments_by_student, get_enrollments_by_course,
    get_all_enrollments, create_enrollment, delete_enrollment,
    update_enrollment_access, complete_enrollment,
    # Lesson Progress services
    get_lesson_progress_by_id, get_progress_by_enrollment,
    create_lesson_progress, update_lesson_progress
)
from app.auth import create_access_token, get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="LJCourses API",
    description="Student Course Management System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LJCourses API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ==================== Authentication Endpoints ====================

@app.post("/api/auth/token")
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token endpoint for Swagger UI authentication
    Use email as username
    """
    # Authenticate user (username field contains the email)
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    update_last_login(db, user.id)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/auth/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Student signup endpoint"""

    # Validate passwords match
    if user_data.confirm_password and user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Create new user
        new_user = create_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            role=UserRole.STUDENT
        )

        # Create access token
        access_token = create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )

        return Token(
            access_token=access_token,
            user=UserResponse.model_validate(new_user)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Student login endpoint"""

    # Authenticate user
    user = authenticate_user(db, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    update_last_login(db, user.id)

    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return Token(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@app.post("/api/auth/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout endpoint - sets user's is_active to False"""
    deactivated_user = deactivate_user(db, current_user.id)
    
    if not deactivated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "message": "Logged out successfully",
        "email": deactivated_user.email
    }


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return UserResponse.model_validate(current_user)


@app.post("/api/auth/reset-password")
async def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    """
    Reset/change user password
    Used by both forgot password and change password flows
    """
    
    # Validate passwords match
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    try:
        # Reset password
        user = reset_user_password(db, data.email, data.new_password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found"
            )
        
        return {
            "message": "Password reset successful",
            "email": user.email
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ==================== Student CRUD Endpoints ====================

@app.get("/api/students", response_model=List[UserResponse])
async def get_students(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all students (requires authentication)"""
    students = get_all_students(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(student) for student in students]


@app.get("/api/students/{user_id}", response_model=UserResponse)
async def get_student(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get student by ID"""
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return UserResponse.model_validate(user)


@app.put("/api/students/{user_id}", response_model=UserResponse)
async def update_student(
        user_id: UUID,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Update student profile"""

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this profile"
        )

    try:
        # Filter out None values
        update_data = user_update.model_dump(exclude_unset=True)

        updated_user = update_user(db, user_id, **update_data)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return UserResponse.model_validate(updated_user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/api/students/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this profile"
        )

    success = delete_user(db, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None


# ==================== File Upload Endpoints ====================

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("static/uploads/profile_photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files for serving uploaded photos
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")


@app.post("/api/upload/profile-photo")
async def upload_profile_photo(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Upload profile photo for current user"""
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Allowed types: jpg, jpeg, png, webp"
        )
    
    # Validate file size (max 5MB)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()  # Get position (size)
    file.file.seek(0)  # Reset to beginning
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large. Maximum size is 5MB"
        )
    
    # Delete old profile photo if it exists
    if current_user.profile_image:
        try:
            # Extract filename from URL path
            old_photo_path = current_user.profile_image.replace('/uploads/profile_photos/', '')
            old_file_path = UPLOAD_DIR / old_photo_path
            
            # Delete old file if it exists
            if old_file_path.exists():
                old_file_path.unlink()
                print(f"Deleted old profile photo: {old_photo_path}")
        except Exception as e:
            print(f"Failed to delete old profile photo: {e}")
            # Continue with upload even if deletion fails
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{current_user.id}_{int(dt.now().timestamp())}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Update user's profile_image in database
    photo_url = f"/uploads/profile_photos/{unique_filename}"
    current_user.profile_image = photo_url
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Profile photo uploaded successfully",
        "photo_url": photo_url
    }


# ==================== Instructor CRUD Endpoints ====================

@app.get("/api/instructors", response_model=List[InstructorResponse])
async def get_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all instructors (public endpoint)"""
    instructors = get_all_instructors(db, skip=skip, limit=limit)
    return [InstructorResponse.model_validate(inst) for inst in instructors]


@app.get("/api/instructors/{instructor_id}", response_model=InstructorResponse)
async def get_instructor(instructor_id: UUID, db: Session = Depends(get_db)):
    """Get instructor by ID (public endpoint)"""
    instructor = get_instructor_by_id(db, instructor_id)
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return InstructorResponse.model_validate(instructor)


@app.post("/api/instructors", response_model=InstructorResponse, status_code=status.HTTP_201_CREATED)
async def create_instructor_endpoint(
    instructor_data: InstructorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new instructor (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create instructors"
        )
    
    try:
        new_instructor = create_instructor(
            db,
            name=instructor_data.name,
            designation=instructor_data.designation,
            image=instructor_data.image
        )
        return InstructorResponse.model_validate(new_instructor)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/instructors/{instructor_id}", response_model=InstructorResponse)
async def update_instructor_endpoint(
    instructor_id: UUID,
    instructor_data: InstructorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update instructor (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update instructors"
        )
    
    update_data = instructor_data.model_dump(exclude_unset=True)
    updated_instructor = update_instructor(db, instructor_id, **update_data)
    
    if not updated_instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    
    return InstructorResponse.model_validate(updated_instructor)


@app.delete("/api/instructors/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instructor_endpoint(
    instructor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete instructor (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete instructors"
        )
    
    success = delete_instructor(db, instructor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor not found"
        )
    return None


# ==================== Category CRUD Endpoints ====================

@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories (public endpoint)"""
    categories = get_all_categories(db, skip=skip, limit=limit)
    return [CategoryResponse.model_validate(cat) for cat in categories]


@app.get("/api/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: UUID, db: Session = Depends(get_db)):
    """Get category by ID (public endpoint)"""
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return CategoryResponse.model_validate(category)


@app.get("/api/categories/slug/{slug}", response_model=CategoryResponse)
async def get_category_by_slug_endpoint(slug: str, db: Session = Depends(get_db)):
    """Get category by slug (public endpoint)"""
    category = get_category_by_slug(db, slug)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return CategoryResponse.model_validate(category)


@app.post("/api/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new category (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create categories"
        )
    
    try:
        new_category = create_category(
            db,
            name=category_data.name,
            slug=category_data.slug
        )
        return CategoryResponse.model_validate(new_category)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/categories/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update category (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update categories"
        )
    
    try:
        update_data = category_data.model_dump(exclude_unset=True)
        updated_category = update_category(db, category_id, **update_data)
        
        if not updated_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        return CategoryResponse.model_validate(updated_category)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/api/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete category (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete categories"
        )
    
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return None


# ==================== Course CRUD Endpoints ====================

@app.get("/api/courses", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 100,
    category_id: UUID | None = None,
    instructor_id: UUID | None = None,
    difficulty_level: str | None = None,
    db: Session = Depends(get_db)
):
    """Get all courses with optional filters (public endpoint)"""
    courses = get_all_courses(
        db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        instructor_id=instructor_id,
        difficulty_level=difficulty_level
    )
    return [CourseResponse.model_validate(course) for course in courses]


@app.get("/api/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID, db: Session = Depends(get_db)):
    """Get course by ID with nested relationships (public endpoint)"""
    course = get_course_by_id(db, course_id, include_relations=True)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return CourseResponse.model_validate(course)


@app.get("/api/courses/slug/{slug}", response_model=CourseResponse)
async def get_course_by_slug_endpoint(slug: str, db: Session = Depends(get_db)):
    """Get course by slug with nested relationships (public endpoint)"""
    course = get_course_by_slug(db, slug, include_relations=True)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return CourseResponse.model_validate(course)


@app.post("/api/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course_endpoint(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new course (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can create courses"
        )
    
    try:
        course_dict = course_data.model_dump()
        new_course = create_course(db, **course_dict)
        return CourseResponse.model_validate(new_course)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/courses/{course_id}", response_model=CourseResponse)
async def update_course_endpoint(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update course (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can update courses"
        )
    
    try:
        update_data = course_data.model_dump(exclude_unset=True)
        updated_course = update_course(db, course_id, **update_data)
        
        if not updated_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return CourseResponse.model_validate(updated_course)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course_endpoint(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete course (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can delete courses"
        )
    
    success = delete_course(db, course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return None


# ==================== Lesson CRUD Endpoints ====================

@app.get("/api/lessons", response_model=List[LessonResponse])
async def get_lessons_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all lessons (public endpoint)"""
    lessons = get_all_lessons(db, skip=skip, limit=limit)
    return [LessonResponse.model_validate(lesson) for lesson in lessons]


@app.get("/api/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: UUID, db: Session = Depends(get_db)):
    """Get lesson by ID (public endpoint)"""
    lesson = get_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    return LessonResponse.model_validate(lesson)


@app.get("/api/courses/{course_id}/lessons", response_model=List[LessonResponse])
async def get_course_lessons(course_id: UUID, db: Session = Depends(get_db)):
    """Get all lessons for a course, ordered (public endpoint)"""
    lessons = get_lessons_by_course(db, course_id)
    return [LessonResponse.model_validate(lesson) for lesson in lessons]


@app.post("/api/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson_endpoint(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new lesson (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can create lessons"
        )
    
    try:
        lesson_dict = lesson_data.model_dump()
        new_lesson = create_lesson(db, **lesson_dict)
        return LessonResponse.model_validate(new_lesson)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson_endpoint(
    lesson_id: UUID,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update lesson (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can update lessons"
        )
    
    update_data = lesson_data.model_dump(exclude_unset=True)
    updated_lesson = update_lesson(db, lesson_id, **update_data)
    
    if not updated_lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    return LessonResponse.model_validate(updated_lesson)


@app.delete("/api/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson_endpoint(
    lesson_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete lesson (instructor/admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors and admins can delete lessons"
        )
    
    success = delete_lesson(db, lesson_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    return None


# ==================== Enrollment CRUD Endpoints ====================

@app.get("/api/enrollments", response_model=List[EnrollmentResponse])
async def get_enrollments_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all enrollments (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all enrollments"
        )
    
    enrollments = get_all_enrollments(db, skip=skip, limit=limit)
    return [EnrollmentResponse.model_validate(enr) for enr in enrollments]


@app.get("/api/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(
    enrollment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get enrollment by ID (requires authentication)"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Only allow student to view their own enrollments or admin
    if enrollment.student_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this enrollment"
        )
    
    return EnrollmentResponse.model_validate(enrollment)


@app.get("/api/students/me/enrollments", response_model=List[EnrollmentResponse])
async def get_my_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's enrollments"""
    enrollments = get_enrollments_by_student(db, current_user.id)
    return [EnrollmentResponse.model_validate(enr) for enr in enrollments]


@app.post("/api/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Enroll current user in a course"""
    try:
        new_enrollment = create_enrollment(
            db,
            student_id=current_user.id,
            course_id=enrollment_data.course_id
        )
        # Refresh to get nested relationships
        enrollment = get_enrollment_by_id(db, new_enrollment.id)
        return EnrollmentResponse.model_validate(enrollment)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.delete("/api/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_from_course(
    enrollment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Unenroll from a course"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Only allow student to unenroll themselves or admin
    if enrollment.student_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this enrollment"
        )
    
    success = delete_enrollment(db, enrollment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return None


# ==================== Lesson Progress CRUD Endpoints ====================

@app.get("/api/enrollments/{enrollment_id}/progress", response_model=List[LessonProgressResponse])
async def get_enrollment_progress(
    enrollment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all lesson progress for an enrollment"""
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Only allow student to view their own progress or admin
    if enrollment.student_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this progress"
        )
    
    progress_records = get_progress_by_enrollment(db, enrollment_id)
    return [LessonProgressResponse.model_validate(prog) for prog in progress_records]


@app.get("/api/lesson-progress/{progress_id}", response_model=LessonProgressResponse)
async def get_lesson_progress(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific lesson progress"""
    progress = get_lesson_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson progress not found"
        )
    
    # Verify user owns this progress
    enrollment = get_enrollment_by_id(db, progress.enrollment_id)
    if enrollment.student_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this progress"
        )
    
    return LessonProgressResponse.model_validate(progress)


@app.post("/api/lesson-progress", response_model=LessonProgressResponse, status_code=status.HTTP_201_CREATED)
async def start_lesson(
    progress_data: LessonProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a lesson (create progress record)"""
    # Verify user owns the enrollment
    enrollment = get_enrollment_by_id(db, progress_data.enrollment_id)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    if enrollment.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create progress for this enrollment"
        )
    
    try:
        new_progress = create_lesson_progress(
            db,
            enrollment_id=progress_data.enrollment_id,
            lesson_id=progress_data.lesson_id
        )
        return LessonProgressResponse.model_validate(new_progress)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.put("/api/lesson-progress/{progress_id}", response_model=LessonProgressResponse)
async def update_lesson_progress_endpoint(
    progress_id: UUID,
    progress_data: LessonProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update lesson progress (mark as complete)"""
    progress = get_lesson_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson progress not found"
        )
    
    # Verify user owns this progress
    enrollment = get_enrollment_by_id(db, progress.enrollment_id)
    if enrollment.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this progress"
        )
    
    is_completed = progress_data.is_completed if progress_data.is_completed is not None else False
    updated_progress = update_lesson_progress(db, progress_id, is_completed=is_completed)
    
    if not updated_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson progress not found"
        )
    
    return LessonProgressResponse.model_validate(updated_progress)



# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )