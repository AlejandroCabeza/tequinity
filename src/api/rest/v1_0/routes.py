# Python Imports
# Third-Party Imports
from aiohttp import web
# Project Imports
from src.api.rest.v1_0.views import FilesView, upload_files


routes: tuple = (
    web.put("/files/", upload_files),
    web.view("/files/{path:.*}", FilesView)
    # For the sake of time and sanity let's assume '.*' is a valid REGEX to parse file paths.
)
