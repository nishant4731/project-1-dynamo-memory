# Gorilla Time-Series Port

This Dynamo task asks an agent to port a legacy C++ implementation of Facebook Gorilla-style timestamp and float compression into a Rust library exposed through PyO3 as the Python module `gorilla_rs`. The starting environment provides the legacy C++ source, small binary stream fixtures, and a Rust/PyO3 stub under `/app/rust_gorilla/`.

The task is complete when the agent builds and installs `gorilla_rs`, implements bit-exact compression and decompression for the count-prefixed legacy Gorilla stream format, preserves the C++ implementation quirks on boundary inputs, handles damaged single-stream tail repair metadata, implements the GRA1 multi-series archive container, returns PyArrow `RecordBatch` objects with `timestamp` and `value` columns for streams and archives, and writes `/app/output.json` with the required manifest fields.

## Environment

The single Harbor image is built from the approved Python 3.13 slim base image pinned by digest. It installs the Rust toolchain plus pinned verifier/build dependencies including `pytest`, `pytest-json-ctrf`, `numpy`, `pyarrow`, and `maturin`. The image copies only seed inputs from `task/environment/data` into `/app`; it does not copy the solution or verifier tests.

## Reference Solution

`task/solution/solve.sh` delegates to `solve.py`, which copies a complete Rust implementation into `/app/rust_gorilla`, builds a wheel with `maturin`, installs it into system Python, smoke-tests the module, and writes `/app/output.json`.

## Verification

`task/tests/test.sh` runs the pytest suite and writes the Harbor reward to `/logs/verifier/reward.txt`. The tests check the output manifest, module import and API surface, decompression of legacy `.bin` fixtures, byte-exact recompression, boundary-bucket stress fixtures, GRTF tail-repair recovery plus footer and anchor CRC rejection for damaged single-series streams, GRA1 archive byte layout and CRC/point-count skip semantics including invalid same-name recovery records followed by valid retries, round-trip correctness, PyArrow schema and values, IEEE 754 payload preservation, invalid inputs, and graceful handling of truncated input.

Local calibration commands:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
