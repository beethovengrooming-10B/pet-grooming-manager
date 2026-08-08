from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db() -> Generator[Session, None, None]:
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def create_client(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/clients",
        json={
            "first_name": "Mario",
            "last_name": "Rossi",
            "phone": "3331234567",
            "email": "mario.rossi@example.com",
            "notes": "Cliente di test",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_client(client: TestClient) -> None:
    created_client = create_client(client)

    assert created_client["id"] == 1
    assert created_client["first_name"] == "Mario"
    assert created_client["phone"] == "3331234567"


def test_list_clients_and_search(client: TestClient) -> None:
    create_client(client)

    response = client.get("/clients?search=Ros")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["last_name"] == "Rossi"


def test_get_client(client: TestClient) -> None:
    created_client = create_client(client)

    response = client.get(f"/clients/{created_client['id']}")

    assert response.status_code == 200
    assert response.json()["email"] == "mario.rossi@example.com"


def test_update_client(client: TestClient) -> None:
    created_client = create_client(client)

    response = client.patch(
        f"/clients/{created_client['id']}",
        json={"phone": "3337654321"},
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "3337654321"


def test_delete_client(client: TestClient) -> None:
    created_client = create_client(client)

    response = client.delete(f"/clients/{created_client['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/clients/{created_client['id']}")

    assert get_response.status_code == 404


def test_returns_404_for_unknown_client(client: TestClient) -> None:
    response = client.get("/clients/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente non trovato."


def test_rejects_invalid_client(client: TestClient) -> None:
    response = client.post(
        "/clients",
        json={
            "first_name": "",
            "last_name": "Rossi",
            "phone": "",
        },
    )

    assert response.status_code == 422