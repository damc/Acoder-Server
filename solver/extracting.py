from pathlib import Path
from re import search
from typing import List

from .codex import codex, prompt
from .errors import InvalidIdentifierError
from .preparation import prepare

LANGUAGE_PYTHON = 0
LANGUAGE_PHP = 1
LANGUAGE_JAVA = 2
LANGUAGE_JAVASCRIPT = 3
LANGUAGE_CPP = 4
LANGUAGE_RUBY = 5
LANGUAGE_GOLANG = 6
LANGUAGE_JULIA = 7
LANGUAGE_RUST = 8
LANGUAGE_SOLIDITY = 9

FUNCTION_DECLARATION_REGEX = {
    LANGUAGE_PYTHON: r'\s*def\s+<function>\s*\(',
    LANGUAGE_PHP: r'\s*function\s+<function>\s*\(',
    LANGUAGE_JAVASCRIPT: r'\s*function\s+<function>\s*\(',
    LANGUAGE_GOLANG: r'\s*func\s+<function>\s*\('
}


def extract_code(file_path: str, code: str, identifier: str) -> str:
    """Extract the code that relates to the identifier.

    Identifier might be:
    1. Range (a string, e.g. '20-30') - in that case, it will extract
        the given lines of code.
    2. Function/method name - in that case, it will extract the
        function/method code.
    3. Other identifier - in that case, it will just tell Codex
        to extract the part of code related to that identifier.

    Args:
        file_path(str): path to the file
        code(str): content of a file with code
        identifier(str): identifier name (range or identifier name)

    Returns:
        The part of the code with the declaration and the definition of
        the method/function. If the identifier is not a
        method/function, then some code related to that identifier.
    """
    if search(r'^[0-9]+:[0-9]+$', identifier):
        return extract_code_range(code, identifier)
    if identifier not in code:
        raise InvalidIdentifierError("Invalid identifier")
    extension = Path(file_path).suffix.lower()
    if extension == '.py':
        return extract_code_python(code, identifier)
    if extension == '.php':
        return extract_code_brackets(code, identifier, LANGUAGE_PHP)
    if extension == '.js':
        return extract_code_brackets(code, identifier, LANGUAGE_JAVASCRIPT)
    if extension == '.go':
        return extract_code_brackets(code, identifier, LANGUAGE_GOLANG)
    return extract_code_with_codex(code, identifier)


def extract_code_range(code: str, identifier: str) -> str:
    lines = code.split("\n")
    start, end = [int(number) for number in identifier.split(':')]
    return "\n".join(lines[(start - 1):end])


def extract_code_python(code: str, identifier: str) -> str:
    lines = code.split("\n")
    declaration_line = find_declaration_line(code, identifier, LANGUAGE_PYTHON)
    indentation = search(r'^([ \t]*)', lines[declaration_line + 1]).group(0)
    start = function_start_python(declaration_line, indentation, lines)
    end = function_end_python(declaration_line, indentation, lines)
    return '\n'.join(lines[start:end]).rstrip()


def find_declaration_line(code: str, function: str, language: int) -> int:
    lines = code.split('\n')
    for key, line in enumerate(lines):
        regex = FUNCTION_DECLARATION_REGEX[language]
        regex = regex.replace("<function>", function)
        if search(regex, line):
            return key
    raise InvalidIdentifierError("Invalid identifier")


def function_start_python(
        declaration_line: int,
        indentation: str,
        lines: List[str]
) -> int:
    current_line = declaration_line - 1
    while (
            current_line > 0 and
            lines[current_line].startswith(indentation) and
            not whitespaces_only(lines[current_line])
    ):
        current_line -= 1
    return current_line + 1


def function_end_python(
        declaration_line: int,
        indentation: str,
        lines: List[str]
) -> int:
    current_line = declaration_line + 2
    while (
        current_line < len(lines) and (
            lines[current_line].startswith(indentation) or
            whitespaces_only(lines[current_line])
        )
    ):
        current_line += 1
    return current_line


def whitespaces_only(text: str) -> bool:
    return bool(search(r'^\s*$', text))


def extract_code_brackets(code: str, function: str, language: int) -> str:
    """Extract function for a language that uses curly brackets.

    Args:
        code(str): code
        function(str): function name
        language(int): language

    Returns:
        str: extracted code
    """
    lines = code.split("\n")
    declaration_line = find_declaration_line(code, function, language)
    start = code.find(lines[declaration_line])
    character_position = code.find("{", start) + 1
    brackets = 1
    while brackets > 0:
        if code[character_position] == "}":
            brackets -= 1
        if code[character_position] == "{":
            brackets += 1
        character_position += 1
    return code[start:character_position]


def extract_code_with_codex(code, identifier):
    prompt_ = prompt("extract_code.txt", code=code, identifier=identifier)
    truncated = codex(prompt_, temperature=0, stop="```", max_tokens=1500)
    if truncated.strip() == "":
        raise InvalidIdentifierError("Invalid identifier")
    extracted = prepare(truncated)
    return extracted
