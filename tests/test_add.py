import pytest

from dundie.database import connect, commit, add_person
from dundie.core import add


@pytest.mark.unit
def test_add_movement():
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

    add(-30, email="joe@doe.com")
    add(90, dept="management")

    db = connect()

    assert db["balance"]["joe@doe.com"] == 470
    assert db["balance"]["jim@due.com"] == 190
