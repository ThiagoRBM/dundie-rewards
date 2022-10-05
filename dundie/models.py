# representar o banco de dados com ajuda de classes
from datetime import datetime
from typing import Optional

from pydantic import condecimal, validator
from sqlmodel import Field, Relationship, SQLModel

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


class InvalidEmailError(Exception):
    # criando uma classe específica para erro de email inválido
    ...


class Person(SQLModel, table=True):  # classe para representar pessoa
    #  criar índices é interessante quando serão usados muito para busca
    #  se não for o caso, é bom não usar porque vai demorar para atualizar
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(nullable=False, index=True)
    name: str = Field(nullable=False)
    dept: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)
    currency: str = Field(default="USD")

    balance: "Balance" = Relationship(back_populates="person")
    movement: "Movement" = Relationship(back_populates="person")
    user: "User" = Relationship(back_populates="person")

    @validator("email")  # criando uma validação de email.
    # o "v" é o valor recebido
    # o "cls" equivale ao self, para classe
    def validate_email(cls, v):
        if not check_valid_email(v):
            raise InvalidEmailError(f"invalid email for {v}")
        return v

    def __str__(self):
        # definindo como a classe será mostrada com o print (protocolo
        # __str__ : printable)
        return f"{self.name} - {self.role}"


class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    value: condecimal(decimal_places=3) = Field(default=0)
    # SQLite não entende decima, mas essa funcao transforma o valor

    person: Person = Relationship(back_populates="balance")
    #  recebe uma instância de Person
    #  vai ser um campo virtual, nao estará no arquivo .db
    #  é costume dar um espaço para indicar os virtuais

    class Config:  # uma classe dentro de uma classe
        # essa classe especifica como o objeto Person deve ser serializado
        json_encoders = {Person: lambda p: p.pk}


class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    date: datetime = Field(default_factory=lambda: datetime.now())
    #  SQLalchemy recebe o objeto de tempo sem formatação
    actor: str = Field(nullable=False, index=True)
    value: condecimal(decimal_places=3) = Field(default=0)

    person: Person = Relationship(back_populates="movement")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    password: str = Field(default_factory=generate_simple_password)

    person: Person = Relationship(back_populates="user")

    class Config:
        json_encoders = {Person: lambda p: p.pk}
