.PHONY: install test lint format build clean help

install:  ## Instala as dependencias (inclui o proprio pacote em modo editavel)
	pip install -r requirements.txt

test:  ## Roda testes + lint via tox
	tox

lint:  ## Roda black + flake8 via tox (o env de lint)
	tox -e lint

format:  ## Formata o codigo com black
	black src tests

build:  ## Gera os artefatos de distribuicao (sdist + wheel)
	python -m build

clean:  ## Remove artefatos de build e caches
	rm -rf build dist *.egg-info src/*.egg-info .tox .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

help:  ## Lista os alvos disponiveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'
