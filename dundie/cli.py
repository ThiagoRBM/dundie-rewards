import json

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
    headers = ["email", "name", "dept", "role", "currency", "created"]
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


@main.command()
@click.option("--dept", required=False)  # se deixado em branco,
# mostra todo o DB
@click.option("--email", required=False)  # se deixado em branco,
# mostra todo o DB
@click.option("--output", default=None)  # passar se quer salvar.
def show(output, **query):
    """Shows info about an specific email or entire department and if
    left without arguments, all employees are shown.
    Saves information on specified path if output is supplied.

    # Info shown
    - Account balance (points to spend)
    - Last Movement
    - Name
    - Department
    - Role

    Example::
        dundie show --dept=sales
        dundie show --dept=sales --output=/tmp/foo.json

    """
    result = core.read(**query)

    if output:
        with open(output, "w") as output_file:
            output_file.write(json.dumps(result))

    if not result:
        print("Nothing to show")

    table = Table(title="Dunder Mifflin Report")
    for key in result[0]:
        table.add_column(key.title(), style="#e96600")

    for person in result:
        person["value"] = f"{person['value']:.2f}"
        person["balance"] = f"{person['balance']:.2f}"
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context  # para mostrar a tabela no CLI após fazer a movimentação
# possibilita que um comando chame outro
def add(ctx, value, **query):
    """Add points to user or dept."""
    core.add(value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context  # para mostrar a tabela no CLI após fazer a movimentação
def remove(ctx, value, **query):
    """Remove points from user or dept."""
    core.add(-value, **query)
    ctx.invoke(show, **query)
