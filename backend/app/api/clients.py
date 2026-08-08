from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])

DbSession = Annotated[Session, Depends(get_db)]


def get_client_or_404(client_id: int, db: Session) -> Client:
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente non trovato.",
        )

    return client


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_data: ClientCreate, db: DbSession) -> Client:
    client = Client(**client_data.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.get("", response_model=list[ClientResponse])
def list_clients(
    db: DbSession,
    search: str | None = Query(default=None, min_length=1, max_length=100),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
) -> list[Client]:
    statement = select(Client).order_by(Client.last_name, Client.first_name)

    if search is not None:
        term = f"%{search}%"
        statement = statement.where(
            or_(
                Client.first_name.ilike(term),
                Client.last_name.ilike(term),
                Client.phone.ilike(term),
            )
        )

    return list(db.scalars(statement.offset(skip).limit(limit)).all())


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: DbSession) -> Client:
    return get_client_or_404(client_id, db)


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: DbSession,
) -> Client:
    client = get_client_or_404(client_id, db)

    for field_name, value in client_data.model_dump(exclude_unset=True).items():
        setattr(client, field_name, value)

    db.commit()
    db.refresh(client)

    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: DbSession) -> Response:
    client = get_client_or_404(client_id, db)

    db.delete(client)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)