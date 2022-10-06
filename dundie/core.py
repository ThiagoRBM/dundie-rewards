import sys
from csv import reader
from decimal import Decimal
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import check_user_password, get_session
from dundie.models import Balance, Movement, Person
from dundie.settings import DATEFMT
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
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
    headers = ["name", "dept", "role", "email", "currency"]

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

    User must be logged to run command. Checks user's permissions
    before running.
    """

    #  transforma a query em um dicionário para processamento
    query = {k: v for k, v in query.items() if v is not None}

    if "login" not in query:
        login = input("Digite seu email:\n").strip()
    else:
        login = query["login"]
        query.pop("login")

    if "senha" not in query:
        senha = input("Digite sua senha:\n").strip()
    else:
        senha = query["senha"]
        query.pop("senha")

    role = check_user_password(login, senha)
    # print(role)
    return_data = []

    with get_session() as session:
        #  obtem os departamentos existentes
        sql = select(Person.dept)
        depts = session.exec(sql)
        depts = set([dept for dept in depts])
        # print(depts)

    with get_session() as session:
        #  obtem os emails existentes
        sql = select(Person.email)
        emails = session.exec(sql)
        emails = set([dept for dept in emails])

    if role == "CEO":
        #  caso o usuário seja CEO, tem acesso aos dados de
        #  qualquer funcionário ou departamento

        query_statements = []
        if "dept" in query:
            if query["dept"] in depts:
                query_statements.append(Person.dept == query["dept"])
            else:
                print(f"Departamento '{query['dept']}' não existe.")
                sys.exit(0)

        if "email" in query:
            if query["email"] in emails:
                query_statements.append(Person.email == query["email"])
            else:
                print(f"Usuário '{query['email']}' não existe.")
                sys.exit(0)

        sql = select(Person)  # SELECT FROM PERSON
        # breakpoint()
        if query_statements:  # caso haja query, são passados em list pro where
            sql = sql.where(*query_statements)  # WHERE

        with get_session() as session:
            currencies = session.exec(
                select(Person.currency).distinct(Person.currency)
            )
            rates = get_rates(currencies)
            results = session.exec(sql)
            # breakpoint()
            for person in results:
                total = rates[person.currency].value * person.balance[0].value
                return_data.append(
                    {
                        "email": person.email,
                        "balance": person.balance[0].value,
                        "last_movement": person.movement[-1].date.strftime(
                            DATEFMT
                        ),
                        **person.dict(exclude={"id"}),
                        **{"value": total},
                    }
                )

    elif role == "manager":
        #  caso o funcionário seja manager, tem acesso a todos os funcionários
        #  do mesmo setor (subordinados)

        query_statements = []
        with get_session() as session:
            #  pega o departamento do manager
            #  e os emails do mesmo departamento
            sql = select(Person).where(Person.email == login)
            dept = session.exec(sql)
            dept = [i for i in dept][0].dept

            sql = select(Person).where(Person.dept == dept)
            emails_dept = session.exec(sql)
            emails_dept = [i.email for i in emails_dept]
            # print(emails_dept)

        if "dept" in query:
            if query["dept"].lower() != dept.lower():
                print(f"Usuário com acesso apenas ao departamento: {dept}.")
                sys.exit(0)
            else:
                query_statements.append(Person.dept == query["dept"])

        if "email" in query:
            if query["email"] not in emails_dept and query["email"] in emails:
                print(
                    f"Funcionário {query['email']} é de outro departamento."
                    f"Acesso negado."
                )
                sys.exit(0)
            elif (
                query["email"] not in emails_dept
                and query["email"] not in emails
            ):
                print(f"Usuário {query['email']} não existe.")
                sys.exit(0)
            else:
                query_statements.append(Person.email == query["email"])

        if not query_statements:
            #  caso nada seja passado após show, é mostrado o departamento
            #  inteiro
            query_statements.append(Person.dept == dept)

        sql = select(Person)  # SELECT FROM PERSON
        sql = sql.where(*query_statements)

        with get_session() as session:
            currencies = session.exec(
                select(Person.currency).distinct(Person.currency)
            )
            rates = get_rates(currencies)
            results = session.exec(sql)
            for person in results:
                total = rates[person.currency].value * person.balance[0].value
                return_data.append(
                    {
                        "email": person.email,
                        "balance": person.balance[0].value,
                        "last_movement": person.movement[-1].date.strftime(
                            DATEFMT
                        ),
                        **person.dict(exclude={"id"}),
                        **{"value": total},
                    }
                )

    elif role == 0:
        sys.exit(0)

    else:
        #  se o usuário não for nem CEO nem manager, só tem acesso aos próprios
        #  dados

        if "dept" in query:
            print("Operação não permitida.")
            sys.exit(0)

        if "email" in query:
            if query["email"] != login and query["email"] in emails:
                print("Operação não permitida.")
                sys.exit(0)
            else:
                print(f"Usuário '{query['email']}' não existe.")
                sys.exit(0)

        with get_session() as session:
            sql = select(Person)
            sql = sql.where(Person.email == login)

            with get_session() as session:
                currencies = session.exec(
                    select(Person.currency).distinct(Person.currency)
                )
                rates = get_rates(currencies)
                results = session.exec(sql)
                for person in results:
                    total = (
                        rates[person.currency].value * person.balance[0].value
                    )

                    return_data.append(
                        {
                            "email": person.email,
                            "balance": person.balance[0].value,
                            "last_movement": person.movement[-1].date.strftime(
                                DATEFMT
                            ),
                            **person.dict(exclude={"id"}),
                            **{"value": total},
                        }
                    )

    return return_data


def add(value: Decimal, **query: Query):
    """Add value to each record on query.
    User must be logged to run.
    """
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    role = check_user_password(query["login"], query["senha"])

    if role not in ["manager", "CEO"]:
        print("Operação não permitida.")
        sys.exit(0)

    if not people:
        raise RuntimeError("Not Found")

    with get_session() as session:
        user = query["login"]  # por enquanto pega o user do ENV do sistema
        # caso o argumento seja deixado em branco
        for person in people:
            if person["email"] != query["login"]:
                instance = session.exec(
                    select(Person).where(Person.email == person["email"])
                ).first()
                add_movement(session, instance, value, user)

                donnor = session.exec(
                    select(Person).where(Person.email == query["login"])
                ).first()

                donnor_balance = session.exec(
                    select(Balance).where(Balance.person_id == donnor.id)
                ).first()
                #breakpoint()
                if donnor_balance.value - value < 0:
                    print(f"Saldo insuficiente: {donnor_balance.value}")
                    sys.exit(0)
                else:
                    donnor_balance.value = donnor_balance.value - value

                    session.commit()


def read_movements(**query: Query):
    """Reads user's movement history from the Balance table."""

    query = {k: v for k, v in query.items() if v is not None}
    # breakpoint()
    # print("aqui")
    if "login" not in query:
        login = input("Digite seu email:\n").strip()
    else:
        login = query["login"]
        query.pop("login")

    if "senha" not in query:
        senha = input("Digite sua senha:\n").strip()
    else:
        senha = query["senha"]
        query.pop("senha")

    role = check_user_password(login, senha)

    if not role:
        sys.exit(0)
    else:
        with get_session() as session:

            #  aqui, selecionando as movimentacoes de acordo com o LOGIN
            #  a partir da coluna Movement.person_id pego qual é o email
            #  que RECEBEU a tranferência
            History = session.exec(
                select(Person.email, Movement).where(
                    Movement.actor == login, Person.id == Movement.person_id
                )
            )
            History = [i for i in History]
            # breakpoint()

            Movements = []
            for movement in History:
                # breakpoint()
                Movements.append(
                    {
                        "donnor": movement[1].actor,
                        "date": movement[1].date.strftime(DATEFMT),
                        "value": Decimal(movement[1].value),
                        "receptor": movement[0],
                    }
                )
            # breakpoint()
            return Movements
