import os
from setuptools import setup, find_packages

def read(*paths):
    """Lê arquivos text.
    >>> read("projeto","VERSION")
    '0.1.0'
    >>> read(README.md)
    """
    rootpath= os.path.dirname(__file__) ## retorna o caminho de setup.py
    filepath=os.path.join(rootpath, *paths)
    with open(filepath) as file_:
        return file_.read().strip()

def read_requierements(path):
    """Retorna a lista d requirements de um arquivo texto."""
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(("#", "git+", '"', '-'))
    ]


setup(
    name= "dundie", ## pode ser qualquer coisa. É o nome que será usado do pip
    version= "0.1.0", ## padrão semantic versioning
    description= "Rewars point system",
    #long_description= read_requierements("README.md"), ## essa linha estava dando problema na hora de rodar make install, Bruno falou para substituir e funcionou
    long_description="test",
    long_description_content_type= "text/markdown",
    author= "thiago",
    python_requires= ">=3.8",
    packages= find_packages(), ## pastas com o programa. Esse comando pega todas as pastas com arquivo init dentro. Pode ser feito manualmente também com listas.
    entry_points= {
        "console_scripts": [ ## especificar tipo de entrypoint
            "dundie = dundie.__main__:main" ## nome que será chamado no terminal e o pacote do entrypoint, especificando o modulo (__main__) e a funcao zz
        ]
    },
    install_requires= read_requierements("requirements.txt"),
    extras_require= {
        "test": read_requierements("requirements.test.txt"),
        "dev": read_requierements("requirements.dev.txt")
    }
)
