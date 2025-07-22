from pydantic import BaseModel, Field, constr
from typing import List, Optional, Literal, Pattern

class PreferenceBase(BaseModel):
    sources: List[str] = Field(
        default_factory=list, 
        example=["Hacker News", "TechCrunch", "r/technology"],
        description="List of sources to include in the feed"
    )
    topics: List[str] = Field(
        default_factory=list,
        example=["AI", "blockchain"],
        description="List of keywords/topics to filter articles by"
    )
    frequency: Literal["daily", "weekly"]= Field(
        "daily",
        description="How often to send the digest: 'daily' or 'weekly'"
    )
    preferred_time: str = Field(
        "9:00",
        pattern="^[0-2][0-9]:[0-5][0-9]$",
        description="HH:MM 24-hour time for sending the digest"
    )

class PreferenceCreate(PreferenceBase):
    """
    All fields required to create a new preference.
    """

class PreferenceUpdate(BaseModel):
    """
    Any subset of fields to update an existing preference.
    """

    sources: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    frequency: Optional[str] = Field(
        default=None,
        pattern="^(daily|weekly)$",
        description="How often to send the digest: 'daily' or 'weekly'"
    )
    preferred_time: Optional[constr] = Field(
        default=None,
        pattern="^[0-2][0-9]:[0-5][0-9]$",
        description="HH:MM 24-hour time for sending the digest"
    )

class PreferenceOut(PreferenceBase):
    """
    What we return in API responses
    """

    id: str = Field(..., description="Unique preference record ID")
    user_id: str = Field(..., description="ID of the owning user")

    class Config: 
        orm_mode = True 