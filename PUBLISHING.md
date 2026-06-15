# Publicacao do pacote `msgram` (CLI)

Guia de como empacotar e publicar este repositorio no PyPI. Escrito para os
proximos grupos: leia inteiro antes da primeira release.

Pacote no PyPI: **`msgram`** (a CLI, comando `msgram` no terminal).
Depende de **`msgram-core`** e **`msgram-parser`**, entao tem cuidados extras
de ordem (ver secao "Ordem de publicacao").

---

## TL;DR

A publicacao e automatica via GitHub Actions e **Trusted Publishing (OIDC)**:
nao existe token nem secret no repositorio. Tudo e disparado por **tag git**.

| Tag que voce cria        | Onde publica       | Quando usar                          |
|--------------------------|--------------------|--------------------------------------|
| `vX.Y.ZrcN` (`v3.3.1rc1`)| TestPyPI           | Testar o pacote antes de producao    |
| `vX.Y.Z` (`v3.3.1`)      | PyPI (producao)    | Release final, depois de validar a rc|

**Trava de seguranca:** a tag final (`vX.Y.Z`) so publica em producao se ja
existir uma release candidate (`vX.Y.ZrcN`) da mesma versao no TestPyPI. Sem rc,
o job falha. E impossivel publicar em producao sem ter testado antes.

---

## Antes de tudo: as dependencias internas

A CLI declara em `pyproject.toml`:

```toml
dependencies = [
    ...
    "msgram-core~=1.5.3",
    "msgram-parser~=1.2.1",
    ...
]
```

Se voce subiu versoes novas de `msgram-core` e/ou `msgram-parser`, **atualize
esses pins aqui** antes de lancar a CLI, e publique core/parser PRIMEIRO (ver
"Ordem de publicacao"). Senao a CLI vai puxar versoes antigas, ou nem instalar.

---

## Fluxo completo de uma release (passo a passo)

1. **Bump da versao para a rc.** Em `pyproject.toml`, ajuste:
   ```toml
   version = "3.3.1rc1"
   ```
   A versao do `pyproject.toml` tem que bater EXATAMENTE com a tag, senao o CI
   falha de proposito (step "Validar tag == versao do pyproject").
2. **Commit + tag da rc:**
   ```bash
   git commit -am "chore: bump 3.3.1rc1"
   git tag v3.3.1rc1
   git push origin develop --tags
   ```
   O push da tag dispara o workflow, que publica no **TestPyPI**.
3. **Teste a rc** instalando do TestPyPI (secao abaixo). Rode `msgram --help` e
   um fluxo real (`extract`, `calculate`).
4. **Se estiver tudo certo, prepare a final.** No `pyproject.toml`:
   ```toml
   version = "3.3.1"
   ```
5. **Commit + tag final:**
   ```bash
   git commit -am "chore: release 3.3.1"
   git tag v3.3.1
   git push origin develop --tags
   ```
   O workflow roda o **gate** (confere que `3.3.1rcN` existe no TestPyPI) e, se
   passar, publica em **producao**.

Achou um problema na rc? Corrija, suba a versao da rc (`3.3.1rc2`) e repita do
passo 1. So promova para final quando a rc estiver boa.

---

## Pre-requisitos: configurar o Trusted Publisher (uma vez por projeto)

Quem tiver acesso de **owner** do projeto no PyPI precisa registrar o publisher
confiavel nos DOIS indices (sao contas/sites separados):

- Producao: <https://pypi.org/manage/project/msgram/settings/publishing/>
- Teste: <https://test.pypi.org/manage/project/msgram/settings/publishing/>

Em cada um, adicione um "GitHub" trusted publisher com:

| Campo               | Valor                              |
|---------------------|------------------------------------|
| Owner               | `fga-eps-mds`                      |
| Repository name     | `2026.1-MeasureSoftGram-CLI`      |
| Workflow filename   | `python-publish.yml`              |
| Environment name    | `pypi` no PyPI / `testpypi` no TestPyPI |

Depois, no GitHub do repo (Settings > Environments), crie os environments
**`testpypi`** e **`pypi`**. Recomendado: no `pypi`, marque "Required reviewers"
com alguem do time, assim toda release de producao passa por um OK humano alem
do gate da rc.

> Nota: Trusted Publishing substitui os antigos secrets `PYPI_API_TOKEN` e
> `TEST_PYPI_API_TOKEN`. Eles nao sao mais usados e podem ser removidos.

---

## Como testar a partir do TestPyPI

O `--extra-index-url` aponta para o PyPI de producao, de onde vem tanto as deps
pesadas (pandas, etc.) quanto `msgram-core`/`msgram-parser`, caso a versao que a
CLI pede ja esteja em producao:

```bash
uv venv --python 3.10 .venv
uv pip install --python .venv/bin/python \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  "msgram==3.3.1rc1"

.venv/bin/msgram --help
```

> Atencao: se a CLI rc depende de uma versao de `msgram-core`/`msgram-parser`
> que **so existe como rc no TestPyPI** (ainda nao em producao), o `pip` pode nao
> resolver com o comando acima. Nesse caso, ou (a) teste a CLI apontando o pin
> para uma versao de core/parser ja publicada em producao, ou (b) instale as rc
> de core/parser manualmente do TestPyPI antes. O caminho limpo e sempre:
> **publicar core e parser em producao primeiro**, depois lancar a CLI.

(Com `pip` puro: `pip install --index-url ... --extra-index-url ... msgram==3.3.1rc1`.)

---

## Ordem de publicacao entre os pacotes do MeasureSoftGram

O ecossistema tem tres pacotes com dependencia entre eles:

```
msgram (CLI)  ->  depende de  ->  msgram-core  +  msgram-parser
```

`msgram` (este repo) e o **ultimo** da fila. Ordem ao subir versoes novas em
producao:

1. **msgram-core** e **msgram-parser** (publicar e confirmar em producao)
2. atualizar os pins `msgram-core~=...` / `msgram-parser~=...` no `pyproject.toml`
   desta CLI, se as versoes mudaram
3. so entao, **msgram** (esta CLI)

Motivo: quando a CLI for publicada, o PyPI precisa ja ter as versoes novas de
core e parser disponiveis para resolver as dependencias.

---

## Versionamento

- Segue [PEP 440](https://peps.python.org/pep-0440/). Release candidate e
  `X.Y.ZrcN` (ex: `3.3.1rc1`), final e `X.Y.Z`.
- Cada versao so pode ser publicada **uma vez** em cada indice. Para republicar,
  suba o numero (nao da para sobrescrever no PyPI nem no TestPyPI).
- A tag git sempre tem o prefixo `v` (`v3.3.1rc1`, `v3.3.1`).

---

## Troubleshooting

| Sintoma | Causa provavel / solucao |
|---|---|
| `403 ... isn't allowed to upload to project` | Trusted publisher nao configurado ou com campo divergente (owner/repo/workflow/environment). Confira a secao de pre-requisitos. |
| `400 File already exists` | Essa versao ja foi publicada nesse indice. Suba o numero da versao. |
| Job de producao falhou no "Gate" | Nao existe rc da mesma versao no TestPyPI. Publique e teste a `vX.Y.ZrcN` primeiro. |
| `Tag ... difere da versao em pyproject.toml` | A tag e a `version` do `pyproject.toml` precisam ser iguais. Ajuste e re-tague. |
| CLI instala mas puxa core/parser antigos | Atualize os pins `msgram-core~=...`/`msgram-parser~=...` no `pyproject.toml` e republique. |
| `pip` nao resolve core/parser ao instalar a rc do TestPyPI | As versoes pedidas ainda nao estao em producao. Publique core/parser primeiro (ver "Ordem de publicacao"). |

---

## Referencias

- Trusted Publishing (PyPI): <https://docs.pypi.org/trusted-publishers/>
- Action oficial: <https://github.com/pypa/gh-action-pypi-publish>
- Workflow deste repo: `.github/workflows/python-publish.yml`
