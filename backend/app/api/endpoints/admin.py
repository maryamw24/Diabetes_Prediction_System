from fastapi import APIRouter, Depends, HTTPException
from app.db import (
    get_todays_logs,
    get_new_users,
    get_all_users,
    ban_user,
    get_user_by_email,
)
from app.dependencies import get_admin_user
from typing import List
from app.schemas.auth import User as UserSchema

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/logs/today")
async def get_todays_logs_endpoint(admin: dict = Depends(get_admin_user)):
    return get_todays_logs()


@router.get("/users/new", response_model=List[UserSchema])
async def get_new_users_endpoint(admin: dict = Depends(get_admin_user)):
    return get_new_users()


@router.get("/users", response_model=List[UserSchema])
async def get_all_users_endpoint(admin: dict = Depends(get_admin_user)):
    return get_all_users()


@router.post("/users/ban/{user_id}")
async def ban_user_endpoint(user_id: int, admin: dict = Depends(get_admin_user)):
    user = get_user_by_email(admin["email"])
    if user["id"] == user_id:
        raise HTTPException(status_code=403, detail="Cannot ban yourself")
    target_user = next((u for u in get_all_users() if u["id"] == user_id), None)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if target_user["role"] == "admin":
        raise HTTPException(status_code=403, detail="Cannot ban an admin")
    ban_user(user_id)
    return {"message": f"User {user_id} banned successfully"}
