from __future__ import annotations

from typing import BinaryIO, Union

from ._rdbgen_rs import RDBWriter
from ._version import VERSION

__version__ = VERSION

__all__ = ["RDBWriter", "REDIS_DATA_TYPES", "REDIS_DB_TYPE", "rdbgen"]

REDIS_DATA_TYPES = Union[bytes, list[bytes], dict[bytes, bytes]]
REDIS_DB_TYPE = dict[bytes, REDIS_DATA_TYPES]


def rdbgen(io: BinaryIO, dct: REDIS_DB_TYPE) -> None:
    with RDBWriter(io, 7) as writer:
        writer.write_db(0, dct)
