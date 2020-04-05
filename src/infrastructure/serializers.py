# Python Imports
from typing import List
# Third-Party Imports
# Project Imports


class JsonSerializer:

    def to_dict(self) -> dict:
        raise NotImplementedError


class CreateOrUpdateFilesJsonSerializer(JsonSerializer):

    def __init__(self):
        self._created_files: List[str] = list()
        self._updated_files: List[str] = list()
        self._error_files: List[str] = list()

    def _get_created_or_updated_file_list(self, was_updated: bool):
        return self._updated_files if was_updated else self._created_files

    def add_result(self, file_name: str, was_updated: bool):
        self._get_created_or_updated_file_list(was_updated).append(file_name)

    def add_error(self, file_name):
        self._error_files.append(file_name)

    def to_dict(self) -> dict:
        return {
            "created_files": self._created_files,
            "updated_files": self._updated_files,
            "error_files": self._error_files,
        }


class ProcessOutputJsonSerializer(JsonSerializer):

    DEFAULT_STD_DECODE_FORMAT: str = "utf-8"

    def __init__(self, return_code: int, stdout: bytes, stderr: bytes):
        self.return_code: int = return_code
        self._stdout: bytes = stdout
        self._stderr: bytes = stderr

    @property
    def stdout(self):
        return self._stdout.decode(self.DEFAULT_STD_DECODE_FORMAT)

    @property
    def stderr(self):
        return self._stderr.decode(self.DEFAULT_STD_DECODE_FORMAT)

    def to_dict(self) -> dict:
        return {
            "return_code": self.return_code,
            "stdout": self.stdout,
            "stderr": self.stderr
        }
