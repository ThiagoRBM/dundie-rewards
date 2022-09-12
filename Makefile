.PHONY: install virtualenv ipython clean test watch pflake8 build docs docs-serve build
# assim o makefile não cria arquivos extras (que é o padrão), coloca os comandos que foram criados abaixo


install: # rodar como "make install
	@echo "instalando para ambiente de desenvolvimento" # o arroba no início omite o comando em si
	@.venv/bin/python -m pip install -e '.[test,dev]' # adicionando o caminho para ativar a venv e instalar nela. Se ela não existir, ele falha por padrão


virtualenv: # rodar como "make virtualenv"
	@python -m venv .venv # comando para criar uma venv caso não exista


ipython:
	@.venv/bin/ipython


lint: # "buscar problemas", linters
	@.venv/bin/pflake8


fmt: # roda o black e formata o código
	@.venv/bin/isort dundie  # tests integration setup.py # chama o isort
	@.venv/bin/black dundie  # tests integration setup.py # nessas pastas


test: # testes unitarios
	@.venv/bin/pytest -s --forked  # tests integration
	# -- forked usa o pytest-forked

watch:
	#@.venv/bin/ptw # rodar o pytest-watch automaticamente ao salvar algum
	# arquivo do projeto
	@ls **/*.py | entr pytest --forked  # faz a mesma coisa que o ptwd, mas
	# funciona com o arquivo .toml pq o ptwd nao funcionou com ele.
	# É uma ferramenta do UNIX e não python; sudo apt install entr
	# -- forked usa o pytest-forked

clean:            # Clean unused files. Util quando limpamos para fazer outra build
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

docs:  # gera o site
	@mkdocs build --clean


docs-serve:  # cria uma pasta para o site
	@mkdocs serve


build:  # faz a build do repositório
	@python setup.py sdist bdist_wheel


publish-test:  # publica no testpypi
	@twine upload --repository testpypi dist/*


publish:  # publica no pypi
	@twine upload dist/*
