from dundie.core import load
from .constants import PEOPLE_FILE
import uuid
import pytest

#@pytest.fixture(scope="function", autouse= True) ## todas as funcoes DESSE arquivo em autouse=True
#def create_new_file(tmpdir): ## cria no tmpdir
#    tmpdir.join("new_file.txt").write("isso é sujeira")

@pytest.fixture(scope="function") ## apenas a funcao em que a funcao create_new_file for argumento usara a fixture
def create_new_file(tmpdir): ## cria no tmpdir
    tmpdir.join("new_file.txt").write("isso é sujeira")

@pytest.mark.unit
@pytest.mark.high
def test_load(create_new_file):
    """Testes da função load."""
    with open(f"arquivo_indesejado-{uuid.uuid4()}.txt", "w") as f:
        f.write("dados uteis somente para o teste")
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == "f" # primeira letra do primeiro item == f


@pytest.mark.unit
@pytest.mark.high
def test_load(request): ## mesmo request do modulo conftest
    """Testes da função load."""

    request.addfinalizer(lambda: print("terminou")) ## funcao roda depois que o teste termina

    with open(f"arquivo_indesejado-{uuid.uuid4()}.txt", "w") as f:
        f.write("dados uteis somente para o teste")
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == "f" # primeira letra do primeiro item == f
