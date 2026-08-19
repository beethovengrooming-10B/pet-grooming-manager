import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Species(str, enum.Enum):
    DOG = "cane"
    CAT = "gatto"


class Size(str, enum.Enum):
    SMALL = "piccola"
    MEDIUM = "media"
    LARGE = "grande"
    GIANT = "gigante"


class CoatType(str, enum.Enum):
    SHORT = "corto"
    MEDIUM = "medio"
    LONG = "lungo"
    CURLY_DOUBLE = "riccio_doppio_strato"


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    species: Mapped[Species] = mapped_column(
        SAEnum(
            Species,
            name="species_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )

    breed: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    size: Mapped[Size | None] = mapped_column(
        SAEnum(
            Size,
            name="size_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=True,
    )

    coat_type: Mapped[CoatType | None] = mapped_column(
        SAEnum(
            CoatType,
            name="coat_type_enum",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=True,
    )

    age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    client: Mapped["Client"] = relationship(
        back_populates="animals",
        passive_deletes=True,
    )
