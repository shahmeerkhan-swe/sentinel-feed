import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base, engine
from app.models.article import Article
from app.models.user import User
from app.models.preference import UserPreference

if __name__ == "__main__":
    print("[i] Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("[✓] Tables created successfully.")
    