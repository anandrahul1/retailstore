from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import sys
import os

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from models import User, UserCreate, UserLogin, Token, APIResponse
from database import db_client, DatabaseConfig
from auth import get_password_hash, verify_password, create_token_pair, get_current_user
from events import event_handlers
from utils import ResponseFormatter, validate_email, validate_phone
from boto3.dynamodb.conditions import Attr
import uuid

app = FastAPI(
    title="User Management Service",
    description="Handles user authentication, registration, and profile management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.post("/register", response_model=APIResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        # Validate email format
        if not validate_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Validate phone if provided
        if user_data.phone and not validate_phone(user_data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )
        
        # Check if user already exists
        existing_users = await db_client.scan_items(
            DatabaseConfig.USERS_TABLE,
            filter_condition=Attr('email').eq(user_data.email)
        )
        
        if existing_users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Check username availability
        existing_username = await db_client.scan_items(
            DatabaseConfig.USERS_TABLE,
            filter_condition=Attr('username').eq(user_data.username)
        )
        
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)
        
        user_item = {
            "id": user_id,
            "email": user_data.email,
            "username": user_data.username,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "password_hash": hashed_password,
            "role": "customer",
            "is_active": True,
            "phone": user_data.phone
        }
        
        created_user = await db_client.create_item(DatabaseConfig.USERS_TABLE, user_item)
        
        # Remove password hash from response
        created_user.pop('password_hash', None)
        
        # Publish user registration event
        await event_handlers.handle_user_registered({
            "user_id": user_id,
            "email": user_data.email,
            "username": user_data.username,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name
        })
        
        return ResponseFormatter.success(
            data=created_user,
            message="User registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering user: {str(e)}"
        )

@app.post("/login", response_model=Token)
async def login_user(login_data: UserLogin):
    """Authenticate user and return tokens"""
    try:
        # Find user by email
        users = await db_client.scan_items(
            DatabaseConfig.USERS_TABLE,
            filter_condition=Attr('email').eq(login_data.email)
        )
        
        if not users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        user = users[0]
        
        # Verify password
        if not verify_password(login_data.password, user['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.get('is_active', True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Create tokens
        token_data = {
            "sub": user['id'],
            "email": user['email'],
            "role": user['role']
        }
        
        tokens = create_token_pair(token_data)
        
        return Token(**tokens)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

@app.get("/profile", response_model=APIResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    try:
        user = await db_client.get_item(
            DatabaseConfig.USERS_TABLE,
            {"id": current_user["user_id"]}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Remove sensitive data
        user.pop('password_hash', None)
        
        return ResponseFormatter.success(
            data=user,
            message="Profile retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving profile: {str(e)}"
        )

@app.put("/profile", response_model=APIResponse)
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        # Remove sensitive fields that shouldn't be updated
        profile_data.pop('id', None)
        profile_data.pop('email', None)
        profile_data.pop('password_hash', None)
        profile_data.pop('role', None)
        profile_data.pop('created_at', None)
        
        # Validate phone if provided
        if 'phone' in profile_data and profile_data['phone']:
            if not validate_phone(profile_data['phone']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid phone number format"
                )
        
        updated_user = await db_client.update_item(
            DatabaseConfig.USERS_TABLE,
            {"id": current_user["user_id"]},
            profile_data
        )
        
        # Remove sensitive data
        updated_user.pop('password_hash', None)
        
        return ResponseFormatter.success(
            data=updated_user,
            message="Profile updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating profile: {str(e)}"
        )

@app.post("/change-password", response_model=APIResponse)
async def change_password(
    password_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Change user password"""
    try:
        current_password = password_data.get('current_password')
        new_password = password_data.get('new_password')
        
        if not current_password or not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password and new password are required"
            )
        
        # Get user
        user = await db_client.get_item(
            DatabaseConfig.USERS_TABLE,
            {"id": current_user["user_id"]}
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not verify_password(current_password, user['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        new_password_hash = get_password_hash(new_password)
        await db_client.update_item(
            DatabaseConfig.USERS_TABLE,
            {"id": current_user["user_id"]},
            {"password_hash": new_password_hash}
        )
        
        return ResponseFormatter.success(
            message="Password changed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error changing password: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "user-management"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)