# arquivo que vai manipular o arquivo json

import json
from datetime import datetime

from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import check_valid_email, send_mail
from dundie.utils.user import generate_simple_password

EMPTY_DB = {"people": {}, "balance": {}, "movement": {}, "users": {}}
# esse é o "formato" do arquivo json que servirá como DB provisoriamente


def connect() -> dict:  # funcao para se conectar com banco de dados
    """Funcao que abre o arquivo JSON. Retorna um dict."""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return EMPTY_DB  # caso o banco não seja JSON ou não exista,


# o banco vazio é retornado


def commit(db) -> dict:
    """Salva as informações alteradas ou adicionadas no DB.
    Testa se o formato dos dados passado estão seguindo o padrão estabelecido
    """
    if db.keys() != EMPTY_DB.keys():
        raise ("Database schema is invalid.")

    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_person(db, pk, data):
    """Adiciona pessoa ou atualiza informacoes de pessoa no bando de dados
    db: banco de dados, pk: primary key (email da pessoa), data: dados a serem
    pasados.

    - E-mail é único
    - Se o usuário existir, informações serão atualizadas
    - Banlanço inicial (manager= 100, others= 500)
    - Gera uma senha, se o usuário é novo e a envia por email
    """
    if not check_valid_email(pk):
        raise ValueError(f"{pk} não é um email válido")

    table = db["people"]
    person = table.get(pk, {})  # caso o usuário não exista, retorna um dict
    # vazio
    created = not bool(person)  # se retornar True: dicionário está vazio
    # então a pessoa não existe no DB e um dicinário vazio vai ter sido
    # criado
    person.update(data)  # atualiza o dicionário com as informações passadas
    table[pk] = person  # atualiza o DB com o dicionário atualizado
    if created:  # se for um usuário novo
        set_initial_balance(db, pk, person)
        password = set_inital_password(db, pk)
        send_mail(EMAIL_FROM, pk, "Your Dundie password.", password)
        #  TODO: encrypt and send link, not password
    return person, created


def set_inital_password(db, pk):
    """Gera e salva senha"""
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = generate_simple_password(8)
    return db["users"][pk]["password"]


def set_initial_balance(db, pk, person):
    """Adiciona movimentaçoes de pontos e especifica o balanço inicial

    - Manager= 100
    - Others= 500
    """
    value = 100 if person["role"] == "manager" else 500
    add_movement(db, pk, value)


def add_movement(db, pk, value, actor="system"):
    """Cria a movimentação da pontuação entre usuário"""
    movements = db["movement"].setdefault(pk, [])
    # usa a tabela de MOVIMENTACAO e busca pela chave pk. Se ela não
    # existir, eu forneço um valor padrão, uma lista vazia
    movements.append(
        {"date": datetime.now().isoformat(), "actor": actor, "value": value}
    )
    db["balance"][pk] = sum([item["value"] for item in movements])
