import pytest

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


@pytest.mark.unit
@pytest.mark.parametrize("address", ["thiagorbm@gmail.com", "joe@doe.com"])
def test_positive_check_valid_email(address):
    """Ensures email is valid"""
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.parametrize("address", ["@doe.com", "joe@.com", "a@b"])
def test_negative_check_valid_email(address):
    """Ensures email is valid"""
    assert check_valid_email(address) is False


@pytest.mark.unit
def test_generate_simple_password():
    """Test generation of randim simple password.
    TODO: Generate hashed complex passrowds.
    """
    passwords = []  # garantir que mesmo com centenas de passwords gerados, não
    # haja repetições
    n = 1000  # especificar numero de testes
    for i in range(n):
        passwords.append(generate_simple_password(8))
    # [print(p) for p in passwords]  # ver os passwords
    assert (
        len(set(passwords)) == n
    )  # lembrando: set não aceitam valores duplicados. Se ao transformar
    # a lista em set, o comprimento for < 100, alguma foi igual
