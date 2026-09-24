from fastapi import APIRouter
from pydantic import BaseModel

from services.assistant_service import (
    ask_ai
)


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)

class AssistantRequest(BaseModel):
    question: str
    model: str = "OpenAI"

@router.post("")
async def assistant(request: AssistantRequest):

    answer = ask_ai(
        request.question,
        request.model
    )

    return {
        "response": answer
    }
