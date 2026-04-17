import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes import router
from app.rag.indexer import index_documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data/chroma", exist_ok=True)
    index_documents()
    yield


app = FastAPI(title="RAG Knowledge Bot", lifespan=lifespan)

app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
