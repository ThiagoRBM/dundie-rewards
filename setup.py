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
