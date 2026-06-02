# FastAPI DDD Kafka Chat

Embeddable chat service for websites and internal products. The project combines a FastAPI backend, DDD-style domain layer, optional Kafka event publishing, and a small React interface that can be used as a ready demo or adapted into a widget.

## What It Includes

- REST API for creating chats, listing chats, opening a chat, and sending messages.
- Domain entities, value objects, commands, events, and a mediator layer.
- In-memory repository for quick local demos and tests.
- Optional Kafka publisher for chat and message events.
- Vite + React frontend with chat selection, message history, and message composer.
- Docker Compose setup for backend and frontend.

## API

- `POST /api/chats` - create a chat.
- `GET /api/chats` - list chats.
- `GET /api/chats/{chat_oid}` - get chat details with messages.
- `POST /api/chats/{chat_oid}/messages` - send a message.
- `GET /api/docs` - OpenAPI documentation.

## Run With Docker

```bash
cp .env.example .env
make app
```

Open the frontend at [http://localhost:5173](http://localhost:5173).

The backend is available at [http://localhost:8000](http://localhost:8000).

## Local Development

Backend:

```bash
poetry install
poetry run uvicorn --factory app.application.api.main:create_app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Configuration

`KAFKA_ENABLED=false` keeps the demo fully local. Set `KAFKA_ENABLED=true` and provide `KAFKA_BOOTSTRAP_SERVERS` when event publishing is needed.

`CHAT_ALLOWED_ORIGINS=*` can be narrowed to specific website origins for production deployments.

## Tests

```bash
poetry install
poetry run pytest
```
