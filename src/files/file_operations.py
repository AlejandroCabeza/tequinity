# Python Imports
from pathlib import Path
# Third-Party Imports
from aiofile import AIOFile
from aiohttp import MultipartReader, BodyPartReader
# Project Imports
from src.files.file_verification import verify_file_pre_write, verify_file_post_write
from src.code_runners.factory import build_code_runner
from src.files.file_utils import get_absolute_file_path_to_db
from src.infrastructure.serializers import CreateOrUpdateFilesJsonSerializer, JsonSerializer


async def parse_files_from_multipart(multipart_reader: MultipartReader) -> JsonSerializer:
    create_or_update_serializer: CreateOrUpdateFilesJsonSerializer = CreateOrUpdateFilesJsonSerializer()
    while file := await multipart_reader.next():
        if await verify_file_pre_write(file.name):
            _file_name, _file_was_updated = await create_or_update_file_in_db_from_body_part_reader(file)
            if await verify_file_post_write(_file_name):
                create_or_update_serializer.add_result(_file_name, _file_was_updated)

        create_or_update_serializer.add_error(file.name)
    return create_or_update_serializer


async def create_or_update_file_in_db_from_body_part_reader(body_part_reader: BodyPartReader) -> (str, bool):
    file_name: str = body_part_reader.name
    path: Path = get_absolute_file_path_to_db(file_name)
    file_was_updated: bool = path.is_file()
    async with AIOFile(str(path.resolve()), "wb+") as async_file:
        while file_chunk := await body_part_reader.read_chunk():
            await async_file.write(file_chunk)
    return file_name, file_was_updated


async def execute_file(path: Path, run_detached: bool) -> JsonSerializer:
    if not path.is_file():
        raise FileNotFoundError
    return await build_code_runner(path).run(run_detached)
