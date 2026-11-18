"""Grupos de pesos do msgram.json.

Um grupo é o conjunto de entidades irmãs (mesmo pai) cujos pesos somam 100:
as características, as subcaracterísticas de cada característica e as medidas
de cada subcaracterística. Os grupos são sempre lidos do arquivo no momento
da execução, na ordem em que aparecem nele.
"""

import copy
from dataclasses import dataclass
from math import comb
from typing import Dict, List

LEVEL_LABELS = {
    "characteristics": "Características",
    "subcharacteristics": "subcaracterísticas",
    "measures": "medidas",
}


class InvalidGroupPath(ValueError):
    def __init__(self, path: str, valid_paths: List[str]):
        self.path = path
        self.valid_paths = valid_paths
        super().__init__(f"Grupo inexistente: {path}")


@dataclass(frozen=True)
class WeightGroup:
    path: str
    label: str
    entities: List[str]
    weights: Dict[str, int]

    @property
    def comparisons(self) -> int:
        return comb(len(self.entities), 2)


def _group(parents: List[str], level: str, items: list) -> WeightGroup:
    if parents:
        label = " › ".join(parents + [LEVEL_LABELS[level]])
    else:
        label = LEVEL_LABELS[level]
    return WeightGroup(
        path="/".join(parents + [level]),
        label=label,
        entities=[item["key"] for item in items],
        weights={item["key"]: item.get("weight") for item in items},
    )


def _walk(config: dict):
    """Percorre o config devolvendo (pais, nível, itens) de cada grupo, em pré-ordem."""
    characteristics = config.get("characteristics", [])
    yield [], "characteristics", characteristics
    for char in characteristics:
        subchars = char.get("subcharacteristics", [])
        yield [char["key"]], "subcharacteristics", subchars
        for sub in subchars:
            yield [char["key"], sub["key"]], "measures", sub.get("measures", [])


def list_groups(config: dict) -> List[WeightGroup]:
    return [_group(parents, level, items) for parents, level, items in _walk(config)]


def find_group(groups: List[WeightGroup], path: str) -> WeightGroup:
    for group in groups:
        if group.path == path:
            return group
    raise InvalidGroupPath(path, [g.path for g in groups])


def apply_weights(config: dict, new_weights: Dict[str, Dict[str, int]]) -> dict:
    """Devolve uma cópia do config com só o campo weight alterado nos grupos informados."""
    result = copy.deepcopy(config)
    groups_by_path = {}
    for parents, level, items in _walk(result):
        groups_by_path["/".join(parents + [level])] = items

    for path, weights in new_weights.items():
        if path not in groups_by_path:
            raise InvalidGroupPath(path, list(groups_by_path))
        items = groups_by_path[path]
        keys = {item["key"] for item in items}
        unknown = set(weights) - keys
        if unknown:
            raise ValueError(
                f"Entidades fora do grupo {path}: {', '.join(sorted(unknown))}"
            )
        for item in items:
            if item["key"] in weights:
                item["weight"] = weights[item["key"]]

    return result
