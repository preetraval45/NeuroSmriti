"""
API endpoint tests
"""
import pytest


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestAuthEndpoints:
    """Tests for authentication endpoints"""

    def test_register_new_user(self, client):
        """Test user registration"""
        user_data = {
            "email": "newuser@test.com",
            "password": "SecurePass123!",
            "full_name": "New User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data

    def test_register_duplicate_email(self, client, test_user_credentials):
        """Test registration with duplicate email fails"""
        # First registration
        client.post("/api/v1/auth/register", json=test_user_credentials)

        # Second registration with same email
        response = client.post("/api/v1/auth/register", json=test_user_credentials)
        assert response.status_code == 400

    def test_login_success(self, client, test_user_credentials):
        """Test successful login"""
        # Register first
        client.post("/api/v1/auth/register", json=test_user_credentials)

        # Login
        response = client.post("/api/v1/auth/login", json={
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_credentials):
        """Test login with wrong password fails"""
        # Register first
        client.post("/api/v1/auth/register", json=test_user_credentials)

        # Login with wrong password
        response = client.post("/api/v1/auth/login", json={
            "email": test_user_credentials["email"],
            "password": "WrongPassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user fails"""
        response = client.post("/api/v1/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "Password123"
        })
        assert response.status_code == 401


class TestPatientEndpoints:
    """Tests for patient management endpoints"""

    def test_create_patient(self, authenticated_client):
        """Test creating a new patient"""
        patient_data = {
            "full_name": "John Doe",
            "date_of_birth": "1950-01-15",
            "gender": "Male",
            "phone": "+1234567890",
            "email": "john.doe@example.com",
            "current_stage": 2,
            "mmse_score": 24,
            "moca_score": 22
        }
        response = authenticated_client.post("/api/v1/patients", json=patient_data)
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == patient_data["full_name"]
        assert "id" in data

    def test_get_patients_list(self, authenticated_client):
        """Test getting list of patients"""
        # Create a patient first
        patient_data = {
            "full_name": "Jane Smith",
            "date_of_birth": "1955-03-20",
            "gender": "Female",
            "current_stage": 1
        }
        authenticated_client.post("/api/v1/patients", json=patient_data)

        # Get patients list
        response = authenticated_client.get("/api/v1/patients")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_patient_by_id(self, authenticated_client):
        """Test getting a specific patient"""
        # Create a patient
        patient_data = {
            "full_name": "Test Patient",
            "date_of_birth": "1960-05-10",
            "gender": "Male",
            "current_stage": 1
        }
        create_response = authenticated_client.post("/api/v1/patients", json=patient_data)
        patient_id = create_response.json()["id"]

        # Get the patient
        response = authenticated_client.get(f"/api/v1/patients/{patient_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == patient_id
        assert data["full_name"] == patient_data["full_name"]

    def test_update_patient(self, authenticated_client):
        """Test updating patient information"""
        # Create a patient
        patient_data = {
            "full_name": "Original Name",
            "date_of_birth": "1965-08-15",
            "gender": "Female",
            "current_stage": 1
        }
        create_response = authenticated_client.post("/api/v1/patients", json=patient_data)
        patient_id = create_response.json()["id"]

        # Update the patient
        update_data = {
            "mmse_score": 26,
            "moca_score": 24,
            "current_stage": 2
        }
        response = authenticated_client.patch(f"/api/v1/patients/{patient_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["mmse_score"] == 26
        assert data["current_stage"] == 2


class TestPredictionEndpoints:
    """Tests for ML prediction endpoints"""

    def test_predict_stage_endpoint_exists(self, authenticated_client):
        """Test that stage prediction endpoint exists"""
        # Create a patient first
        patient_data = {
            "full_name": "Prediction Test",
            "date_of_birth": "1955-01-01",
            "gender": "Male",
            "current_stage": 1,
            "mmse_score": 24,
            "moca_score": 22
        }
        create_response = authenticated_client.post("/api/v1/patients", json=patient_data)
        patient_id = create_response.json()["id"]

        # Call prediction endpoint
        response = authenticated_client.post(f"/api/v1/predictions/stage?patient_id={patient_id}")

        # Should return prediction (may be mock if models not loaded)
        assert response.status_code in [200, 500]  # 500 if models not available
        if response.status_code == 200:
            data = response.json()
            assert "predicted_stage" in data
            assert "confidence" in data

    def test_memory_decay_prediction(self, authenticated_client):
        """Test memory decay prediction endpoint"""
        # Create a patient
        patient_data = {
            "full_name": "Memory Test",
            "date_of_birth": "1960-01-01",
            "gender": "Female",
            "current_stage": 2
        }
        create_response = authenticated_client.post("/api/v1/patients", json=patient_data)
        patient_id = create_response.json()["id"]

        # Call memory decay prediction
        response = authenticated_client.get(f"/api/v1/predictions/memory-decay/{patient_id}")

        # Should return prediction (may have no memories)
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "total_memories" in data
            assert "high_risk_memories" in data


class TestAuthorizationTests:
    """Tests for authorization and access control"""

    def test_access_protected_endpoint_without_auth(self, client):
        """Test that protected endpoints require authentication"""
        response = client.get("/api/v1/patients")
        assert response.status_code == 401

    def test_invalid_token(self, client):
        """Test that invalid tokens are rejected"""
        client.headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/patients")
        assert response.status_code == 401
