from copy import copy
from typing import List

from .codex import codex, prompt
from .model import Task, Place
from .safety import validate_description


def solve(task: Task) -> List[Place]:
    validate_description(task)
    changes = []
    for key, place in enumerate(task.places_to_change):
        changed_place = copy(place)
        prompt_ = prompt(
            "main.txt",
            task=task,
            changes=changes,
            current_place=place,
            replace_stop=replace_stop
        )
        changed_place.code = codex(prompt_, temperature=0.1, stop="```")
        changed_place.code = changed_place.code.strip()
        changes.append(changed_place)
    return changes


def replace_stop(code: str) -> str:
    return code.replace('```', '<three_apostrophes>')
