from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    Depends,
)

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import Optional

# Import all Dependencies
from dependencies.common import (
    ApplicationSettings, get_settings,
    PaginationParams, get_pagination
)

router = APIRouter(tags=["Clients"])

clients = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com", "age": 40, "phone": "+971500000001"},
    {"id": 2, "name": "Mary Smith", "email": "mary.smith@example.com", "age": 35, "phone": None},
    {"id": 3, "name": "David Lee", "email": "david.lee@example.com", "age": 29, "phone": "+971500000003"},
]

class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(gt=18, lt=80)
    phone: Optional[str] = Field(None, description="Phone number is optional")

class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    phone: Optional[str] = None


# Endpoint to create a new user
@router.post("/clients",response_model=ClientResponse)
def create_user(user: ClientCreate):

    new_user = {
        "id": max((item["id"] for item in clients), default=0) + 1,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "phone": user.phone,
    }
    clients.append(new_user)
    return new_user

# Endpoint to get user by ID
@router.get("/clients/{client_id}", response_model=ClientResponse)
def get_client(client_id: int= Path(ge=1)):
    for client in clients:
        if client["id"] == client_id:
            return client

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Client not found",
    )

# Endpoints to fetch all users
@router.get("/clients", response_model=list[ClientResponse])
def get_clients(
    search: Optional[str] = Query(default=None, min_length=1),
    pagination: PaginationParams = Depends(get_pagination),
):

    start = (pagination.page - 1) * pagination.limit
    end = start + pagination.limit

    filtered_clients = clients

    if search:
        search_text = search.lower()
        filtered_clients = [
            client
            for client in clients
            if search_text in client["name"].lower()
            or search_text in client["email"].lower()
        ]

    return filtered_clients[start:end]