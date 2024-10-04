from flask import Request
from pathlib import Path
from tempfile import gettempdir
from typing import Final
from werkzeug.datastructures import FileStorage

from .env_pomes import APP_PREFIX, env_get_path

TEMP_FOLDER: Final[Path] = env_get_path(key=f"{APP_PREFIX}_TEMP_FOLDER",
                                        def_value=Path(gettempdir()))


def file_from_request(request: Request,
                      file_name: str = None,
                      file_seq: int = 0) -> bytes:
    """
    Retrieve and return the contents of the file returned in the response to a request.

    The file may be referred to by its name (*file_name*), or if no name is specified,
    by its sequence number (*file_seq*).

    :param request: the request
    :param file_name: optional name for the file
    :param file_seq: sequence number for the file, defaults to the first file
    :return: the contents retrieved from the file
    """
    # inicialize the return variable
    result: bytes | None = None

    count: int = len(request.files) \
                 if hasattr(request, "files") and request.files else 0
    # has a file been found ?
    if count > 0:
        # yes, retrieve it
        file: FileStorage | None = None
        if isinstance(file_name, str):
            file = request.files.get(file_name)
        elif (isinstance(file_seq, int) and
              len(request.files) > file_seq >= 0):
            file_in: str = list(request.files)[file_seq]
            file = request.files[file_in]

        if file:
            result: bytes = file.stream.read()

    return result


def file_get_data(file_data: Path | str | bytes) -> bytes:
    """
    Retrieve the data in *file_data* (type *bytes*), or in a file in path *file_data* (type *Path* or *str*).

    :param file_data: file data, or the path to locate the file
    :return: the data, or 'None' if the file data could not be obtained
    """
    # initialize the return variable
    result: bytes | None = None

    # what is the argument type ?
    if isinstance(file_data, bytes):
        # argument is type 'bytes'
        result = file_data

    elif isinstance(file_data, Path | str):
        # argument is a file path
        buf_size: int = 128 * 1024
        file_path: Path = Path(file_data)
        with file_path.open(mode="rb") as f:
            file_bytes: bytearray = bytearray()
            in_bytes: bytes = f.read(buf_size)
            while in_bytes:
                file_bytes += in_bytes
                in_bytes = f.read(buf_size)
        result = bytes(file_bytes)

    return result
