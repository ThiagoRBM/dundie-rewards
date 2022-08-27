## além do main e init, é importante ter um arquivo de "build" que ajuda no empacotamente
## ele fica na raiz do REPOSITÓRIO (mesmo lugar do README) e chama setup.py
## O setup.py é transformado para outro formato e colocado no binário do python.
## nele ficam informações importantes para que o programa possa ser instalando.
## o jeito mais tracional é usando o setuptools. Ele é necessário para
## o jeito mais tracional é usando o setuptools. Ele é necessário para
## o pacote poder ser instalado.
## python setup.py build ## cria um wheel e cria a pasta build
## tree -L 2 build
## pip install -e ## se dentro do diretorio atual existe um arquivo setup.py
## ao instalar com o -e, alteracoes feitas no repositorio sao automaticamente
## "instaladas".
## "instaladas".
## pip list # dundie apareceu na lista, como editável.
## pasta egg.info metadados como dependências e etc.

from setuptools import setup, find_packages

setup(
    name= "dundie", ## pode ser qualquer coisa. É o nome que será usado do pip
    version= "0.1.0", ## padrão semantic versioning
    description= "Rewars point system",
    author= "thiago",
    packages= find_packages(), ## pastas com o programa. Esse comando pega todas as pastas com arquivo init dentro. Pode ser feito manualmente também com listas.
    entry_points= {
        "console_scripts": [ ## especificar tipo de entrypoint
            "dundie = dundie.__main__:main" ## nome que será chamado no terminal e o pacote do entrypoint, especificando o modulo (__main__) e a funcao zz
        ]
    }
)
