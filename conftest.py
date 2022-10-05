import pytest
from unittest.mock import patch  # usa o "mocking"
from sqlmodel import create_engine
from dundie import models


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
    """Cria um banco de dados para cada teste em tmpdir e evita conflitos
    Força database.py a usar esse diretório"""
    tmpdir = request.getfixturevalue("tmpdir")
    test_db = str(tmpdir.join("database.test.db"))
    # breakpoint()
    engine = create_engine(f"sqlite:///{test_db}")
    models.SQLModel.metadata.create_all(bind=engine)
    with patch("dundie.database.engine", engine):
        yield  # testes vem para cá: /tmp/pytest-of-thiagorbm/pytest-current
