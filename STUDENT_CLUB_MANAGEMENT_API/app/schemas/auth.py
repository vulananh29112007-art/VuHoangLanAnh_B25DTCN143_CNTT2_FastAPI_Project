from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# Dữ liệu client gửi lên khi đăng ký
class RegisterUser(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(
        min_length=6,
        max_length=50
    )


# Dữ liệu server trả về sau khi đăng ký
class RegisterResponse(BaseModel):
    message: str
    email: EmailStr


# Dữ liệu client gửi lên khi đăng nhập
class LoginUser(BaseModel):
    email: EmailStr
    password: str


# Dữ liệu server trả về sau khi đăng nhập
class TokenResponse(BaseModel):
    access_token: str
    token_type: str