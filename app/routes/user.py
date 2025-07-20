from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.auth.deps import get_current_user
from app.models.user import User
from app.crud.user import get_user_by_email, create_user, verify_password
from app.database import SessionLocal
from app.auth.jwt import create_access_tokens
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally: 
        db.close()

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)

def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = create_user(db, user_in)
    return user

@router.post(
    "/login",
    summary="Authenticate user and get JWT token"
)

def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_tokens(
        data={"sub": user.id}
    )

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.get(
    "/me", 
    response_model=UserOut,
    summary="Get current authenticated user"
)

def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

