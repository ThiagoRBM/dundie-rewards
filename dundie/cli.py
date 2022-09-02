import argparse  # substitui o sys e sys.argv

from dundie.core import load  # noqa


def main():
    parser = argparse.ArgumentParser(
        description="Dunder Mifflin Rewards CLI",
        epilog="...",
    )
    parser.add_argument(
        "subcommand",
        type=str,
        help="the subcommand to run",
        choices=("load", "show", "send"),
        default="help",
    )
    parser.add_argument(
        "filepath", type=str, help="Filepath to load", default=None
    )

    args = parser.parse_args()
    # print(args)
    # print([key for key in globals().keys()]) # vendo o que está disponível
    # em globals

    print(
        *globals()[args.subcommand](args.filepath)
    )  # pega a funcao "load" e usa como argumento o "filepath"

    # print("executando main pelo entrypoint")
