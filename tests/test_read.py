import pytest

from dundie.core import read
from dundie.database import get_session
from dundie.utils.db import add_person
from sqlmodel import select
from dundie import models


@pytest.mark.unit
def test_read_with_query():
    session = get_session()

    data = {
        "role": "salesman",
        "dept": "sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    _, created = add_person(session, models.Person(**data))
    assert created is True

    data = {
        "role": "manager",
        "dept": "sales",
        "name": "Jim Doe",
        "email": "jim@doe.com",
    }
    _, created = add_person(session, models.Person(**data))
    assert created is True

    session.commit()

    user = session.exec(
        select(models.Person.id)
        .where(models.Person.email == "jim@doe.com")
        )
    user = [i for i in user][0]

    pass_ = session.exec(
            select(models.User).
            where(models.User.person_id == user)
        )
    pass_ = [i for i in pass_][0].password

    response = read(dept="sales", login="jim@doe.com", senha=pass_)
    assert len(response) == 2
    assert response[1]["name"] == "Jim Doe"

    response = read(email="joe@doe.com", login="jim@doe.com", senha=pass_)
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"
