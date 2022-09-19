# representar o banco de dados com ajuda de classes
from pydantic import BaseModel, validator
from decimal import Decimal
from datetime import datetime
from dundie.utils.email import check_valid_email
from dundie.database import connect


class InvalidEmailError(Exception):
    # criando uma classe específica para erro de email inválido
    ...


class Person (BaseModel):  # classe para representar pessoa
    # como inicilmenten no json
    pk: str  # usar type annotation para definir tipo do atributo
    name: str
    dept: str
    role: str

    @validator("pk")  # criando uma validação de email.
    # o "v" é o valor recebido
    # o "cls" equivale ao self, para classe
    def validate_email(cls, v):
        if not check_valid_email(v):
            raise InvalidEmailError(
                f"invalid email for {v}"
                )
        return v

    def __str__(self):
        # definindo como a classe será mostrada com o print (protocolo
        # __str__ : printable)
        return f"{self.name} - {self.role}"


class Balance(BaseModel):
    person: Person  # recebe uma instância de Person
    value: Decimal  # usar tipo decimal, para boa precisão

    class Config:  # uma classe dentro de uma classe
        # essa classe especifica como o objeto Person deve ser serializado
        json_encoders = {Person: lambda p: p.name}


class Movement(BaseModel):
    person: Person
    date: datetime
    actor: str
    value: Decimal


# conectando com o db e serializando ou desserialização

db = connect()

for pk, data in db["people"].items():
    #  fazendo a desserialização do banco de dados em json
    p = Person(pk=pk, **data)
    print(p)

print(p)
print(p.json())  # não precisa criar método de serialização. O pydantic já
#  tem um. Como as classes herdam o BaseModel, ele já consegue serializar
# sozinho. Ele também sabe serializar a classe Decimal

balance = Balance(person=p, value=100)
print(balance.json(models_as_dict=False))  # quando usamos encoders
# customizados usar isso
