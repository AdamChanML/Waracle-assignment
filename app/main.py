"""
Cake Database implemented in FastAPI
Provides endpoints to maintain a cake catalog with CRUD operations.
"""

from typing import List

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Waracle Cake API (Adam Chan test assignment)",
    description="API for managing a cake catalog (Protected with API Key Authentication)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# API Key configuration
API_KEY = "12345"
api_key_header = APIKeyHeader(name="API-Key")


# Test if the API key is valid
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


# Set up the Cake model using Pydantic
class Cake(BaseModel):
    id: int = Field(..., description="Unique identifier for the cake")
    name: str = Field(..., max_length=30, description="Name of the cake")
    comment: str = Field(..., max_length=200, description="Comment about the cake")
    imageUrl: str = Field(..., description="URL for the cake image")
    yumFactor: int = Field(..., ge=1, le=5, description="Yum factor rating (1-5)")

    # Validators to ensure name and comment are not empty or just whitespace
    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @field_validator("comment")
    @classmethod
    def comment_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Comment cannot be empty")
        return v.strip()


# Set up an In-memory database for cakes
cakes_db: List[Cake] = [
    Cake(
        id=1,
        name="Chocolate Cake",
        comment="Rich chocolate cake",
        imageUrl="https://www.adamchan.com/images/chocolate-cake.jpg",
        yumFactor=5,
    ),
    Cake(
        id=2,
        name="Carrot Cake",
        comment="Light and fluffy carrot cake",
        imageUrl="https://www.adamchan.com/images/vanilla-cake.jpg",
        yumFactor=4,
    ),
    Cake(
        id=3,
        name="Tiramisu Cake",
        comment="Classic Tiramisu cake",
        imageUrl="https://www.adamchan.com/images/tiramisu-cake.jpg",
        yumFactor=5,
    ),
]


# GET all cakes
@app.get("/cakes", response_model=List[Cake], tags=["cakes"])
async def list_cakes(api_key: str = Security(verify_api_key)) -> List[Cake]:
    """
    Get all cakes in the catalog.

    Returns a list of all available cakes.
    """
    return cakes_db


# POST a new cake
@app.post("/cakes", response_model=Cake, status_code=201, tags=["cakes"])
async def add_cake(cake: Cake, api_key: str = Security(verify_api_key)) -> Cake:
    """
    Add a new cake to the catalog.

    The cake ID must be unique. If a cake with the same ID already exists,
    an error will be returned.
    """
    for existing_cake in cakes_db:
        if existing_cake.id == cake.id:
            raise HTTPException(
                status_code=400, detail=f"Cake with ID {cake.id} already exists"
            )

    cakes_db.append(cake)
    return cake


# DELETE a cake by ID
@app.delete("/cakes/{cake_id}", status_code=204, tags=["cakes"])
async def delete_cake(cake_id: int, api_key: str = Security(verify_api_key)):
    """
    Delete a cake from the catalog by its ID.

    Returns 204 No Content on success.
    Returns 404 if the cake is not found.
    """
    for i, cake in enumerate(cakes_db):
        if cake.id == cake_id:
            cakes_db.pop(i)
            return None

    raise HTTPException(status_code=404, detail=f"Cake with ID {cake_id} not found")


# GET a specific cake by cake_id
@app.get("/cakes/{cake_id}", response_model=Cake, tags=["cakes"])
async def get_cake(cake_id: int, api_key: str = Security(verify_api_key)) -> Cake:
    """
    Get a specific cake by its ID.

    Returns the cake if found.
    Returns 404 if the cake is not found.
    """
    for cake in cakes_db:
        if cake.id == cake_id:
            return cake

    raise HTTPException(status_code=404, detail=f"Cake with ID {cake_id} not found")


# if __name__ == "__main__":

#     uvicorn.run(app, host="0.0.0.0", port=8000)
