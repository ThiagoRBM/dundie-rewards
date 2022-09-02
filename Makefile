.PHONY: install virtualenv ipython clean test watch pflake8 ## assim o makefile não cria arquivos extras (que é o padrão), coloca os comandos que foram criados abaixo


install: ## rodar como "make install
	@echo "instalando para ambiente de desenvolvimento" ## o arroba no início omite o comando em si
	@.venv/bin/python -m pip install -e '.[dev]' ## adicionando o caminho para ativar a venv e instalar nela. Se ela não existir, ele falha por padrão


virtualenv: ## rodar como "make virtualenv"
	@.venv/bin/python -m pip -m venv .venv ## comando para criar uma venv caso não exista


ipython:
	@.venv/bin/ipython


lint: ## "buscar problemas", linters
	@.venv/bin/pflake8


test: ## testes unitarios
	@.venv/bin/pytest -s -vv tests integration


watch:
	#@.venv/bin/ptw ## rodar o pytest-watch automaticamente ao salvar algum arquivo do projeto
	@ls **/*.py | entr pytest # faz a mesma coisa que o ptwd, mas funciona com o arquivo .toml pq o ptwd nao funcionou com ele. É uma ferramenta do UNIX e não pytho; sudo apt install entr

clean:            ## Clean unused files.
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
