"""Auth router — register, login, refresh, logout, me, profile."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.dependencies import get_current_user
from app.utils.security import (hash_password, verify_password, create_access_token, create_refresh_token)
from app.schemas import *

router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.execute(select(User).where(User.username == req.username)).scalar_one_or_none():
        raise HTTPException(400, "Username already taken")
    if db.execute(select(User).where(User.email == req.email)).scalar_one_or_none():
        raise HTTPException(400, "Email already registered")
    user = User(username=req.username, email=req.email, hashed_password=hash_password(req.password), role="user")
    db.add(user); db.commit(); db.refresh(user)
    at = create_access_token(user.id, user.username, user.role)
    rt = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token=rt, expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return TokenResponse(access_token=at, refresh_token=rt, username=user.username, email=user.email, role=user.role)

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.username == req.username)).scalar_one_or_none()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(401, "Invalid username or password")
    at = create_access_token(user.id, user.username, user.role)
    rt = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token=rt, expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return TokenResponse(access_token=at, refresh_token=rt, username=user.username, email=user.email, role=user.role)

@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshRequest, db: Session = Depends(get_db)):
    entry = db.execute(select(RefreshToken).where(RefreshToken.token == req.refresh_token, RefreshToken.is_revoked == "0", RefreshToken.expires_at > datetime.utcnow())).scalar_one_or_none()
    if not entry: raise HTTPException(401, "Invalid or expired refresh token")
    entry.is_revoked = "1"
    user = db.get(User, entry.user_id)
    at = create_access_token(user.id, user.username, user.role)
    new_rt = create_refresh_token(user.id)
    db.add(RefreshToken(user_id=user.id, token=new_rt, expires_at=datetime.utcnow() + timedelta(days=7)))
    db.commit()
    return TokenResponse(access_token=at, refresh_token=new_rt, username=user.username, email=user.email, role=user.role)

@router.post("/logout")
def logout(req: RefreshRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.execute(select(RefreshToken).where(RefreshToken.token == req.refresh_token)).scalar_one_or_none()
    if entry: entry.is_revoked = "1"; db.commit()
    return {"message": "Logged out"}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)): return user

@router.put("/me", response_model=UserOut)
def update_profile(req: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.email: user.email = req.email
    if req.phone is not None: user.phone = req.phone
    if req.avatar_url is not None: user.avatar_url = req.avatar_url
    db.commit(); db.refresh(user); return user

@router.put("/me/password")
def change_password(req: PasswordChange, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(req.old_password, user.hashed_password): raise HTTPException(400, "Wrong current password")
    user.hashed_password = hash_password(req.new_password)
    db.commit(); return {"message": "Password changed"}
