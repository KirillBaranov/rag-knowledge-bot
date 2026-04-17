from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.config import settings
from app.rag.embeddings import _get_token
from app.rag.indexer import get_vectorstore


def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(d.page_content for d in docs)


def build_chain():
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(
        model=settings.MODEL,
        streaming=True,
        temperature=0,
        base_url=settings.OPENAI_BASE_URL,
        api_key=_get_token(),
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", settings.SYSTEM_PROMPT + "\n\nКонтекст из документов:\n{context}"),
        ("human", "{question}"),
    ])

    return (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


async def ask_stream(question: str) -> AsyncIterator[str]:
    chain = build_chain()
    async for chunk in chain.astream(question):
        yield chunk
