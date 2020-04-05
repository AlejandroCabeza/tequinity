# Python Imports
import asyncio
from pathlib import Path
from abc import ABC, abstractmethod
from asyncio.subprocess import Process
# Third-Party Imports
# Project Imports
from src.infrastructure.serializers import ProcessOutputJsonSerializer, JsonSerializer


class CodeRunner(ABC):

    def __init__(self, path: Path):
        self.path: path = path

    @abstractmethod
    async def run(self):
        raise NotImplementedError


class DockerCodeRunner(CodeRunner, ABC):

    DOCKER_WORKING_DIRECTORY: str = "/runners/"


class PythonDockerCodeRunner(DockerCodeRunner):
    """
    Runs the selected script inside a safely isolated docker container.
    Using plain cmd commands because the library docker-py doesn't support Python3.8 yet.
    """
    def _create_command(self, run_detached: bool) -> str:
        return (f"docker run {'-d ' if run_detached else ''}-t "
                f"-v {str(self.path.parent.resolve())}:{self.DOCKER_WORKING_DIRECTORY} "
                f"-w {self.DOCKER_WORKING_DIRECTORY} "
                f"python:3.8 "
                f"python {self.path.name}")

    async def run(self, run_detached: bool = False) -> JsonSerializer:
        """
        :return: Return code for the executed process in the container
        """
        # return os.system(self._create_command(run_detached))
        process: Process = await asyncio.create_subprocess_shell(
            self._create_command(run_detached),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return ProcessOutputJsonSerializer(process.returncode, stdout, stderr)
