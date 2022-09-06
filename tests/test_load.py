import pytest

from dundie.core import load

from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_positive_has_2_names():
    """Testes da função load."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
def test_positive_starts_with_fulano(request):
    print(f"TESTE= {load(PEOPLE_FILE)}")
    assert (
        load(PEOPLE_FILE)[0]["name"] == "fulano"
    )  # primeira letra do primeiro item == fulano
