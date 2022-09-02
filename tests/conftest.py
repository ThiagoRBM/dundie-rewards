MARKER = """\
integration: mark integration tests
unit: mark unit tests
high: high priority
medium: medium priority
low: low priority
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)
