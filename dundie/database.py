import warnings

from sqlalchemy.exc import SAWarning
from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, SelectOfScalar

from dundie import models  # IMPORTANTE importar
from dundie.settings import SQL_CONN_STRING

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
