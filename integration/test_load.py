from subprocess import check_output, CalledProcessError ## com isso é possível rodar qualquer comando
import pytest

@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Testar o comando load."""
    out= check_output(
        ["dundie", "load", "tests/assets/people.csv"]
    ).decode("utf-8").split("\n") ## comandos que são passados no terminal
    assert len(out) == 2

@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"]) ## o teste vai rodar com cada palavra depois de "wonrg command"
def test_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Testar o comando load."""
    with pytest.raises(CalledProcessError) as error: ## erro de digitação ("loady") gera o CalledProcessError
        check_output(
            ["dundie", wrong_command, "tests/assets/people.csv"] ## recebe a lista do decorator
        ).decode("utf-8").split("\n") ## comandos que são passados no terminal
    assert "status 2" in str(error.getrepr())
