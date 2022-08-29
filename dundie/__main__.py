## o modulo de "entry point" para um programa python chama __main__.py
## ele faz com que um pacote seja transformado em um modulo executavel.
## o __init__.py inicializa o programa (e pode alterar alguns comportamentos e
## ter hacks) e o __main__.py é o arquivo principal.
## quando o programa for chamado, vai ser inicializado pelo init e ser executado
## pelo main.
## com o main é possível rodar no terminal:
##python -m dundie
## se ele for deletado, não será

import argparse ## substitui o sys e sys.argv


def load(filepath):
    """Loads data from filepath to the database."""
    try:
        with open(filepath) as file_:
            for line in file_:
                print(line)
    except FileNotFoundError as e:
        print(f"File not found {e}")


def main():
    parser= argparse.ArgumentParser(
    description= "Dunder Mifflin Rewards CLI",
    epilog= "...",
)
    parser.add_argument(
        "subcommand",
        type= str,
        help= "the subcommand to run",
        choices=("load", "show", "send"),
        default= "help",
    )
    parser.add_argument(
        "filepath",
        type= str,
        help= "Filepath to load",
        default= None
    )

    args= parser.parse_args()
    print(args)
    #print([key for key in globals().keys()]) ## vendo o que está disponível em globals
    globals()[args.subcommand](args.filepath) ## pega a funcao "load" e usa como argumento o "filepath"

    #print("executando main pelo entrypoint")

if __name__ == "__main__":
    main()
