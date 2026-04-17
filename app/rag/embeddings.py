import httpx
from langchain_core.embeddings import Embeddings

from app.config import settings


class KBLabsEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        url = settings.OPENAI_BASE_URL.rstrip("/").replace("/v1", "") + "/platform/v1/embeddings/embed"
        resp = httpx.post(
            url,
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json={"args": [text]},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()[0]
