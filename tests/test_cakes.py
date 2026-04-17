from fastapi.testclient import TestClient

from app.main import app  # Import your FastAPI app

# Create test client
client = TestClient(app)

# API Key for testing
HEADERS = {"API-Key": "12345"}


# ===== GET /cakes Tests =====
def test_list_cakes_with_valid_key():
    """Test listing all cakes with valid API key"""
    response = client.get("/cakes", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least 1 cake exists


def test_list_cakes_without_key():
    """Test listing cakes without API key - should fail"""
    response = client.get("/cakes")
    assert response.status_code == 401


def test_list_cakes_with_wrong_key():
    """Test listing cakes with wrong API key - should fail"""
    response = client.get("/cakes", headers={"API-Key": "wrong-key"})
    assert response.status_code == 401


# ===== GET /cakes/{cake_id} Tests =====
def test_get_cake_by_id_success():
    """Test getting a specific cake by ID"""
    response = client.get("/cakes/1", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_cake_by_id_not_found():
    """Test getting non-existent cake"""
    response = client.get("/cakes/999", headers=HEADERS)
    assert response.status_code == 404


# ===== POST /cakes Tests =====
def test_add_cake_success():
    """Test adding a new cake"""
    new_cake = {
        "id": 100,
        "name": "Cheesecake",
        "comment": "Creamy and delicious",
        "imageUrl": "https://www.adamchan.com/cheesecake.jpg",
        "yumFactor": 5,
    }
    response = client.post("/cakes", json=new_cake, headers=HEADERS)
    assert response.status_code == 201
    assert response.json()["name"] == "Cheesecake"


def test_add_cake_duplicate_id():
    """Test adding cake with existing ID - should fail"""
    duplicate_cake = {
        "id": 1,  # This ID already exists
        "name": "Duplicate",
        "comment": "Should fail",
        "imageUrl": "https://www.adamchan.com/dup.jpg",
        "yumFactor": 3,
    }
    response = client.post("/cakes", json=duplicate_cake, headers=HEADERS)
    assert response.status_code == 400


def test_add_cake_invalid_yum_factor():
    """Test adding cake with invalid yum factor"""
    invalid_cake = {
        "id": 200,
        "name": "Test",
        "comment": "Test",
        "imageUrl": "https://www.adamchan.com/test.jpg",
        "yumFactor": 10,  # Must be 1-5
    }
    response = client.post("/cakes", json=invalid_cake, headers=HEADERS)
    assert response.status_code == 422


def test_add_cake_name_too_long():
    """Test adding cake with name exceeding 30 characters"""
    invalid_cake = {
        "id": 201,
        "name": "A" * 31,  # Max is 30
        "comment": "Test",
        "imageUrl": "https://www.adamchan.com/test.jpg",
        "yumFactor": 3,
    }
    response = client.post("/cakes", json=invalid_cake, headers=HEADERS)
    assert response.status_code == 422


# ===== DELETE /cakes/{cake_id} Tests =====
def test_delete_cake_success():
    """Test deleting a cake"""
    # First add a cake to delete
    new_cake = {
        "id": 300,
        "name": "Temp Cake",
        "comment": "Will be deleted",
        "imageUrl": "https://www.adamchan.com/temp.jpg",
        "yumFactor": 2,
    }
    client.post("/cakes", json=new_cake, headers=HEADERS)

    # Now delete it
    response = client.delete("/cakes/300", headers=HEADERS)
    assert response.status_code == 204


def test_delete_cake_not_found():
    """Test deleting non-existent cake"""
    response = client.delete("/cakes/999", headers=HEADERS)
    assert response.status_code == 404
