from typing import List


from .codex import codex, prompt
from .error import AcoderError
from .messages import error_messages
from .model.task import Place, Task


class UnsafeTaskError(AcoderError):
    pass


def validate_description(task: Task):
    prompt_ = prompt(
        "description_validation.txt",
        description=task.description
    )
    output = codex(prompt_, stop="Explanation", max_tokens=12).strip().lower()
    if output != "safe":
        raise UnsafeTaskError(error_messages['task_unsafe'])
