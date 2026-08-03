AFR transfer notes

Every ledger row names a block under `/app/transfer`. The ledger is authoritative; ignore block files that are not referenced by an approved ledger row.

AFR file layout:
- bytes 0..3: ASCII `AFR1`
- bytes 4..5: unsigned little-endian JSON header length
- next header-length bytes: UTF-8 JSON header
- remaining bytes: payload

Data blocks with `codec=dpcm8-mono` store the first sample as signed 16-bit little-endian. Each remaining payload byte is a signed 8-bit delta from the previous stored sample. After decoding, apply the ledger `polarity` to obtain canonical signed 16-bit PCM for that row.

Data blocks with `codec=qad4-chain` store one 4-bit code per output sample, packed low nibble first in each byte. QAD4 is chained: before decoding a QAD4 block, the previous output block in restored-master order must already be known. The initial predictor is the final signed sample of that previous canonical block. The initial step index is `(abs(predictor) + start_sample) mod 16`. The step table is `[1, 2, 3, 5, 7, 10, 14, 19, 26, 35, 47, 63, 85, 114, 153, 205]`. For each nibble, `magnitude = code & 7`, `delta = ((2*magnitude + 1) * step_table[step_index]) // 2`, and bit 3 chooses the sign: clear adds the delta to the predictor, set subtracts it. Clamp the predictor to signed 16-bit after the delta, emit it as the next canonical sample, then update `step_index` by `[-2, -1, 0, 1, 2, 3, 4, 5][magnitude]` and clamp the index to `0..15`. QAD4 rows always use ledger polarity `+`.

The SHA-256 in `decoded_sha256` is over the canonical PCM bytes for data rows and over the raw parity payload for parity rows.

Rows with `kind=xor_parity` use `codec=xor_parity`. Their payload is the bytewise XOR of the canonical PCM16LE bytes for all data slots in the stripe.

Rows with `kind=gf256_parity` use `codec=gf256_parity`. Their payload is a second bytewise parity equation over GF(256) with reducing polynomial `0x11d`. The AFR JSON header contains `slot_coefficients`, an object whose keys are slot numbers as strings and whose values are byte coefficients. For each byte position, the stored parity byte equals the XOR of `mul(coefficient, slot_byte)` for every data slot in that stripe, where `mul` is multiplication in GF(256).

If one data slot in a stripe is unverified, recover it from `xor_parity`. If two data slots in a stripe are unverified, recover both by solving the two bytewise equations supplied by `xor_parity` and `gf256_parity`.
