from pytest import mark
from os import listdir
from typing import List, Tuple


from solver.truncating import truncate_code


TEST_TRUNCATE_CODE_PATH = 'solver/tests/truncate_code'


def truncate_code_data_provider() -> List[Tuple[str, str, str]]:
    directories = listdir(TEST_TRUNCATE_CODE_PATH)
    data = []
    for directory in directories:
        file_path = f'{TEST_TRUNCATE_CODE_PATH}/{directory}/code.txt'
        code = open(file_path).read()
        file_path = f'{TEST_TRUNCATE_CODE_PATH}/{directory}/identifier.txt'
        identifier = open(file_path).read()
        file_path = f'{TEST_TRUNCATE_CODE_PATH}/{directory}/expected.txt'
        expected = open(file_path).read()
        data.append((code, identifier, expected))
    return data


@mark.parametrize(
    "code, identifier, expected",
    truncate_code_data_provider(),
)
def test_truncate_code(code: str, identifier: str, expected: str):
    assert truncate_code(code, identifier) == expected
