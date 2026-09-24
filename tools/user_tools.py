from database.database import (
    SessionLocal
)

from database.models import (
    User
)
import os



def get_application_name():

    return {
        "application":
            "FastAPI User Management"
    }

# Tool to List all Users
def list_users():
  db = SessionLocal()
  
  try:
  
      users = (db.query(User).all())
  
      return [{"id": user.id,"name": user.name,"email": user.email}for user in users]
  
  finally:

    db.close()

# Tool to List Single User
def get_user(user_id: int):
    db = SessionLocal()
    try:
        user = (db.query(User).filter(User.id == user_id).first())
    finally:
        db.close()

    
    if not user:

        return {
            "error":
                "User not found"
        }

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


def list_uploaded_files():

    return os.listdir(
        "uploads"
    )
