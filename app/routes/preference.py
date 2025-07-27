from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user 
from app.database import SessionLocal
from app.crud.preference import get_preference, create_preference, update_preference, upsert_preference
from app.schemas.preference import PreferenceCreate, PreferenceOut, PreferenceUpdate
from app.schemas.user import UserOut
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@router.get(
    "/preferences",
    response_model=PreferenceOut,
    summary="Get current user's preferences"
)

def read_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pref = get_preference(db, current_user.id)
    if not pref: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    return pref

@router.post(
    "/preferences",
    response_model=PreferenceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create preferences for current user"
)

def create_prefs(
    pref_in: PreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = get_preference(db, current_user.id)
    if existing: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preferences already exist. Use PUT or PATCH to update"
        )
    return create_preference(db, current_user.id, pref_in)

@router.put(
    "/preferences",
    response_model=PreferenceOut,
    summary="Create or replace preferences for current user"
)

def upsert_prefs(
    pref_in: PreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return upsert_preference(db, current_user.id, pref_in)

@router.patch(
    "/preferences",
    response_model=PreferenceUpdate,
    summary="Update partial preferences for current user"
)
def patch_prefs(
    pref_update: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try: 
        return update_preference(db, current_user.id, pref_update)
    except ValueError as e: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )