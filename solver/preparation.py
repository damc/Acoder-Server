from typing import List


def prepare(code: str) -> str:
    code = strip_language_name(code)
    return code[1:-1]


def strip_language_name(code: str) -> str:
    for language in languages():
        if code.startswith(language) or code.lower().startswith(language):
            return code[len(language):]
    return code


def languages() -> List[str]:
    return [
        'python',
        'ruby',
        'php',
        'html',
        'xml',
        'cpp',
        'java',
        'javascript',
        'pascal',
        'julia',
        'rust'
    ]
