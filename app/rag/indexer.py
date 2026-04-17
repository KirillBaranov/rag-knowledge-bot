from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.config import settings
from app.rag.loader import load_docs

_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, base_url=settings.OPENAI_BASE_URL, api_key=settings.OPENAI_API_KEY)
        _vectorstore = Chroma(
            persist_directory=settings.CHROMA_PATH,
            embedding_function=embeddings,
        )
    return _vectorstore


def index_documents():
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    docs = load_docs(settings.DOCS_PATH)
    if not docs:
        print("No documents found to index.")
        return

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PATH,
    )
    global _vectorstore
    _vectorstore = vectorstore
    print(f"Indexed {len(docs)} chunks.")
