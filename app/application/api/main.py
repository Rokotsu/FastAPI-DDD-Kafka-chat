from fastapi import FastAPI

from app.application.api.messages import router as messages_router

def create_app():
    app = FastAPI(
        title='Simple Kafka Chat',
        docs_url='/api/docs',
        description='Simple Kafka + ddd.',
        debug=True,
    )

    app.include_router(messages_router)
    return app
