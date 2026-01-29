import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.application.api.main import create_app  # noqa: E402
from app.application.api.messages.router import get_mediator  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    get_mediator.cache_clear()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
