from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.chain import ask_stream

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask(body: QuestionRequest):
    async def generate():
        async for chunk in ask_stream(body.question):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")


@router.get("/health")
async def health():
    return {"status": "ok"}
