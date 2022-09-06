import pytest
from click.testing import CliRunner  # roda comandos durante o teste

from dundie.cli import load, main

from .constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Testar o comando load."""
    out = cmd.invoke(load, PEOPLE_FILE)
    assert str("Dunder Mifflin Associates") in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize(
    "wrong_command", ["loady", "carrega", "start"]
)  # o teste vai rodar com cada palavra depois de "wonrg command"
def test_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Testar o comando load."""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)

    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output
