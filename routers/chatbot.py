from fastapi import APIRouter
from pydantic import BaseModel
from services.assistant_service import ask_ai

router = APIRouter(tags=["Chatbot"], prefix="/chatbot")

class ChatRequest(BaseModel):
    prompt: str


@router.post("/chat")
async def chat(
    request: ChatRequest
):

    answer = ask_ai(request.prompt, model_name="gpt-4o")
    return {"answer": answer}
