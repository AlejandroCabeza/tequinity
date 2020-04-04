# Python Imports
from typing import List
# Third-Party Imports
# Project Imports


class JsonSerializer:

    def to_dict(self) -> dict:
        raise NotImplementedError


class ExecuteFileJsonSerializer(JsonSerializer):

    def __init__(self, return_code: int = -1):
        self.return_code: int = return_code

    def to_dict(self) -> dict:
        return {
            "return_code": self.return_code,
        }


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
