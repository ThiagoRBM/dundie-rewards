import pytest

from dundie.database import check_user_password
from dundie import models
from dundie.database import get_session
from dundie.utils.db import add_person
from sqlmodel import select


@pytest.mark.unit
def test_user_negative_exists():
    """Testa se será retornado erro caso um usuário não existente
    seja usado para o login."""
    with get_session() as session:
        data = {
            "name": "Joe Donde",
            "role": "Salesman",
            "dept": "Sales",
            "email": "joe@donde.com",
        }
        joe, created = add_person(session, models.Person(**data))
        assert created is True

        session.commit()

        log = check_user_password("not@dunder.com", "8iINKxaD")

        assert log == 0


@pytest.mark.unit
def test_wrong_password():
    """Testa se será retornado erro caso uma senha incorreta seja usada"""
    with get_session() as session:
        data = {
            "name": "Joe Donde",
            "role": "Salesman",
            "dept": "Sales",
            "email": "joe@donde.com",
        }
        joe, created = add_person(session, models.Person(**data))
        assert created is True

        session.commit()

        log = check_user_password("joe@doe.com", "8iINKx")

        assert log == 0


@pytest.mark.unit
def test_positive_login():
    """Testa se o login é feito com sucesso caso usuário
    e senha sejam passados corretamente e role é retornado corretamente"""

    with get_session() as session:
        data = {
            "name": "Joe Donde",
            "role": "Salesman",
            "dept": "Sales",
            "email": "joe@donde.com",
        }
        joe, created = add_person(session, models.Person(**data))
        assert created is True

        session.commit()  # adiciona um usuário no db de teste
        # uma senha é criada automaticamente e de modo aleatório

        user = session.exec(
            select(models.Person.id)
            .where(models.Person.email == data["email"])
        )

        user = [i for i in user][0]

        assert user == 1  # checando se o usuário foi inserido na id 1

        #  pegar o password da tabela, que foi criado aleatoriamente
        pass_ = session.exec(
            select(models.User).
            where(models.User.person_id == user)
        )
        pass_ = [i for i in pass_][0].password

        log = check_user_password(data["email"], pass_)

        assert log == "Salesman"
