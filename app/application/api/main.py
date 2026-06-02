import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.api.messages import router as messages_router


def _allowed_origins() -> list[str]:
    raw_origins = os.getenv("CHAT_ALLOWED_ORIGINS", "*")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app() -> FastAPI:
    app = FastAPI(
        title='Embeddable FastAPI Chat',
        docs_url='/api/docs',
        description='DDD chat API with optional Kafka event publishing.',
        debug=os.getenv("APP_DEBUG", "false").lower() in {"1", "true", "yes", "on"},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins(),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(messages_router)
    return app
