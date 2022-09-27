import os
from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person
from dundie.settings import DATEFMT
from dundie.utils.db import add_movement, add_person
from dundie.utils.log import get_logger

"""Funcoes principais"""

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


def load(filepath: str) -> ResultDict:
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

    people = []
    headers = ["name", "dept", "role", "email"]

    with get_session() as session:
        for line in csv_data:
            person_data = dict(zip(headers, [item.strip() for item in line]))
            instance = Person(**person_data)
            person, created = add_person(session, instance)

            return_data = person.dict(exclude={"id"})
            return_data["created"] = created
            people.append(return_data)

        session.commit()
    return people


def read(**query: Query) -> ResultDict:
    """Reads data from database and filters according to query.
    Receives query in dict format.
    Accepts as query key: 'dept' or 'email'.

    read(email= "joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    return_data = []

    query_statements = []
    if "dept" in query:
        query_statements.append(Person.dept == query["dept"])
    if "email" in query:
        query_statements.append(Person.email == query["email"])
    sql = select(Person)  # SELECT FROM PERSON
    if query_statements:  # caso haja query, são passados em list pro where
        sql = sql.where(*query_statements)  # WHERE

    with get_session() as session:
        results = session.exec(sql)
        for person in results:
            return_data.append(
                {
                    "email": person.email,
                    "balance": person.balance[0].value,
                    "last_movement": person.movement[-1].date.strftime(
                        DATEFMT
                    ),
                    **person.dict(exclude={"id"}),
                }
            )
    return return_data


def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    with get_session() as session:
        user = os.getenv("USER")  # por enquanto pega o user do ENV do sistema
        # caso o argumento seja deixado em branco
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()
            add_movement(session, instance, value, user)

        session.commit()
