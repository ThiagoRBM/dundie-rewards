## o modulo de "entry point" para um programa python chama __main__.py
## ele faz com que um pacote seja transformado em um modulo executavel.
## o __init__.py inicializa o programa (e pode alterar alguns comportamentos e
## ter hacks) e o __main__.py é o arquivo principal.
## quando o programa for chamado, vai ser inicializado pelo init e ser executado
## pelo main.
## com o main é possível rodar no terminal:
##python -m dundie
## se ele for deletado, não será

print("executando main")
