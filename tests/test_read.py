import pytest

from dundie.core import load, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE

@pytest.mark.unit
def test_read_with_query():
    session = get_session()

    data = {
        "role": "Salesman",
        "dept": "Sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    data = {
        "role": "Manager",
        "dept": "Management",
        "name": "Jim Doe",
        "email": "jim@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    session.commit()

    response = read()
    assert len(response) == 2

    response = read(dept="Management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Doe"

    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"

# @pytest.mark.unit
# def test_read_with_query():
#     db = connect()  # conecta no DB
#     # breakpoint()
#     pk = "alberto@dunder.com"
#     data = {"role": "salesman", "dept": "management", "name": "alberto"}
#     _, created = add_person(db, pk, data)
#     # breakpoint()
#     assert created is True

#     pk = "jim2@due.com"
#     data = {"role": "manager", "dept": "accounting", "name": "Jim Due"}
#     db = connect()  # conecta no DB
#     _, created = add_person(db, pk, data)
#     assert created is True
#     commit(db)
#     # breakpoint()  ## aqui
#     response = read()
#     # breakpoint()
#     # assert len(response) == 2  # se não passar nada, recebe os dois usuários

#     response = read(dept="accounting")
#     assert len(response) == 1
#     assert response[0]["name"] == "Jim Due"
#     # funcao read gera uma lista, por isso o indice 0
#     response = read(email="alberto@dunder.com")
#     assert len(response) == 1
#     assert response[0]["name"] == "alberto"
#     # para rodar apenas esse teste e não todos (com o make test):
#     # pytest -m "unit" -k read
