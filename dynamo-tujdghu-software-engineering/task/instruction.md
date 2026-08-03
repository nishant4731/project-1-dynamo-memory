A legacy C++ time-series storage service uses a custom implementation of Facebook's Gorilla floating-point and timestamp compression algorithm located at `/app/legacy_gorilla/`. The legacy C++ engine packs variable-length bit streams to compress 64-bit UNIX epoch timestamps (delta-of-delta encoding) and 64-bit IEEE 754 double-precision floats (XOR difference encoding with leading/trailing zero bit elimination).

Your task is to port this legacy C++ compression logic into a production-grade Rust library with PyO3 Python bindings, located at `/app/rust_gorilla/`, compile it into a Python wheel, and install it into the system Python environment under the module name `gorilla_rs`.

### Specific Requirements

1. **Bit-Exact Decompression & Compression**:
   - Port the legacy wire format exactly as implemented by `/app/legacy_gorilla/gorilla.cpp` and `/app/legacy_gorilla/gorilla.h`, including bit order, count header, bucket boundaries, sign extension, partial-byte flush behavior, single-stream repair metadata, and other compatibility quirks.
   - Implement bit-level stream reading (`BitReader`) and writing (`BitWriter`) for unaligned variable-length fields. A generic Gorilla codec is not sufficient; compressed bytes produced by Rust must be byte-for-byte compatible with the provided legacy C++ implementation.
   - Preserve all 64-bit IEEE 754 payload bits for finite values, signed zero, subnormals, Inf, and non-canonical NaN values without mathematical canonicalization.
   - For empty or mismatched timestamp/value inputs, `compress_series` should return an empty byte vector. For malformed or truncated binary streams, `decompress_series` should not crash Python and should return the prefix it can decode as parallel list objects.

2. **PyO3 Module & Interface**:
   - Build a PyO3 native Python module named `gorilla_rs`.
   - Expose the following Python API:
     - `gorilla_rs.compress_series(timestamps: list[int], values: list[float]) -> bytes`: Compresses input timestamp and value arrays into a single binary stream byte vector.
     - `gorilla_rs.decompress_series(data: bytes) -> tuple[list[int], list[float]]`: Decompresses binary stream back into parallel lists of integer timestamps and float values.
     - `gorilla_rs.decompress_to_arrow(data: bytes) -> object`: Decompresses binary stream and exports the result directly as a PyArrow RecordBatch.
     - `gorilla_rs.compress_archive(series: dict[str, tuple[list[int], list[float]]]) -> bytes`: Compresses a mapping of series names to timestamp/value arrays into the legacy archive container.
     - `gorilla_rs.decompress_archive(data: bytes) -> dict[str, tuple[list[int], list[float]]]`: Decompresses every valid series block from an archive, skipping corrupt blocks.
     - `gorilla_rs.archive_to_arrow(data: bytes) -> dict[str, object]`: Exports each valid archive series as a PyArrow RecordBatch keyed by series name.
   - The RecordBatch returned by `decompress_to_arrow` must contain two columns named `timestamp` and `value`, preserving the same row order as `decompress_series`.
   - Malformed or truncated input data must not crash Python; `decompress_series` should return list objects for both timestamps and values.
   - Also port the legacy multi-series archive container documented in `/app/legacy_gorilla/gorilla.h`: sorted raw-UTF-8 names, exact little-endian index fields, CRC32 validation, one-point/empty entries, shared payload offsets for byte-identical blocks, duplicate-name first-valid recovery, optional payload patch, embedded, XOR, threshold-share, transform, composite, delta, hash-chain, and alias footers, corrupt-entry skipping, and recovery-footer retry semantics where an invalid same-name footer record does not reserve that name against a later valid record.
   - `GRAT` transform footers derive a new series from an already recovered base series by applying per-row timestamp deltas and a raw float64 bit XOR mask, recompressing with the normal Gorilla writer, validating the recovered block CRC, and making the result available to later aliases.
   - `GRAC` composite footers derive a new series from two already recovered base series using checked row-wise timestamp composition and rotated/XORed raw float64 bit patterns, then recompress and CRC-validate before aliases.
   - `GRAD` delta footers run after `GRAC` and before aliases: decode per-row unsigned LEB128 pairs from the footer payload, zigzag-decode timestamp corrections, XOR cumulative float64 mask deltas, derive from an already recovered base, require the payload to be consumed exactly, recompress, CRC-validate, and expose valid records to aliases.
   - `GRAH` hash-chain footers run after `GRAD` and before aliases: decode per-row unsigned LEB128 pairs, zigzag-decode timestamp corrections, initialize/advance the 64-bit wrapping row chain exactly as described in `gorilla.h` including high-bit authority-seeded bases, derive timestamps with the low-chain offset and values with `base_bits ^ mask_delta ^ chain`, require exact payload consumption, recompress, CRC-validate, and expose valid records to aliases.

3. **Build & Output Manifest**:
   - Use `maturin` to build and install `gorilla_rs` into the system Python environment (`pip install .`).
   - Create a JSON file at `/app/output.json` with the following schema:
     ```json
     {
       "status": "success",
       "module_name": "gorilla_rs",
       "installed_version": "0.1.0",
       "supported_features": ["delta_of_delta", "xor_float64", "arrow_record_batch", "archive_container", "archive_block_dedup", "archive_patch_repair", "archive_embedded_recovery", "archive_xor_recovery", "archive_share_recovery", "archive_transform_recovery", "archive_composite_recovery", "archive_delta_recovery", "archive_hash_chain_recovery", "series_tail_repair"]
     }
     ```

Legacy C++ code reference and test sample `.bin` files are located at `/app/legacy_gorilla/`.
