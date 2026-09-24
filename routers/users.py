import asyncio

from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,Depends,Header
)

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import Optional,List

# Import all Dependencies
from dependencies.common import (
    ApplicationSettings, get_settings,
    PaginationParams, get_pagination,get_db
)

from sqlalchemy.orm import Session
from database.models import User
from security.auth import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(tags=["Users"], prefix="/users")




class LoginRequest(
    BaseModel
):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(gt=18, lt=80)
    phone: Optional[str] = Field(None, description="Phone number is optional")
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    phone: Optional[str] = None


@router.get("/async-demo")
async def async_demo():

    await asyncio.sleep(5)

    return {
        "message":
            "Completed"
    }


#End Point to Login
@router.post("/login")
def login(request: LoginRequest,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(user.email)

    return {
        "access_token":access_token,"token_type":"bearer"}


#End Point for Profile Access
@router.get("/profile")
def profile(
    authorization: str
        | None = Header(None)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    return {
        "message":
            "Protected Route"
    }



#End Point for Application Settings
@router.get("/info")
def get_application_info(
    settings: ApplicationSettings = Depends(get_settings),
):
    return settings


# Endpoint to create a new user
@router.post("",response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        phone=user.phone,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Endpoint to get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


# Endpoints to fetch all users
@router.get("", response_model=list[UserResponse])
def get_users(
    search: Optional[str] = Query(default=None, min_length=1),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db)
):

    start = (pagination.page - 1) * pagination.limit
    end = start + pagination.limit

    filtered_users = db.query(User).all()

    if search:
        search_text = search.lower()
        filtered_users = [
            user
            for user in filtered_users
            if search_text in user.name.lower()
            or search_text in user.email.lower()
        ]

    return filtered_users[start:end]

