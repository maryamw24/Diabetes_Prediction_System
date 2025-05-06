from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_user_by_email, create_user, verify_user, update_verification_code
from app.schemas.auth import UserCreate, Token, VerifyRequest, ResendEmailRequest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    send_verification_email,
)
from datetime import timedelta
import random
import string

router = APIRouter(prefix="", tags=["Authentication"])


def generate_verification_code(length=6):
    return "".join(random.choices(string.digits, k=length))


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    verification_code = generate_verification_code()
    hashed_password = get_password_hash(user.password)
    create_user(user.email, hashed_password, verification_code)
    send_verification_email(user.email, verification_code)

    return {
        "message": "User created, please check your Mailtrap inbox for verification code"
    }


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user["is_verified"]:
        raise HTTPException(status_code=403, detail="Email not verified")
    if user["is_banned"]:
        raise HTTPException(status_code=403, detail="User is banned")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}


@router.post("/verify")
async def verify_email(request: VerifyRequest):
    if not verify_user(request.email, request.code):
        raise HTTPException(
            status_code=400, detail="Invalid email or verification code"
        )
    return {"message": "Email verified successfully"}


@router.post("/resend-email")
async def resend_email(request: ResendEmailRequest):
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user["is_verified"]:
        raise HTTPException(status_code=400, detail="Email already verified")

    new_code = generate_verification_code()
    update_verification_code(request.email, new_code)
    send_verification_email(request.email, new_code)
    return {"message": "Verification code resent"}
