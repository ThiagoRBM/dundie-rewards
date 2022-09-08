import os
from csv import reader

from dundie.database import add_movement, add_person, commit, connect
from dundie.utils.log import get_logger

"""Funcoes principais"""

log = get_logger()


def load(filepath):
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv')) ## doctest, para rodar no terminal:
    python -m doctest -v dundie/core.py
    2
    """
    try:
        csv_data = reader(open(filepath))  # retorna uma lista
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    db = connect()
    people = []
    headers = ["name", "dept", "role", "email"]
    for line in csv_data:
        person_data = dict(zip(headers, [item.strip() for item in line]))
        pk = person_data.pop("email")
        person, created = add_person(db, pk, person_data)
        # breakpoint()

        return_data = person.copy()
        return_data["created"] = created
        return_data["email"] = pk
        people.append(return_data)

    commit(db)
    return people


def read(**query):
    """Reads data from database and filters according to query.
    Receives query in dict format.
    Accepts as query key: 'dept' or 'email'.

    read(email= "joe@doe.com")
    """
    db = connect()
    # breakpoint()
    return_data = []
    for pk, data in db["people"].items():  # lê chave e valor em "people"

        dept = query.get("dept")
        if dept and dept != data["dept"]:  # caso o dept da pessoa não seja o
            # que foi pedido, passa para a próxima iteração
            continue

        # query assignment, funciona a partir do python 3.8 e substitui linhas
        # acima. ':=' chama WALRUS ou Assignment Expression
        if (email := query.get("email")) and email != pk:
            continue
        # breakpoint()
        return_data.append(
            {
                "email": pk,  # o email está como key
                "balance": db["balance"][pk],
                "last_movement": db["movement"][pk][-1]["date"],
                **data,
            }
        )
    return return_data


def add(value, **query):
    """Add value to each record on query"""
    people = read(**query)
    if not people:
        raise RuntimeError("Not Found")

    db = connect()
    user = os.getenv("USER")  # por enquanto pega o user do ENV do sistema
    # caso o argumento seja deixado em branco
    for person in people:
        add_movement(db, person["email"], value, user)
    commit(db)
