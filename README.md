# MeasureSoftGram-CLI

## Badges

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-CLI&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-CLI)
[![Downloads](https://static.pepy.tech/badge/msgram)](https://pepy.tech/project/msgram)
[![Downloads](https://static.pepy.tech/badge/msgram/month)](https://pepy.tech/project/msgram)
[![Downloads](https://static.pepy.tech/badge/msgram/week)](https://pepy.tech/project/msgram)
[![PyPI](https://img.shields.io/pypi/v/msgram.svg)](https://pypi.python.org/pypi/msgram/)

> **Este README resume o componente CLI.** A documentação completa do produto — incluindo o uso
> detalhado da CLI, as políticas de contribuição e o código de conduta — é central e vive no
> [MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/).

## O que é

O **MeasureSoftGram-CLI** (pacote [`msgram`](https://pypi.org/project/msgram/)) é a interface de linha de comando do MeasureSoftGram. É o módulo responsável por configurar o modelo de qualidade, extrair métricas de exports do SonarQube/SonarCloud e do GitHub, e calcular localmente os valores das medidas, subcaracterísticas e características do modelo algébrico.

## Como Executar o Projeto

Requisitos: **Python 3.9 ou superior** (o CI de testes e lint roda em 3.10).

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
make install
```

*(Equivale a `pip install -r requirements.txt`, que instala o próprio pacote em modo editável — o comando `msgram` fica disponível no terminal).*

### 3. Verificar a instalação

```bash
msgram -h
```

### 4. Ver a CLI funcionando (demo)

Para executar o fluxo completo (init, extract e calculate) sobre o dataset de exemplo embutido em `examples/analytics-raw-data/`, sem precisar fornecer dados próprios nem acesso à rede:

```bash
msgram demo
```

O resultado é gerado em `./msgram-demo/`.

---

## Principais Comandos

### Comandos da CLI

| Comando | Descrição |
|---|---|
| `msgram init` | Cria o arquivo de configuração padrão do modelo (`.msgram/msgram.json`) |
| `msgram list` | Lista os parâmetros da configuração atual |
| `msgram extract` | Extrai as métricas suportadas a partir dos arquivos de análise |
| `msgram calculate` | Calcula os valores das entidades do modelo a partir das métricas extraídas |
| `msgram diff` | Calcula e interpreta a diferença entre os tensores planejado (RP) e desenvolvido (RD) |
| `msgram norm_diff` | Calcula a norma de Frobenius da diferença entre os tensores RP e RD |
| `msgram demo` | Executa o pipeline completo sobre o dataset de exemplo embutido |
| `msgram <comando> -h` | Exibe as opções de um comando específico |

### Alvos do Makefile

| Comando | Descrição |
|---|---|
| `make install` | Instala as dependências, incluindo o próprio pacote em modo editável |
| `make test` | Roda testes + lint via `tox` |
| `make lint` | Roda `black` e `flake8` via `tox` |
| `make format` | Formata o código com `black` |
| `make build` | Gera os artefatos de distribuição (sdist + wheel) |
| `make clean` | Remove artefatos de build e caches |
| `make help` | Lista os alvos disponíveis |

> 📖 **Flags, valores padrão e o fluxo típico de uso de cada subcomando estão na [Referência da CLI](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/referencia-cli/).**

---

## Como Rodar os Testes

```bash
# Testes + lint via tox
make test

# Apenas os linters
make lint
```

Para rodar um arquivo de teste específico com o pytest:

```bash
pip install pytest pytest-cov pytest-mock
pytest tests/unit/test_calculate.py
```

---

## Documentação

A documentação oficial e completa é central: **[MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/)**. Este repositório guarda apenas o código do componente e um resumo. As páginas mais relevantes para esta CLI:

- [Primeiros passos](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/primeiros-passos/) — tutorial da instalação até o primeiro relatório de qualidade
- [Referência da CLI](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/referencia-cli/) — subcomandos, flags, valores padrão e fluxo típico
- [Como usar](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-usar/) — uso da CLI, como subir o sistema completo e problemas comuns
- [Componente CLI](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/componente-cli/) — pré-requisitos, setup a partir do código-fonte, testes e publicação no PyPI
- [Como contribuir](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-contribuir/) — fluxo de issue/branch/PR, padrão de commits e Definition of Done

## Informações Adicionais

- **PyPI:** [msgram](https://pypi.org/project/msgram/)
- **Docker Hub:** [Core](https://hub.docker.com/r/measuresoftgram/core) · [Service](https://hub.docker.com/r/measuresoftgram/service)
- **Documentação:** [MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/)
- **Guia de Contribuição:** Veja nosso [Guia de Contribuição](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-contribuir) e o arquivo [CONTRIBUTING.md](./CONTRIBUTING.md).
- **Demais repositórios do produto:**
  - [Core](https://github.com/fga-eps-mds/MeasureSoftGram-Core)
  - [Service](https://github.com/fga-eps-mds/MeasureSoftGram-Service)
  - [Front Web](https://github.com/fga-eps-mds/MeasureSoftGram-Front)
  - [Action](https://github.com/fga-eps-mds/MeasureSoftGram-Action)
  - [Parser](https://github.com/fga-eps-mds/MeasureSoftGram-Parser)
  - [Docs](https://github.com/fga-eps-mds/MeasureSoftGram-Docs)

## Contribuição

As políticas de contribuição são as mesmas para todos os repositórios do produto e estão em **[Guia de Contribuição e Padrões](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-contribuir)**. Consulte também o [CONTRIBUTING.md](./CONTRIBUTING.md) deste repositório.

## Código de Conduta

Este projeto segue o **[Código de Conduta](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/codigo-de-conduta)** do MeasureSoftGram, único para todos os repositórios. Veja também o [code_of_conduct.md](./code_of_conduct.md).

## Licença

Este projeto é distribuído sob a licença [AGPL-3.0](./LICENSE).
