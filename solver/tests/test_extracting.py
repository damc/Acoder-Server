from pytest import mark
from os import listdir
from typing import List, Tuple


from solver.extracting import extract_code


TEST_EXTRACT_CODE_PATH = 'solver/tests/extract_code'


def extract_code_data_provider() -> List[Tuple[str, str, str, str]]:
    directories = listdir(TEST_EXTRACT_CODE_PATH)
    data = []
    for directory in directories:
        directory_path = f'{TEST_EXTRACT_CODE_PATH}/{directory}'
        file_path = open(f'{directory_path}/file_path.txt').read()
        code = open(f'{directory_path}/code.txt').read()
        identifier = open(f'{directory_path}/identifier.txt').read()
        expected = open(f'{directory_path}/expected.txt').read()
        data.append((file_path, code, identifier, expected))
    return data


@mark.parametrize(
    "file_path, code, identifier, expected",
    extract_code_data_provider(),
)
def test_extract_code(
        file_path: str,
        code: str,
        identifier: str,
        expected: str
):
    assert extract_code(file_path, code, identifier) == expected
