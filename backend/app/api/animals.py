from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.animal import Animal
from app.models.client import Client
from app.schemas.animal import AnimalCreate, AnimalResponse, AnimalUpdate


router = APIRouter(tags=["animals"])


@router.get(
    "/clients/{client_id}/animals",
    response_model=list[AnimalResponse],
)
def list_animals(
    client_id: int,
    db: Session = Depends(get_db),
):
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    statement = (
        select(Animal)
        .where(Animal.client_id == client_id)
        .order_by(Animal.id)
    )

    return db.scalars(statement).all()


@router.post(
    "/clients/{client_id}/animals",
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_animal(
    client_id: int,
    payload: AnimalCreate,
    db: Session = Depends(get_db),
):
    client = db.get(Client, client_id)

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    animal = Animal(
        client_id=client_id,
        **payload.model_dump(),
    )

    db.add(animal)
    db.commit()
    db.refresh(animal)

    return animal


@router.get(
    "/animals/{animal_id}",
    response_model=AnimalResponse,
)
def get_animal(
    animal_id: int,
    db: Session = Depends(get_db),
):
    animal = db.get(Animal, animal_id)

    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )

    return animal


@router.put(
    "/animals/{animal_id}",
    response_model=AnimalResponse,
)
def update_animal(
    animal_id: int,
    payload: AnimalUpdate,
    db: Session = Depends(get_db),
):
    animal = db.get(Animal, animal_id)

    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(animal, field, value)

    db.commit()
    db.refresh(animal)

    return animal


@router.delete(
    "/animals/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_animal(
    animal_id: int,
    db: Session = Depends(get_db),
):
    animal = db.get(Animal, animal_id)

    if animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )

    db.delete(animal)
    db.commit()