from re import findall


CODE_THRESHOLD = 0.02


def is_code(content_: str) -> bool:
    """Check if content_ is code or plain text"""
    matches = 0
    lines = content_.splitlines()
    for line in lines:
        line = line[:120]
        matches += len(set(code_keywords()).intersection(line.split()))
        matches += sum([line.count(operator) for operator in code_operators()])
        for regex in code_regex():
            matches += len(findall(regex, line)) * 3
        for regex in text_regex():
            matches -= len(findall(regex, line)) * 2
        if line.endswith(';'):
            matches += 5
    return matches / len(content_) > CODE_THRESHOLD
