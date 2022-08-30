from subprocess import check_output ## com isso é possível rodar qualquer comando
import pytest

@pytest.mark.integration
@pytest.mark.medium
def test_load():
    """Testar o comando load."""
    out= check_output(
        ["dundie", "load", "tests/assets/people.csv"]
    ).decode("utf-8").split("\n") ## comandos que são passados no terminal
    assert len(out) == 2
