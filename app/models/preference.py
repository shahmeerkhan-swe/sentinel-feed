from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from uuid import uuid4
from app.database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"
    id            = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id       = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    sources       = Column(JSON, nullable=False, default=[])
    topics        = Column(JSON, nullable=False, default=[])
    frequency     = Column(JSON, nullable=False, default=["daily"])
    preferred_time = Column(String, nullable=False, default=["09:00"])

