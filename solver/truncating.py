from .codex import codex, prompt
from .errors import InvalidIdentifierError
from .preparation import prepare


def truncate_code(code: str, identifier: str) -> str:
    """Extract the code that relates to the identifier.

    Identifier is usually a function/method name.

    Args:
        code(str): content of a file with code
        identifier(str): identifier name (usually a method or function)

    Returns:
        The part of the code with the declaration and the definition of
        the method/function. If the identifier is not a
        method/function, then some code related to that identifier.
    """
    if identifier not in code:
        raise InvalidIdentifierError("Invalid identifier")
    prompt_ = prompt("truncate_code.txt", code=code, identifier=identifier)
    truncated = codex(prompt_, temperature=0, stop="```", max_tokens=1500)
    if truncated.strip() == "":
        raise InvalidIdentifierError("Invalid identifier")
    return prepare(truncated)
