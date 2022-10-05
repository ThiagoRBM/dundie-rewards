import sys
import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, create_engine, select
from sqlmodel.sql.expression import Select, SelectOfScalar

from dundie import models  # IMPORTANTE importar
from dundie.settings import SQL_CONN_STRING
from dundie.utils.email import check_valid_email

# We have to monkey patch this attributes
# https://github.com/tiangolo/sqlmodel/issues/189
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

warnings.filterwarnings("ignore", category=SAWarning)

engine = create_engine(SQL_CONN_STRING, echo=False)
models.SQLModel.metadata.create_all(bind=engine)
#  acima, pega as tabelas de models e as cria


def get_session() -> Session:
    """Funcao para criar uma Session com engine"""
    return Session(engine)


def check_user_password(login: str, password: str):
    """Checa se um usuário existe e se a senha
    passada bate com o que foi passado na função."""

    if check_valid_email(login) is False:
        print(f"Email '{login}' inválido.")
        sys.exit(0)

    with get_session() as session:

        #  verificar se o user existe
        user = session.exec(
            select(models.Person.id).where(models.Person.email == login)
        )

        try:
            id_ = [i for i in user][0]
        except IndexError:
            print(f"Usuário não encontrado: '{login}'")
            return 0

        #  pegar o password da tabela
        pass_ = session.exec(
            select(models.User).where(models.User.person_id == id_)
        )
        pass_ = [i for i in pass_][0].password

    if pass_ == password:  # caso a senha passada seja igual a recupera,
        # retorna True
        role = session.exec(
            select(models.Person.role).where(models.Person.id == id_)
        )
        # print(f"Logado como '{login}'.")

        return [i for i in role][0]  # retorna o role da pessoa

    else:
        print("Senha incorreta.")
        return 0


# breakpoint()
