"""msgram weights: define os pesos do msgram.json por comparação par a par (AHP).

O cálculo (prioridades e CR) vem do módulo core.ahp, que usa a AHPy. Este
comando só faz as perguntas, mostra o resumo e grava o campo weight depois
da confirmação. Nenhum arquivo novo é criado.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

from core.ahp import (
    CR_THRESHOLD,
    SAATY_PHRASES,
    calculate_group,
    most_inconsistent,
    pairs,
)
from rich.prompt import Prompt
from rich.text import Text

from src.cli.resources.weight_groups import (
    InvalidGroupPath,
    apply_weights,
    find_group,
    list_groups,
)
from src.cli.utils import console, print_error, print_info, print_output, print_rule
from src.config.settings import FILE_CONFIG

INTENSITIES = ["moderadamente", "fortemente", "muito_fortemente", "extremamente"]
INTENSITY_OPTIONS = (
    "[1] moderadamente  [2] fortemente  [3] muito fortemente  [4] extremamente"
)


class Cancelled(Exception):
    pass


class PromptPT(Prompt):
    illegal_choice_message = "[prompt.invalid.choice]Escolha uma das opções mostradas"


# ------------------------------------------------------------------ entrada


def ask_choice(prompt: str, choices, default=None) -> str:
    """Pergunta no terminal e devolve uma das opções. Isolada para os testes."""
    try:
        return PromptPT.ask(
            Text(prompt),
            choices=list(choices),
            default=default,
            show_choices=False,
            show_default=False,
            console=console,
        )
    except EOFError:
        # sem terminal (stdin fechado, CI, pipe): trata como cancelamento
        raise Cancelled()


def ask_pair(a: str, b: str):
    which = ask_choice(
        f"  Qual é mais importante? [1] {a}  [2] {b}  [3] igualmente", ["1", "2", "3"]
    )
    if which == "3":
        return (a, b, None, "igual")
    preferred = a if which == "1" else b
    how = ask_choice(
        f"  Quanto mais importante? {INTENSITY_OPTIONS}", ["1", "2", "3", "4"]
    )
    return (a, b, preferred, INTENSITIES[int(how) - 1])


# ------------------------------------------------------------------ formatação


def format_cr(cr) -> str:
    return f"{cr:.2f}".replace(".", ",")


def describe_answer(answer) -> str:
    a, b, preferred, intensity = answer
    if preferred is None:
        return f"{a} × {b}: igualmente importantes"
    return f"{a} × {b}: {preferred} é {SAATY_PHRASES[intensity]}"


def describe_suggestion(answer) -> str:
    _, _, preferred, intensity = answer
    if preferred is None:
        return "igualmente importantes"
    return f"{preferred} é {SAATY_PHRASES[intensity]}"


def describe_cr(result) -> str:
    if result.consistency_ratio is None:
        return "CR não se aplica"
    if result.consistent:
        return f"CR {format_cr(result.consistency_ratio)}"
    limit = format_cr(CR_THRESHOLD)
    return f"⚠ CR {format_cr(result.consistency_ratio)}, acima de {limit}, aceito"


# ------------------------------------------------------------------ grupos


def ask_group(group, title: str):
    """Faz as perguntas de um grupo até o usuário ter um resultado consistente ou aceitar."""
    group_pairs = pairs(group.entities)
    n = len(group_pairs)
    while True:
        console.line()
        plural = "comparação" if n == 1 else "comparações"
        print_output(f"[{title}] {group.label} ({n} {plural})", "accent")
        answers = []
        for i, (a, b) in enumerate(group_pairs, start=1):
            print_output(f"({i}/{n}) {a} × {b}")
            answers.append(ask_pair(a, b))

        result = calculate_group(group.entities, answers)

        if result.consistency_ratio is None:
            print_output(
                f"  Consistência: não se aplica ({len(group.entities)} entidades)",
                "muted",
            )
            return answers, result
        if result.consistent:
            print_output(
                f"  ✔ Consistência: CR = {format_cr(result.consistency_ratio)}",
                "success",
            )
            return answers, result

        print_output(
            f"  ⚠ Consistência: CR = {format_cr(result.consistency_ratio)} "
            f"(acima de {format_cr(CR_THRESHOLD)})",
            "warning",
        )
        print_output("    Suas respostas se contradizem.", "warning")
        conflict = most_inconsistent(group.entities, answers, result)
        if conflict:
            print_output(
                f"    Conflito mais provável: {conflict.a} × {conflict.b}. "
                f"Sugestão: {describe_suggestion(conflict.suggested)}",
                "warning",
            )
        if (
            ask_choice("    [1] refazer o grupo  [2] aceitar mesmo assim", ["1", "2"])
            == "2"
        ):
            return answers, result


def print_summary(entries, partial: bool):
    console.line()
    print_rule("Resumo")
    for group, answers, result in entries:
        print_output(f"{group.label} ({describe_cr(result)})", "accent")
        for answer in answers:
            print_output(f"  {describe_answer(answer)}")
        print_output(f"{'':33}antes → depois", "muted")
        for entity in group.entities:
            before = group.weights.get(entity)
            before = "-" if before is None else before
            print_output(f"  {entity:<30} {before:>3} → {result.weights[entity]}")
        console.line()
    if partial:
        print_info("Os demais grupos não foram alterados.")


# ------------------------------------------------------------------ arquivo


def save_config(file_path: Path, config: dict):
    """Grava num arquivo temporário e renomeia: uma falha no meio não corrompe o msgram.json."""
    fd, tmp = tempfile.mkstemp(dir=file_path.parent, prefix=".msgram-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(json.dumps(config, indent=4))
        os.replace(tmp, file_path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def display_path(file_path: Path) -> str:
    try:
        return os.path.relpath(file_path)
    except ValueError:
        return str(file_path)


# ------------------------------------------------------------------ comando


def load_config(file_path: Path, shown_path: str) -> dict:
    """Lê o msgram.json ou encerra com a orientação do Cenário 6."""
    if not file_path.exists():
        print_error(f"Nenhum arquivo de configuração encontrado em {shown_path}")
        print_output("  Execute o comando msgram init")
        sys.exit(1)
    try:
        return json.loads(file_path.read_text())
    except json.JSONDecodeError as e:
        print_error(f"O arquivo {shown_path} não é um JSON válido: {e}")
        sys.exit(1)


def select_groups(config: dict, group_path):
    """Todos os grupos do arquivo ou só o informado em --group."""
    groups = list_groups(config)
    if not group_path:
        return groups
    try:
        return [find_group(groups, group_path)]
    except InvalidGroupPath as e:
        print_error(f"Grupo inexistente: {e.path}")
        print_output("  Caminhos válidos:")
        for path in e.valid_paths:
            print_output(f"    {path}")
        sys.exit(1)


def print_header(groups):
    to_ask = [g for g in groups if len(g.entities) > 1]
    singles = len(groups) - len(to_ask)
    total = sum(g.comparisons for g in groups)
    print_output("Definição de pesos por comparação")
    print_output(
        f"{len(groups)} grupos no modelo · {total} comparações · "
        f"{singles} grupos com uma entidade (peso 100, sem perguntas)",
        "muted",
    )


def confirm_save(shown_path: str) -> bool:
    try:
        answer = ask_choice(
            f"Gravar os novos pesos em {shown_path}? [s/N]", ["s", "n"], default="n"
        )
    except (KeyboardInterrupt, Cancelled):
        return False
    return answer == "s"


def command_weights(args):
    group_path = args.get("group")
    file_path = Path(args["config_path"]) / FILE_CONFIG
    shown_path = display_path(file_path)

    config = load_config(file_path, shown_path)
    groups = select_groups(config, group_path)

    print_rule("MSGram")
    if not group_path:
        print_header(groups)

    try:
        entries = run_groups(groups, single_group=bool(group_path))
    except (KeyboardInterrupt, Cancelled):
        console.line()
        print_output(f"Cancelado. {shown_path} não foi alterado.", "warning")
        sys.exit(130)

    changed = [(g, a, r) for g, a, r in entries if a or g.weights != r.weights]
    if not changed:
        console.line()
        print_info("Nenhum peso a alterar.")
        return

    print_summary(changed, partial=bool(group_path))

    if not confirm_save(shown_path):
        print_output(f"Pesos não gravados. {shown_path} não foi alterado.", "warning")
        return

    save_config(
        file_path, apply_weights(config, {g.path: r.weights for g, _, r in changed})
    )
    print_output(f"✔ Pesos gravados em {shown_path}.", "success")


def run_groups(groups, single_group: bool):
    """Pergunta cada grupo e devolve (grupo, respostas, resultado)."""
    entries = []
    to_ask = [g for g in groups if len(g.entities) > 1]
    position = 0
    for group in groups:
        if len(group.entities) <= 1:
            # Cenário 3: sem perguntas, peso 100
            entries.append((group, [], calculate_group(group.entities, [])))
            if single_group:
                print_output(
                    f"{group.label}: uma entidade, peso 100 sem perguntas", "muted"
                )
            continue
        position += 1
        title = "Grupo" if single_group else f"Grupo {position}/{len(to_ask)}"
        answers, result = ask_group(group, title)
        entries.append((group, answers, result))
    return entries
