import pytest

from dundie.database import connect, commit, add_person
from dundie.core import read


@pytest.mark.unit
def test_read_with_query():
    db = connect()  # conecta no DB

    pk = "joe@doe.com"
    data = {"role": "salesman", "dept": "sales", "name": "Joe Doe"}
    _, created = add_person(db, pk, data)
    assert created is True

    pk = "jim@due.com"
    data = {"role": "manager", "dept": "management", "name": "Jim Due"}
    db = connect()  # conecta no DB
    _, created = add_person(db, pk, data)
    print(_)
    assert created is True
    commit(db)

    response = read()
    #  breakpoint()
    assert len(response) == 2  # se não passar nada, recebe os dois usuários

    response = read(dept="management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Due"
    # funcao read gera uma lista, por isso o indice 0
    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"
    # para rodar apenas esse teste e não todos (com o make test):
    # pytest -m "unit" -k read
