import pytest
from unittest.mock import patch  # usa o "mocking".

MARKER = """\
integration: mark integration tests
unit: mark unit tests
high: high priority
medium: medium priority
low: low priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield  # testes vem para cá: /tmp/pytest-of-thiagorbm/pytest-current


@pytest.fixture(autouse=True, scope="function")
def setup_testing_database(request):
    """Cria um banco de dados para cada teste em tmpdir e evitar conflitos
    Força database.py a usar esse diretório"""
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.json"))
    with patch("dundie.database.DATABASE_PATH", test_db):
        yield  # testes vem para cá: /tmp/pytest-of-thiagorbm/pytest-current
