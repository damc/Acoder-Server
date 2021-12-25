from typing import Optional

from .codex import codex, prompt


def answer(question: str, user_id: Optional[str] = None) -> str:
    prompt_ = prompt("question.txt", question=question)
    return codex(prompt_, temperature=0.1, stop='"""', user=user_id).strip()
