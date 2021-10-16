from difflib import unified_diff
from typing import List
from re import findall
from json import load

from .codex import codex, prompt
from .errors import UnsafeTaskError

CODE_VALIDATION_DIR = 'solver/code_validation'
CODE_THRESHOLD = 0.02


def validate_description(description: str):
    prompt_ = prompt(
        "description_validation.txt",
        description=description
    )
    output = codex(prompt_, stop="Explanation", max_tokens=12).strip().lower()
    if output != "safe":
        raise UnsafeTaskError("Task unsafe")


def sanitize_code(old: str, new: str) -> str:
    """Replace new long text that has been added with "{long_text}"

    The function will replace new additions with "{long_text}" if:
    1. The addition is longer than 100 characters,
    2. The addition is plain text, not code.

    Args:
        old: old code
        new: new code

    Returns:
        sanitized code
    """
    additions = find_additions(old, new)
    for addition in additions:
        if len(addition) > 100 and not is_code(addition):
            new = new.replace(addition, "{long_text}")
    return new


def find_additions(old: str, new: str) -> List[str]:
    """Find the text/code that has been added

    For example, if the diff is like this:
    ```
    +++ /home/damian/Projects/Acoder/Server/sorting.py

    @@ -38,3 +38,12 @@

         for i in range(len(counts)):
             result.extend([i] * counts[i])
         return result
    +
    +def heap_sort(array):
    +    heap = Heap()
    +    for element in array:
    +        heap.insert(element)
    +    sorted_array = []
    +    while not heap.is_empty():
    +        sorted_array.append(heap.delete())
    +    return sorted_array
    ```

    then there is only one addition:
    ```
    def heap_sort(array):
        heap = Heap()
        for element in array:
            heap.insert(element)
        sorted_array = []
        while not heap.is_empty():
            sorted_array.append(heap.delete())
        return sorted_array
    ```

    Args:
        old: old code
        new: new code

    Returns:
        list of additions
    """
    additions = []
    previous_line_is_addition = False
    for line in unified_diff(old.splitlines(), new.splitlines()):
        if line.startswith("+"):
            if previous_line_is_addition:
                additions[-1] += "\n" + line
            else:
                additions.append(line[1:])
        previous_line_is_addition = line.startswith("+")
    return additions


def is_code(content_: str) -> bool:
    """Check if content_ is code or plain text"""
    keywords = load_from_json("keywords.json")
    operators = load_from_json("operators.json")
    code_regex = load_from_json("code_regex.json")
    text_regex = load_from_json("text_regex.json")

    matches = 0
    lines = content_.splitlines()
    for entire_line in lines:
        line = entire_line[:120]
        words = [word.lower() for word in line.split()]
        matches += len(set(keywords).intersection(words))
        matches += sum([line.count(operator) for operator in operators])
        for regex in code_regex:
            matches += len(findall(regex, line)) * 3
        for regex in text_regex:
            matches -= len(findall(regex, entire_line)) * 2
        if line.endswith(';'):
            matches += 2
    score = matches / len(content_)
    return score > CODE_THRESHOLD


def load_from_json(file_name: str):
    with open(f'{CODE_VALIDATION_DIR}/{file_name}') as f:
        return load(f)
