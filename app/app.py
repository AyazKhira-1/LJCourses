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
    UserCreate, UserLogin, UserResponse, UserUpdate, Token, PasswordReset
)
from app.services import (
    create_user, authenticate_user, get_user_by_id, get_user_by_email,
    get_all_students, update_last_login, update_user, delete_user,
    reset_user_password
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