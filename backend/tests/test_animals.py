from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
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


@event.listens_for(test_engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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
        },
    )

    assert response.status_code == 201
    return response.json()


def animal_payload() -> dict[str, object]:
    return {
        "name": "Fido",
        "species": "cane",
        "breed": "Barboncino",
        "size": "media",
        "coat_type": "riccio_doppio_strato",
        "age": 5,
        "notes": "Test animale",
    }


def create_animal(client: TestClient, client_id: int) -> dict[str, object]:
    response = client.post(
        f"/clients/{client_id}/animals",
        json=animal_payload(),
    )

    assert response.status_code == 201
    return response.json()


def test_create_animal(client: TestClient) -> None:
    created_client = create_client(client)

    response = client.post(
        f"/clients/{created_client['id']}/animals",
        json=animal_payload(),
    )

    assert response.status_code == 201
    created_animal = response.json()

    assert created_animal["id"] == 1
    assert created_animal["client_id"] == created_client["id"]
    assert created_animal["name"] == "Fido"
    assert created_animal["species"] == "cane"
    assert created_animal["size"] == "media"
    assert created_animal["coat_type"] == "riccio_doppio_strato"


def test_list_animals_for_client(client: TestClient) -> None:
    created_client = create_client(client)
    create_animal(client, created_client["id"])

    response = client.get(f"/clients/{created_client['id']}/animals")

    assert response.status_code == 200
    animals = response.json()
    assert len(animals) == 1
    assert animals[0]["name"] == "Fido"


def test_get_animal(client: TestClient) -> None:
    created_client = create_client(client)
    created_animal = create_animal(client, created_client["id"])

    response = client.get(f"/animals/{created_animal['id']}")

    assert response.status_code == 200
    assert response.json()["breed"] == "Barboncino"


def test_update_animal(client: TestClient) -> None:
    created_client = create_client(client)
    created_animal = create_animal(client, created_client["id"])

    response = client.put(
        f"/animals/{created_animal['id']}",
        json={"name": "Fido Aggiornato", "age": 6},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Fido Aggiornato"
    assert response.json()["age"] == 6


def test_delete_animal(client: TestClient) -> None:
    created_client = create_client(client)
    created_animal = create_animal(client, created_client["id"])

    response = client.delete(f"/animals/{created_animal['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/animals/{created_animal['id']}")
    assert get_response.status_code == 404


def test_returns_404_for_unknown_client_when_listing_animals(
    client: TestClient,
) -> None:
    response = client.get("/clients/999/animals")

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_returns_404_for_unknown_animal(client: TestClient) -> None:
    response = client.get("/animals/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Animal not found"


def test_rejects_invalid_animal(client: TestClient) -> None:
    created_client = create_client(client)

    response = client.post(
        f"/clients/{created_client['id']}/animals",
        json={
            "name": "",
            "species": "cane",
            "age": -1,
        },
    )

    assert response.status_code == 422


def test_cascades_animals_when_client_is_deleted(client: TestClient) -> None:
    created_client = create_client(client)
    created_animal = create_animal(client, created_client["id"])

    delete_response = client.delete(f"/clients/{created_client['id']}")
    assert delete_response.status_code == 204

    animal_response = client.get(f"/animals/{created_animal['id']}")
    assert animal_response.status_code == 404
