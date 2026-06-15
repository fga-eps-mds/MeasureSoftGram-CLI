# Publicacao do pacote `msgram` (CLI)

Guia de como empacotar e publicar este repositorio no PyPI. Escrito para os
proximos grupos: leia inteiro antes da primeira release.

Pacote no PyPI: **`msgram`** (a CLI, comando `msgram` no terminal).
Depende de **`msgram-core`** e **`msgram-parser`**, entao tem cuidados extras de
ordem (ver "Ordem de publicacao").

---

## TL;DR

A publicacao e automatica via GitHub Actions e **Trusted Publishing (OIDC)**:
nao existe token nem secret no repositorio. Tudo acontece no **PyPI de producao**,
disparado por **tag git**. O "teste antes do final" e feito com **release
candidate (pre-release)**, que o `pip` normal ignora.

| Tag que voce cria         | O que publica                  | Quem instala                          |
|---------------------------|--------------------------------|---------------------------------------|
| `vX.Y.ZrcN` (`v3.3.1rc1`) | pre-release no PyPI            | so quem pedir: `pip install --pre` ou `==3.3.1rc1` |
| `vX.Y.Z` (`v3.3.1`)       | versao final no PyPI          | todo mundo: `pip install msgram`      |

**Trava de seguranca:** a tag final (`vX.Y.Z`) so publica se ja existir uma
release candidate (`vX.Y.ZrcN`) da mesma versao no PyPI. Sem rc, o job falha. E
impossivel publicar a final sem ter testado a rc antes.

### Por que pre-release em vez de TestPyPI?

Pre-release na producao e o que numpy, pandas, Django, pip e o proprio CPython
fazem a cada release: a rc fica publicada, mas o `pip install` normal **nao a
pega** (PEP 440 ignora pre-releases por padrao). Quem quer testar pede de
proposito com `--pre`. O TestPyPI serve pra testar o *processo de publicacao*
(pipeline/build), nao pra distribuir software pra alguem usar, e e um sandbox
volatil. Por isso o ciclo de release vive na producao.

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

1. **Bump da versao para a rc.** Em `pyproject.toml`:
   ```toml
   version = "3.3.1rc1"
   ```
   A versao do `pyproject.toml` tem que bater EXATAMENTE com a tag, senao o CI
   falha de proposito (step "Validar tag == versao do pyproject").
2. **Commit + tag da rc:**
   ```bash
   git commit -am "chore: bump 3.3.1rc1"
   git tag v3.3.1rc1
   git push origin main --tags
   ```
   O push da tag dispara o workflow, que publica a rc como pre-release no PyPI.
3. **Teste a rc** (secao abaixo). Rode `msgram --help` e um fluxo real
   (`extract`, `calculate`).
4. **Se estiver tudo certo, prepare a final.** No `pyproject.toml`:
   ```toml
   version = "3.3.1"
   ```
5. **Commit + tag final:**
   ```bash
   git commit -am "chore: release 3.3.1"
   git tag v3.3.1
   git push origin main --tags
   ```
   O workflow roda o **gate** (confere que `3.3.1rcN` existe no PyPI) e, se
   passar, publica a versao final.

Achou um problema na rc? Corrija, suba a versao da rc (`3.3.1rc2`) e repita do
passo 1. So promova para final quando a rc estiver boa.

> **Deu ruim numa rc ja publicada?** Use **yank** na pagina do projeto
> (Manage > Releases > Options > Yank): a versao para de ser instalada (o `pip`
> ignora), sem afetar quem ja tinha pinado. Evite **deletar**, porque o numero
> da versao fica queimado (nao da pra reusar).

---

## Pre-requisitos: configurar o Trusted Publisher (uma vez por projeto)

> Onde este workflow roda de verdade: a producao sai do repositorio que e dono
> do projeto no PyPI. No fluxo da FGA, o trabalho do semestre acontece no fork
> (`2026.1-...`) e e integrado por merge no repositorio upstream
> (`MeasureSoftGram-CLI`), de onde a release sai. Configure o trusted publisher
> apontando para o repositorio de onde a tag de release sera criada.

Quem tiver acesso de **owner** do projeto no PyPI registra o publisher confiavel
em <https://pypi.org/manage/project/msgram/settings/publishing/>, aba GitHub:

| Campo               | Valor                                          |
|---------------------|------------------------------------------------|
| Owner               | `fga-eps-mds`                                  |
| Repository name     | repo de onde sai a release (ex: `MeasureSoftGram-CLI`) |
| Workflow filename   | `python-publish.yml`                          |
| Environment name    | `pypi`                                         |

E crie o environment **`pypi`** nesse repo (GitHub > Settings > Environments).
Opcional mas recomendado: marque "Required reviewers" no `pypi` pra exigir um OK
humano antes de cada publicacao.

> Trusted Publishing substitui os antigos secrets `PYPI_API_TOKEN` e
> `TEST_PYPI_API_TOKEN`. Eles nao sao mais usados e podem ser removidos.

---

## Como testar a rc

O caminho limpo e testar a CLI **depois** que core e parser ja estao em producao
(final ou rc). Para puxar pre-releases das dependencias tambem, use `--pre`:

```bash
uv venv --python 3.10 .venv
uv pip install --python .venv/bin/python --prerelease=allow "msgram==3.3.1rc1"
.venv/bin/msgram --help
```

(Com `pip` puro: `pip install --pre "msgram==3.3.1rc1"`.)

Tudo vem do PyPI de producao, sem `--extra-index-url`.

---

## Ordem de publicacao entre os pacotes do MeasureSoftGram

```
msgram (CLI)  ->  depende de  ->  msgram-core  +  msgram-parser
```

`msgram` (este repo) e o **ultimo** da fila. Ordem ao subir versoes novas:

1. **msgram-core** e **msgram-parser** (publicar e confirmar no PyPI)
2. atualizar os pins `msgram-core~=...` / `msgram-parser~=...` no `pyproject.toml`
   desta CLI, se as versoes mudaram
3. so entao, **msgram** (esta CLI)

Motivo: quando a CLI for publicada, o PyPI precisa ja ter as versoes novas de
core e parser disponiveis para resolver as dependencias.

---

## Versionamento

- Segue [PEP 440](https://peps.python.org/pep-0440/). Release candidate e
  `X.Y.ZrcN` (ex: `3.3.1rc1`), final e `X.Y.Z`.
- Cada versao so pode ser publicada **uma vez**. Para republicar, suba o numero
  (nao da para sobrescrever no PyPI).
- A tag git sempre tem o prefixo `v` (`v3.3.1rc1`, `v3.3.1`).

---

## Troubleshooting

| Sintoma | Causa provavel / solucao |
|---|---|
| `403 ... isn't allowed to upload to project` | Trusted publisher nao configurado ou com campo divergente (owner/repo/workflow/environment). Confira os pre-requisitos. |
| `400 File already exists` | Essa versao ja foi publicada. Suba o numero da versao. |
| Job da versao final falhou no "Gate" | Nao existe rc da mesma versao no PyPI. Publique e teste a `vX.Y.ZrcN` primeiro. |
| `Tag ... difere da versao em pyproject.toml` | A tag e a `version` do `pyproject.toml` precisam ser iguais. Ajuste e re-tague. |
| CLI instala mas puxa core/parser antigos | Atualize os pins `msgram-core~=...`/`msgram-parser~=...` no `pyproject.toml` e republique. |
| `pip install` nao acha a rc | Pre-release nao vem por padrao. Use `--pre` ou pin exato (`==3.3.1rc1`). |

---

## TestPyPI (opcional, so para testar o pipeline)

Se um dia precisar testar mudancas no proprio processo de publicacao sem mexer na
producao, da pra usar o TestPyPI manualmente. Atencao: os nomes oficiais no
TestPyPI estao presos numa conta antiga sem acesso, entao la so da pra publicar
com nomes sufixados (ex: `msgram-test`). Nao faz parte do fluxo de release.

---

## Referencias

- Trusted Publishing (PyPI): <https://docs.pypi.org/trusted-publishers/>
- Pre-releases (PEP 440): <https://peps.python.org/pep-0440/#pre-releases>
- Action oficial: <https://github.com/pypa/gh-action-pypi-publish>
- Workflow deste repo: `.github/workflows/python-publish.yml`
