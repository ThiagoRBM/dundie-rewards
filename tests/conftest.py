import pytest

MARKER= """\
integration: mark integration tests
unit: mark unit tests
high: high priority
medium: medium priority
low: low priority
"""

def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)

@pytest.fixture(autouse= True) ## TODOS os testes vão usar o comportamento colocado aqui
def go_to_tmpdir(request): ## muda a pasta para um diretório temporário (/tmp/pytest-of-thiagorbm). Não precisa criar o request. Quem o fornece é o pytest. Dependency Injection
    tmpdir= request.getfixturevalue("tmpdir") ## usa a pasta do pytest
    with tmpdir.as_cwd(): ## pytest vai rodar dentro desse gerenciador e execute os testes no diretorio temporario
        yield ## ao invés de usar return, usar yield que gera um resultado e continua a funcao. Protocolo de generators.


