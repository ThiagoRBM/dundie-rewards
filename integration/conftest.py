MARKER = """\
integration: mark integration tests
unit: mark unit tests
high: high priority
medium: medium priority
low: low priority
"""


def pytest_configure(
    config,
):  # faz a mesma coisa que a funcao do conftest unitario, usando map
    map(
        lambda line: config.addinivalue_line("markers", line),
        MARKER.split("\n"),
    )
