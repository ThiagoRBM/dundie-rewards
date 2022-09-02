# o modulo de "entry point" para um programa python chama __main__.py
# ele faz com que um pacote seja transformado em um modulo executavel.
# o __init__.py inicializa o programa (e pode alterar alguns comportamentos e
# ter hacks) e o __main__.py é o arquivo principal.
# quando o programa for chamado, vai ser inicializado pelo init e ser executado
# pelo main.
# com o main é possível rodar no terminal:
# python -m dundie
# se ele for deletado, não será

# from dundie import cli # cada bibliteca instalada (dundie foi instalada) é um
# namespace e dá para chamar na hora de importar (esse é um import absoluto)
from dundie.cli import main  # import só a funcao main

# from .cli import main # import só a funcao main, import RELATIVO (pega na
# mesma pasta com o ".")

if __name__ == "__main__":
    main()
