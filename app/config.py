from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = "kblabs"
    OPENAI_BASE_URL: str = "https://api.kblabs.ru/llm/v1"
    KBLABS_GATEWAY_URL: str = "https://api.kblabs.ru"
    KBLABS_CLIENT_ID: str
    KBLABS_CLIENT_SECRET: str
    MODEL: str = "medium"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHROMA_PATH: str = "data/chroma"
    DOCS_PATH: str = "docs"
    SYSTEM_PROMPT: str = (
        "Ты помощник компании. Отвечай только на основе предоставленных документов. "
        "Если информации нет в документах — скажи об этом прямо. "
        "Отвечай на том же языке, на котором задан вопрос."
    )

    class Config:
        env_file = ".env"


settings = Settings()
