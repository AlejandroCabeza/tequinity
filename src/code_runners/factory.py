# Python Imports
from pathlib import Path
# Third-Party Imports
# Project Imports
from src.files.file_tagging import get_accepted_code_file_tags_from_filename
from src.framework.settings import PYTHON_FILE_TAG
from src.code_runners.exceptions import CodeRunnerNotAvailable
from src.code_runners.code_runner import PythonDockerCodeRunner, CodeRunner

_CODE_RUNNERS = {
    PYTHON_FILE_TAG: PythonDockerCodeRunner
}


def build_code_runner(path: Path):
    """
    Builds a code runner that can run the specified file according to its extension.
    :return The first code runner that matches the file.
    :raise StopIteration if there is no match.
    """
    file_code_tags = get_accepted_code_file_tags_from_filename(path)
    for file_code_tag in file_code_tags:
        try:
            code_runner: type(CodeRunner) = next(
                code_runner for code_tag, code_runner
                in _CODE_RUNNERS.items()
                if code_tag in file_code_tag
            )
            return code_runner(path)
        except StopIteration:
            raise CodeRunnerNotAvailable
