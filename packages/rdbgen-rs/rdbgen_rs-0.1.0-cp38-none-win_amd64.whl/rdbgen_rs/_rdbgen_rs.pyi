from __future__ import annotations

from types import TracebackType
from typing import BinaryIO

from typing_extensions import Self

from . import REDIS_DATA_TYPES, REDIS_DB_TYPE

class RDBWriter:
    def __init__(self, bytesio: BinaryIO, redis_version: int = 7) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    def write_db(self, db: int, dct: REDIS_DB_TYPE | None = None) -> None: ...
    def write_fragment(self, key: bytes, value: REDIS_DATA_TYPES) -> None: ...
