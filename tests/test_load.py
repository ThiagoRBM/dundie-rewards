from dundie.core import load
from .constants import PEOPLE_FILE
import pytest

@pytest.mark.unit
@pytest.mark.high
def test_load():
    """Testes da função load."""
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == "f" # primeira letra do primeiro item == f
