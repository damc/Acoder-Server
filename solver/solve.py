from copy import copy
from typing import List, Optional

from .codex import codex, prompt
from .task import Task, Place
from .safety import validate_description, sanitize_code


def solve(task: Task, user_id: Optional[str] = None) -> List[Place]:
    validate_description(task.description)
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
        changed_place.code = codex(
            prompt_,
            temperature=0.1,
            stop="```",
            user=user_id
        )
        changed_place.code = changed_place.code.strip()
        changed_place.code = sanitize_code(place.code, changed_place.code)
        changes.append(changed_place)
    return changes


def replace_stop(code: str) -> str:
    return code.replace('```', '<three_apostrophes>')
