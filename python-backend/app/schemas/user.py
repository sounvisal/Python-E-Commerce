from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re
import html

COMMON_WEAK_PASSWORDS = {
    "password", "password1234", "12345678", "123456789", "qwerty123",
    "admin123", "letmein123", "welcome123"
}

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    avatar: Optional[str] = "/images/avatars/avatar-default.png"

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        clean = html.escape(v.strip())
        if len(clean) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(clean) > 100:
            raise ValueError("Name cannot exceed 100 characters")
        return clean

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        clean = html.escape(v.strip())
        if len(clean) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(clean) > 100:
            raise ValueError("Name cannot exceed 100 characters")
        return clean

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 128:
            raise ValueError("Password cannot exceed 128 characters")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if v.lower() in COMMON_WEAK_PASSWORDS:
            raise ValueError("Password is too common and easily guessed. Please choose a stronger passphrase.")
        return v

class UserLogin(BaseModel):
    email: Optional[str] = None
    identifier: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def validate_login_target(self) -> 'UserLogin':
        login_val = (self.identifier or self.email or "").strip()
        if not login_val:
            raise ValueError("Email or phone number is required")
        if not self.email:
            self.email = login_val
        return self

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    addresses: Optional[List[Dict[str, Any]]] = None
    avatar: Optional[str] = None

class UserOut(UserBase):
    profile_data: Optional[Dict[str, Any]] = None
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    tier: str
    reward_points: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class AuthResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[Token] = None
