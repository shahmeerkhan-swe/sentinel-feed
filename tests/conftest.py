import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi.testclient import TestClient
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from app.database import Base 
from app.main import app
from app.auth.jwt import create_access_tokens
from app.auth.deps import get_current_user
from app.models.user import User

SQLALCHEMY_TEST_DATABASE = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try: 
        yield session
    finally: 
        session.close()

@pytest.fixture()
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_current_user] = lambda: User(id=1, email="test@example.com", hashed_password="...", created_at=None)
    app.dependency_overrides["get_db"] = override_get_db

    return TestClient(app)