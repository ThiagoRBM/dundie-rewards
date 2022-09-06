import pytest

from dundie.database import EMPTY_DB, add_person, commit, connect


@pytest.mark.unit
def test_database_schema():
    """Funcao que testa o formato do DB.
    Abre e verifica se os keys da DB passada são iguais ao padrão vazio"""
    db = connect()
    assert db.keys() == EMPTY_DB.keys()


@pytest.mark.unit
def test_database_commit():
    """Testa se as informações estão sendo salvas corretamente no DB"""
    db = connect()  # conecta no DB
    data = {  # faz alterações, como no nome de alguém
        "name": "fulano da silva",
        "role": "salesman",
        "dept": "sales",
    }
    db["people"]["fulano@dunder.com"] = data
    commit(db)  # faz o commit das alterações
    db = connect()  # conecta no DB novamente
    assert db["people"]["fulano@dunder.com"] == data
    # testa se o nome mudou, inicialmente era apenas fulano e depois do
    # commit é para ser fulano da silva
    # /tmp/pytest-of-thiagorbm/pytest-current/test_database_commit0


@pytest.mark.unit
def test_add_person_for_the_first_time():
    pk = "fulano3@doe.com"  # pessoa que nao existe no DB
    data = {"role": "salesman", "dept": "sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, pk, data)
    assert created is True
    commit(db)  # comita as alteracoes

    db = connect()  # conecta novamente ao DB atualizado
    assert db["people"][pk] == data
    assert db["balance"][pk] == 500  # ele não é manager, então tem que ter 500
    assert len(db["movement"][pk]) > 0  # testa que existe a tabela de
    # movimentacao, que é o valor inicial
    assert db["movement"][pk][0]["value"] == 500  # testa que o valor está
    # no índice 0
    # /tmp/pytest-of-thiagorbm/pytest-current/test_add_person_for_the_first_0


@pytest.mark.unit
def test_negative_add_person_invalid_email():
    """Verifica se emails inválidos resultarão em erros ao invés de serem
    adicionados ao DB"""
    with pytest.raises(ValueError):
        add_person({}, ".@bla", {})