from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

recetas_fav = Table(
    "recetas_fav",
    db.metadata,
    Column("id", db.Integer, primary_key=True),
    Column("usuario_id", ForeignKey("user.id"), nullable=False),
    Column("receta_id", ForeignKey("recetas.id"), nullable=False)
)

ingredientes_receta = Table(
    "ingredientes_recetas",
    db.metadata,
    Column("id", db.Integer, primary_key=True),
    Column("receta_id", ForeignKey("recetas.id"), nullable=False),
    Column("ingredientes_id", ForeignKey("ingredientes.id"), nullable=False)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(unique=False, nullable=False)
    favorito: Mapped[List["Recetas"]] = relationship(
        secondary=recetas_fav,
        back_populates="favoritos_de"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "favorito": [f.name for f in self.favorito]
        }


class Recetas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    ingredientes: Mapped[List["Ingredientes"]] = relationship(
        secondary=ingredientes_receta,
        back_populates="ingrediente_de"
    )
    favoritos_de: Mapped[List["User"]] = relationship(
        secondary=recetas_fav,
        back_populates="favorito"
    )
    #Obviar esta parte del codigo, esta modificada para la explicación
    def __repr__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredientes": [i.serialize() for i in self.ingredientes]
        }


class Ingredientes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    ingrediente_de: Mapped[List["Recetas"]] = relationship(
        secondary=ingredientes_receta,
        back_populates="ingredientes"
    )

    #Obviar esta parte del codigo, esta modificada para la explicación
    def __repr__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "tipo": self.tipo
        }
