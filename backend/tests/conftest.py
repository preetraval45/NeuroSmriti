"""
Pytest configuration and fixtures for backend tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Test client with database override"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_credentials():
    """Test user credentials"""
    return {
        "email": "test@neurosmriti.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }


@pytest.fixture
def authenticated_client(client, test_user_credentials):
    """Client with authenticated user"""
    # Register user
    response = client.post("/api/v1/auth/register", json=test_user_credentials)
    assert response.status_code == 201

    # Login
    login_response = client.post("/api/v1/auth/login", json={
        "email": test_user_credentials["email"],
        "password": test_user_credentials["password"]
    })
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Add authorization header
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
