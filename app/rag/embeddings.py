import time
import httpx
from langchain_core.embeddings import Embeddings

from app.config import settings

_token: str | None = None
_token_expires_at: float = 0


def _get_token() -> str:
    global _token, _token_expires_at
    if _token and time.time() < _token_expires_at - 30:
        return _token
    resp = httpx.post(
        f"{settings.KBLABS_GATEWAY_URL}/auth/token",
        json={"clientId": settings.KBLABS_CLIENT_ID, "clientSecret": settings.KBLABS_CLIENT_SECRET},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    _token = data["accessToken"]
    _token_expires_at = time.time() + data["expiresIn"]
    return _token


class KBLabsEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        resp = httpx.post(
            f"{settings.KBLABS_GATEWAY_URL}/platform/v1/embeddings/embed",
            headers={"Authorization": f"Bearer {_get_token()}"},
            json={"args": [text]},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["result"]
