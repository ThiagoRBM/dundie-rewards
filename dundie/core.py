from dundie.utils.log import get_logger


"""Funcoes principais"""


def load(filepath):
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv')) ## doctest, para rodar no terminal: python -m doctest -v dundie/core.py
    2
    """
    try:
        with open(filepath) as file_:
            return [line.strip() for line in file_.readlines()]
    except FileNotFoundError as e:
        log.error(str(e))
        raise e
