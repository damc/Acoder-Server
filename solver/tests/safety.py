from os import listdir
from pytest import mark

from solver.safety import is_code, sanitize_code


@mark.parametrize('file_name', listdir('solver/tests/is_code/code'))
def test_is_code_code(file_name):
    with open(f'solver/tests/is_code/code/{file_name}') as f:
        assert is_code(f.read())


@mark.parametrize('file_name', listdir('solver/tests/is_code/plain'))
def test_is_code_plain(file_name):
    with open(f'solver/tests/is_code/plain/{file_name}') as f:
        assert not is_code(f.read())


def test_sanitize_code():
    with open(f'solver/tests/sanitize_code/old.txt') as f:
        old = f.read()
    with open(f'solver/tests/sanitize_code/new.txt') as f:
        new = f.read()
    with open(f'solver/tests/sanitize_code/result.txt') as f:
        expected_result = f.read()
    assert sanitize_code(old, new) == expected_result
