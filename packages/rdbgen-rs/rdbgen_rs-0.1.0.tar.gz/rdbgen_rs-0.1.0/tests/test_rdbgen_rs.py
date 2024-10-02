from __future__ import annotations

import io
from enum import Enum, auto

import pytest

from rdbgen_rs import REDIS_DB_TYPE, RDBWriter, rdbgen

TEST_DATA = [
    (
        {},
        b"REDIS0007\xfe\x00\xffc\x9f\xf4\xf1\xebo\xa0\xd9",
    ),
    (
        {b"a": b"0"},
        b"REDIS0007\xfe\x00\x00\x01a\x010\xff\x08\x64\x37\x55\xe6\xfa\xc4\x4d",
    ),
    (
        {b"a": {b"0"}},
        b"REDIS0007\xfe\x00\x02\x01a\x01\x010\xff\x30\xeb\x26\xab\xeb\x94\xd7\xf3",
    ),
    (
        {b"a": [b"0"]},
        b"REDIS0007\xfe\x00\x01\x01a\x01\x010\xff\x26\xdb\x21\x8e\xc0\x72\x2c\x54",
    ),
    (
        {b"a": {b"0": b"z"}},
        b"REDIS0007\xfe\x00\x04\x01a\x01\x010\x01z\xff\xb6\x76\xe4\x10\xed\x97\xce\xdc",
    ),
]


class MethodTestEnum(Enum):
    RDBGEN = auto()
    DB = auto()
    STREAM = auto()


@pytest.mark.parametrize("dct,binary", TEST_DATA)
@pytest.mark.parametrize("method", (list(MethodTestEnum)))
def test_rdbgen(
    dct: REDIS_DB_TYPE,
    binary: bytes,
    method: MethodTestEnum,
) -> None:
    bytesio = io.BytesIO()

    if method is MethodTestEnum.RDBGEN:
        rdbgen(bytesio, dct)
    elif method is MethodTestEnum.DB:
        with RDBWriter(bytesio) as writer:
            writer.write_db(0, dct)
    elif method is MethodTestEnum.STREAM:
        with RDBWriter(bytesio) as writer:
            writer.write_db(0)
            for key, value in dct.items():
                writer.write_fragment(key, value)
    else:
        raise TypeError("Unexpected enum type.")

    assert bytesio.getvalue() == binary
