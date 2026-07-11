# Guia de contribuição

## Primeiramente

Antes de enviar uma alteração para este repositório, se já não houver uma issue, crie uma a partir do template, e utilize as tags oferecidas para ajudar na identificação da issue.

Certifique-se sobre as nossas políticas:

- [Código de conduta](https://fga-eps-mds.github.io/2026.1-MeasureSoftGram-DOC/guia-de-contribuicao/codigo-de-conduta/)
- [Política de Commits](https://fga-eps-mds.github.io/2026.1-MeasureSoftGram-DOC/guia-de-contribuicao/politica-de-commits/)
- [Política de Branches](https://fga-eps-mds.github.io/2026.1-MeasureSoftGram-DOC/guia-de-contribuicao/politica-de-branch/)
- Critérios de aceitação devidamente cumpridos
- Testes automatizados para tudo o que for alterado

## Setup local

Use um ambiente virtual e instale as dependências (o próprio pacote entra em modo
editável, então o comando `msgram` fica disponível):

```bash
python3 -m venv .venv
source .venv/bin/activate
make install     # pip install -r requirements.txt
make test        # roda testes + lint via tox
make lint        # black + flake8
```

A CLI lê apenas a variável de ambiente `LOG` (nível de log: `verbose` ou
`quiet`). Um template está em `env-vars/.env.example`; copie-o para `.env` se
quiser ajustar o nível localmente.

## Crie branches ou fork

Crie sua branch para trabalhar, ou faça um fork do repositório, caso seja um desenvolvedor externo.

## Crie pull request

Crie um pull request no Github, selecionando a branch `develop` como base e a sua branch como comparação.

## Revisões

Se mudanças forem solicitadas, corrija-as e solicite uma nova revisão.

**Muito obrigado por contribuir!!**