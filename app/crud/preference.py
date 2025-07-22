from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.preference import UserPreference
from app.schemas.preference import PreferenceCreate, PreferenceUpdate

def get_preference(db: Session, user_id: str) -> UserPreference | None: 
    """
    Retrieve the preferences record for a given user ID
    """
    return db.query(UserPreference).filter(UserPreference.user_id == user_id).first()

def create_preference(db: Session, user_id: str, pref_in: PreferenceCreate) -> UserPreference:
    """
    Create a new UserPreference record for the specified user.
    """

    db_pref = UserPreference(
        id=str(uuid4()),
        user_id=user_id,
        sources=pref_in.sources,
        topics=pref_in.topics,
        frequency=pref_in.frequency,
        preferred_time=pref_in.preferred_time
    )
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref

def update_preference(db: Session, user_id: str, pref_update: PreferenceUpdate) -> UserPreference:
    """
    Update an existing UserPreference record for the specified user.
    """

    db_pref = get_preference(db, user_id)
    if not db_pref:
        raise ValueError(f"No preferences found for user {user_id}")
    update_data = pref_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pref, field, value)
    db.commit()
    db.refresh(db_pref)
    return db_pref

def upsert_preference(db: Session, user_id: str, pref_in: PreferenceCreate) -> UserPreference:
    """
    Create or update a UserPreference record in one step.
    """

    existing = get_preference(db, user_id)
    if existing: 
        update_data = pref_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing
    return create_preference(db, user_id, pref_in)



