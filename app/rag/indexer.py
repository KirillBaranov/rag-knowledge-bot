from langchain_chroma import Chroma

from app.config import settings
from app.rag.embeddings import KBLabsEmbeddings
from app.rag.loader import load_docs

_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=settings.CHROMA_PATH,
            embedding_function=KBLabsEmbeddings(),
        )
    return _vectorstore


def index_documents():
    embeddings = KBLabsEmbeddings()
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
