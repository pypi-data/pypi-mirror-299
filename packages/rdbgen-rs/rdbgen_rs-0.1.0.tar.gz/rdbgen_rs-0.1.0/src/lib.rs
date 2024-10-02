#![allow(deprecated)]

use crc::{Crc, Digest, Table};
use crc_catalog::CRC_64_REDIS;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList, PySet};
use pyo3_file::PyFileLikeObject;

use std::io::Write;

const RDB_TYPE_STRING: u8 = 0x00;
const RDB_TYPE_LIST: u8 = 0x01;
const RDB_TYPE_SET: u8 = 0x02;
const RDB_TYPE_HASH: u8 = 0x04;

const RDB_OPCODE_EOF: u8 = 0xff;
const RDB_OPCODE_SELECTDB: u8 = 0xfe;

const CRC64: Crc<u64, Table<16>> = crc::Crc::<u64, Table<16>>::new(&CRC_64_REDIS);

#[derive(FromPyObject)]
enum RedisPyDataType<'py> {
    Bytes(&'py PyBytes),
    Set(&'py PySet),
    Dict(&'py PyDict),
    List(&'py PyList),
}

#[pyclass]
struct RDBWriter {
    bytesio: PyFileLikeObject,
    crc: Digest<'static, u64, Table<16>>,
    redis_version: u8,
}

#[pymethods]
impl RDBWriter {
    #[new]
    #[pyo3(signature = (file_like, redis_version = 7))]
    fn new(file_like: PyObject, redis_version: u8) -> Self {
        Self {
            bytesio: PyFileLikeObject::with_requirements(file_like, false, true, false, false)
                .unwrap(),
            crc: CRC64.digest(),
            redis_version,
        }
    }

    fn __enter__(mut slf: PyRefMut<Self>) -> PyResult<PyRefMut<Self>> {
        slf._write_header()?;
        Ok(slf)
    }

    fn __exit__(
        &mut self,
        _exc_type: PyObject,
        _exc_value: PyObject,
        _traceback: PyObject,
    ) -> PyResult<()> {
        self._write_eof()
    }

    #[pyo3(signature = (db, dct=None))]
    fn write_db(&mut self, db: u8, dct: Option<&PyDict>) -> PyResult<()> {
        self._write_bytes(&[RDB_OPCODE_SELECTDB, db])?;

        match dct {
            None => {
                return Ok(());
            }
            Some(dct) => {
                if dct.is_empty() {
                    return Ok(());
                }
                for (key, value) in dct.iter() {
                    let key_bytes = key.downcast::<PyBytes>()?.as_bytes();
                    let redis_value = RedisPyDataType::extract(value)?;
                    self.write_fragment(key_bytes, redis_value)?;
                }
            }
        }

        Ok(())
    }

    fn write_fragment(&mut self, key: &[u8], value: RedisPyDataType) -> PyResult<()> {
        let bytes_key = key.rdb_serialize()?;

        let (typecode, bytes_value): (u8, Vec<u8>) = match value {
            RedisPyDataType::Bytes(bytes) => (RDB_TYPE_STRING, bytes.as_bytes().rdb_serialize()?),
            RedisPyDataType::Set(set) => (RDB_TYPE_SET, set.rdb_serialize()?),
            RedisPyDataType::Dict(mapping) => (RDB_TYPE_HASH, mapping.rdb_serialize()?),
            RedisPyDataType::List(sequence) => (RDB_TYPE_LIST, sequence.rdb_serialize()?),
        };

        self._write_bytes(
            [&[typecode], bytes_key.as_slice(), bytes_value.as_slice()]
                .concat()
                .as_slice(),
        )
    }
}

impl RDBWriter {
    fn _write_header(&mut self) -> PyResult<()> {
        self._write_bytes(format!("REDIS{:04}", self.redis_version).as_bytes())
    }

    fn _write_eof(&mut self) -> PyResult<()> {
        self._write_bytes(&[RDB_OPCODE_EOF])?;

        let crc = self.crc.clone().finalize();
        Ok(self.bytesio.write_all(&crc.to_le_bytes())?)
    }

    fn _write_bytes(&mut self, inp: &[u8]) -> PyResult<()> {
        self.crc.update(inp);
        Ok(self.bytesio.write_all(inp)?)
    }
}

trait RedisSerializable {
    fn rdb_serialize(&self) -> PyResult<Vec<u8>>;
}

impl RedisSerializable for &[u8] {
    fn rdb_serialize(&self) -> PyResult<Vec<u8>> {
        let mut res = encode_length(self.len());
        res.extend_from_slice(self);
        Ok(res)
    }
}

impl RedisSerializable for PySet {
    fn rdb_serialize(&self) -> PyResult<Vec<u8>> {
        let mut result = encode_length(self.len());

        for item in self.iter() {
            let bytes: &PyBytes = item.downcast()?;
            result.extend(bytes.as_bytes().rdb_serialize()?);
        }

        Ok(result)
    }
}

impl RedisSerializable for PyList {
    fn rdb_serialize(&self) -> PyResult<Vec<u8>> {
        let mut result = encode_length(self.len());

        for item in self.iter() {
            let bytes: &PyBytes = item.downcast()?;
            result.extend(bytes.as_bytes().rdb_serialize()?);
        }

        Ok(result)
    }
}

impl RedisSerializable for PyDict {
    fn rdb_serialize(&self) -> PyResult<Vec<u8>> {
        let mut result = encode_length(self.len());

        for item in self.items().iter() {
            let (key, value): (&PyBytes, &PyBytes) = item.extract()?;
            result.extend(key.as_bytes().rdb_serialize()?);
            result.extend(value.as_bytes().rdb_serialize()?);
        }

        Ok(result)
    }
}

fn encode_length(length: usize) -> Vec<u8> {
    if length <= 63 {
        // Convert the length to a single byte in big endian
        vec![length as u8]
    } else if length <= 16383 {
        // Encode length in 2 bytes, with the first byte starting at 64
        vec![(64 + (length / 256)) as u8, (length % 256) as u8]
    } else {
        // Encode length in 5 bytes (1 + 4 bytes for the length)
        let mut encoded = vec![0x80];
        encoded.extend(&(length as u32).to_be_bytes()); // Encode in big endian
        encoded
    }
}

#[pymodule]
fn _rdbgen_rs(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RDBWriter>()?;
    Ok(())
}
