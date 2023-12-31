from dataclasses import dataclass
from json import loads
from typing import Dict, List, Optional


@dataclass
class Place:
    file_path: str
    identifiers: Optional[List[str]]
    code: Optional[str]


@dataclass
class Task:
    description: str
    places_to_change: List[Place]
    places_to_look: List[Place]
    test_commands: List[str]


def dict_to_task(task_dict: Dict) -> Task:
    task_dict['places_to_change'] = [
        Place(**place_dict)
        for place_dict in task_dict['places_to_change']
    ]
    task_dict['places_to_look'] = [
        Place(**place_dict)
        for place_dict in task_dict['places_to_look']
    ]
    task = Task(**task_dict)
    return task


def json_to_task(json: str) -> Task:
    task_dict = loads(json)
    return dict_to_task(task_dict)


@dataclass(eq=False)
class Change:
    place: Place
    new_code: str
