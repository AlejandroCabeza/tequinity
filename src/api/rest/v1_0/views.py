# Python Imports
# Third-Party Imports
from pathlib import Path
from aiohttp import MultipartReader
from aiohttp.abc import StreamResponse
from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import View
from aiohttp.web_response import json_response
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_exceptions import HTTPNotFound, HTTPNoContent, HTTPBadRequest, HTTPUnsupportedMediaType
# Project Imports
from src.files.file_operations import (
    get_absolute_file_path_to_db,
    execute_file,
    parse_files_from_multipart
)
from src.code_runners.exceptions import CodeRunnerNotAvailable
from src.api.rest.v1_0.serializers import JsonSerializer
from src.api.decorators import (
    inject_path_parameter_from_url_path,
    inject_run_detached_parameter_from_query_string
)


async def upload_files(request: Request) -> StreamResponse:
    """
    Create or update file in the server.
    :param request: AioHttp Request object
    :return: Http Response with the appropriate status code
    """
    try:
        multipart_reader: MultipartReader = await request.multipart()
        serializer: JsonSerializer = await parse_files_from_multipart(multipart_reader)
        return json_response(serializer.to_dict())
    except KeyError:
        return HTTPBadRequest()


class FilesView(View):

    @inject_path_parameter_from_url_path
    async def get(self, path: str) -> StreamResponse:
        """
        Retrieve a file from the server.
        :param path: Filename relative to the file DB root.
        :return: Http Response with the appropriate status code
        """
        absolute_file_path: Path = get_absolute_file_path_to_db(path)
        print(absolute_file_path)
        if absolute_file_path.is_file():
            return FileResponse(absolute_file_path)
        else:
            return HTTPNotFound()

    @inject_path_parameter_from_url_path
    async def delete(self, path: str) -> StreamResponse:
        """
        Delete a file from the server.
        :param path: Filename relative to the file DB root.
        :return: Http Response with the appropriate status code
        """
        absolute_file_path: Path = get_absolute_file_path_to_db(path)
        try:
            absolute_file_path.unlink()
            return HTTPNoContent()
        except FileNotFoundError:
            return HTTPNotFound()

    @inject_path_parameter_from_url_path
    @inject_run_detached_parameter_from_query_string
    async def post(self, path: str, run_detached: bool) -> StreamResponse:
        """
        Execute a file in the server with a CodeRunner
        Even though POST is usually used to create an element in a category, for this use case I thought it was cleaner
        to use it for execution alone.
        :param path: Filename relative to the file DB root.
        :param run_detached: Execute the script asynchronously or not.
        :return: Http Response with the appropriate status code
        """
        absolute_file_path = get_absolute_file_path_to_db(path)
        try:
            serializer: JsonSerializer = await execute_file(absolute_file_path, run_detached)
            return json_response(serializer.to_dict(), status=200)
        except FileNotFoundError:
            return HTTPNotFound()
        except CodeRunnerNotAvailable:
            return HTTPUnsupportedMediaType()
