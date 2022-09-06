from csv import reader

from dundie.database import add_person, commit, connect
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
        # return_data = person.copy()
        person["created"] = created
        person["email"] = pk
        people.append(person)
    commit(db)
    return people
