import pkg_resources  # pega informacoes do repositório lá no setup.py
import rich_click as click  # lib para facilitar a criação da CLI
from rich.console import Console  # para printar a tabela ao final
from rich.table import Table  # Table é uma classe para printar tabelas

from dundie import core  # noqa

# Configuracoes gerais do rich_click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(
    pkg_resources.get_distribution("dundie").version
)  # adicionar versão
def main():
    """Dunder Mifflin reward system

    Essa aplicação de CLI controla o sistema de prêmios
    """


@main.command()  # agrega essa função no main
@click.argument(
    "filepath", type=click.Path(exists=True)
)  # o próprio click vai
# validar se o caminho está certo e outras coisas checagens
def load(filepath):  # dependency injection // dundie load --help
    """Load the file to the database

    # Features
    - Validates data
    - Parses the file
    - Loads to database
    """

    table = Table(title="Dunder Mifflin Associates")
    headers = ["name", "dept", "role", "created", "e-mail"]
    for header in headers:
        table.add_column(header, style="#e96600")

    result = core.load(filepath)
    for person in result:
        table.add_row(
            *[str(value) for value in person.values()], style="#0078e9"
        )

    console = Console()  # não da para simplesmente printar a tabela porque é
    # necessário saber o tamanho do terminal
    console.print(table)
