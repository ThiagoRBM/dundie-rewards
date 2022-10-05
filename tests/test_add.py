import pytest

from dundie.core import add
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from sqlmodel import select


@pytest.mark.unit
def test_add_movement():
    with get_session() as session:
        data = {
            "role": "salesman",
            "dept": "sales",
            "name": "Joe Doe",
            "email": "joe@doe.com",
        }
        joe, created = add_person(session, Person(**data))
        assert created is True

        data = {
            "role": "manager",
            "dept": "sales",
            "name": "Jim Doe",
            "email": "jim@doe.com",
        }
        jim, created = add_person(session, Person(**data))
        assert created is True

        session.commit()

        user = session.exec(select(Person.id)
                            .where(Person.email == "jim@doe.com")
                            )
        user = [i for i in user][0]

        pass_ = session.exec(
            select(User).
            where(User.person_id == user)
        )
        pass_ = [i for i in pass_][0].password

        add(-30, email="joe@doe.com", login="jim@doe.com", senha=pass_)
        add(90, dept="sales", login="jim@doe.com", senha=pass_)
        session.refresh(joe)
        session.refresh(jim)

        assert joe.balance[0].value == 560
        assert jim.balance[0].value == 590
