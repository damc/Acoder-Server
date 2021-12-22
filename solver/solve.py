from copy import deepcopy
from typing import List, Optional

from .codex import codex, prompt
from .preparation import prepare
from .safety import sanitize_code
from .task import Task, Place, Change
from .extracting import extract_code


def solve(task: Task, user_id: Optional[str] = None) -> List[Place]:
    truncated_task = divide_places_in_task(task)
    changes = []
    for key, place in enumerate(truncated_task.places_to_change):
        new_code = generate_code(truncated_task, changes, place, user_id)
        changes.append(Change(place, new_code))
    apply_changes(task, changes)
    return task.places_to_change


def divide_places_in_task(task: Task) -> Task:
    new_task = deepcopy(task)
    new_task.places_to_look = divide_places_in_list(task.places_to_look)
    new_task.places_to_change = divide_places_in_list(task.places_to_change)
    return new_task


def divide_places_in_list(places: List[Place]) -> List[Place]:
    new_places = []
    for place in places:
        if not place.identifiers:
            new_places.append(deepcopy(place))
            continue
        for identifier in place.identifiers:
            truncated_code = extract_code(
                place.file_path,
                place.code,
                identifier
            )
            new_place = Place(place.file_path, [identifier], truncated_code)
            new_places.append(new_place)
    return new_places


def generate_code(
        task: Task,
        changes: List[Change],
        place: Place,
        user_id: Optional[str]
):
    prompt_ = prompt(
        "main.txt",
        task=task,
        changes=changes,
        current_place=place,
        replace_stop=replace_stop
    )
    new_code = codex(
        prompt_,
        temperature=0.1,
        stop="```",
        user=user_id
    )
    new_code = prepare(new_code)
    new_code = sanitize_code(place.code, new_code)
    return new_code


def replace_stop(code: str) -> str:
    return code.replace('```', '<three_`>')


def apply_changes(task: Task, changes: List[Change]):
    for change in changes:
        for place_to_change in task.places_to_change:
            if change.place.file_path == place_to_change.file_path:
                place_to_change.code = place_to_change.code.replace(
                    change.place.code,
                    change.new_code
                )
