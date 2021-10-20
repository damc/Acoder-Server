from dataclasses import dataclass
from json import loads
from typing import List, Optional


@dataclass(eq=False)
class Place:
    file_path: str
    functions: Optional[List[str]]
    code: Optional[str]


@dataclass(eq=False)
class Task:
    title: str
    description: str
    places_to_change: List[Place]
    places_to_look: List[Place]


def dict_to_task(task_dict: dict) -> Task:
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