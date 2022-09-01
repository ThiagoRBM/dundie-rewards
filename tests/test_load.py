from dundie.core import load
from .constants import PEOPLE_FILE
import pytest

@pytest.mark.unit
@pytest.mark.high
def test_positive_has_2_names():
    """Testes da função load."""
    assert len(load(PEOPLE_FILE)) == 3

@pytest.mark.unit
@pytest.mark.high
def test_positive_starts_with_f():
    assert load(PEOPLE_FILE)[0][0] == "f" # primeira letra do primeiro item == f
