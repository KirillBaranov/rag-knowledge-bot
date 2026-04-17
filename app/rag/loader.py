from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

LOADERS = {
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".pdf": PyPDFLoader,
}

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def load_docs(docs_path: str) -> list[Document]:
    path = Path(docs_path)
    documents = []

    for file in path.rglob("*"):
        loader_cls = LOADERS.get(file.suffix.lower())
        if not loader_cls:
            continue
        try:
            loader = loader_cls(str(file))
            documents.extend(loader.load())
        except Exception as e:
            print(f"Skipping {file}: {e}")

    return splitter.split_documents(documents)
