# Dragnet restitch charter

A dragnet is what the correlator leaves behind after it has folded a shift of
sensor traffic into one place. This charter is the whole contract: everything a
restitch has to decide is settled here, and nothing outside it is required.

## 1. What a dragnet directory holds

Before a restitch, a dragnet directory holds:

- `FLEET.tsv` — the sensor roster. A header row `sensor` TAB `site`, then one row
  per sensor: `sensor` is the sensor's id, the one a flow record names, and `site`
  is the name of the tap site it sits at. Only the `sensor` column decides
  anything — §3 turns away a record whose `sensor` is not a row here — and no rule
  in this charter reads `site`. It is an input; a restitch leaves the whole file
  exactly as it found it.
- `segments/` — `0001.jsonl`, `0002.jsonl`, … The flow records the correlator had
  already packed. One JSON object per line, ASCII, each line closed by `\n`.
- `inbox/` — `0001.ndjson`, `0002.ndjson`, … Deliveries the correlator accepted
  but had not folded in when it died. One JSON object per line. **The numbers on
  these files are the order the correlator flushed them, which is not the order
  they have to be applied in.**
- `scratch/` — the correlator's working files. Their contents mean nothing.

A **source file** is a regular file lying *directly* in `segments/` or in
`inbox/` — not in a subdirectory of either. The collector sometimes spilled into
subdirectories; nothing under one is ever read as a source of lines, and §10
still removes it with the directory it is in.

`inbox/`, `scratch/` and `segments/` may each be absent or empty; none of those
is an error.

After a restitch the directory holds exactly `FLEET.tsv`, `segments/`,
`CONTACT.tsv`, `REACH.tsv`, `PIVOT.tsv`, `refused/` and `restitch_report.json` —
and nothing else. `inbox/` and `scratch/` are gone. `segments/`, `CONTACT.tsv`, `REACH.tsv`,
`PIVOT.tsv`, `refused/` and `restitch_report.json` are replaced outright each
time, and `refused/` is present even when it is empty.

## 2. A flow record

A flow record is a JSON object carrying exactly these thirteen keys:

| key | what it is |
|---|---|
| `fid` | the flow id: `f-` followed by exactly five decimal digits |
| `src` | the host that opened the flow: `h-` followed by exactly three decimal digits |
| `dst` | the host that received it, same shape as `src` |
| `sport` | source port, an integer in 1…65535 |
| `dport` | destination port, an integer in 1…65535 |
| `first` | when the sensor first saw the flow, an integer in milliseconds |
| `last` | when it last saw it, an integer strictly greater than `first` |
| `bytes` | an integer of at least 1 |
| `pkts` | an integer of at least 1 |
| `sensor` | the sensor that observed it; it must be a row of `FLEET.tsv` |
| `label` | the service attribution: at most 120 characters, a lowercase letter followed by lowercase letters and digits, then any number of further groups of lowercase letters and digits each introduced by one `/` or one `-` |
| `state` | how the flow ended: `closed` if the peers closed it between them, `reset` if one of them tore it down, `timeout` if the sensor stopped seeing it and gave up on it. Exactly one of those three |
| `seq` | the correlator's sequence number for the record, an integer of at least 0 |
| `sum` | the record's check value, sixteen lowercase hex characters |

`seq` and `sum` are counted among the thirteen. An **integer** here means a JSON
integer: `true` is not an integer and neither is a number written with a decimal
point.

Wherever a rule below settles a tie by the **lowest** `fid`, host id or file
name, those compare as text, character by character. Because every `fid` carries
exactly five digits and every host id exactly three, text order and numeric order
agree for them; file names are compared as text throughout.

The **check value** of a record is the first sixteen characters of the
hexadecimal SHA-256 digest of its canonical payload. The canonical payload is the
JSON object of the eleven keys `fid`, `src`, `dst`, `sport`, `dport`, `first`,
`last`, `bytes`, `pkts`, `sensor`, `label`, `state` — that is, the record without
`seq` and without `sum` — encoded as

    json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")

## 3. Sifting

Lines are read in one order: every source file of `segments/` in file-name
order, then every source file of `inbox/` in file-name order, and the lines of a
file in the order they appear. Only source files as §1 defines them are read. A line either stands or is turned away, and a line that is turned
away has exactly one cause: the **first** of these that applies to it.

1. `unparsable` — the line is not a JSON object.
2. `incomplete` — a key the line needs is not there.
3. `malformed` — a value the line carries is the wrong type, the wrong shape or
   out of range, or the line carries a key it has no business carrying.
4. `unknown_sensor` — `sensor` names no row of `FLEET.tsv`.
5. `tampered` — `sum` is not the record's check value.
6. `duplicate_id` — an earlier line that stood already claimed that `fid`.

A line from `segments/` is a flow record and is sifted against §2. A line from
`inbox/` carries an `op` on top of that; see §4. A `duplicate_id` is judged
against every `fid` claimed by an earlier line that stood, in the reading order
above — not in the order §4 folds things.

## 4. The inbox and the fold

An inbox line carries `op`, whose value is `admit`, `amend` or `retract`; any
other value is `malformed`, and a line with no `op` at all is `incomplete`.

- an `admit` carries the thirteen keys of §2 and `op`, and nothing else. It is
  sifted exactly as a flow record is.
- an `amend` carries exactly `op`, `seq`, `fid`, `bytes`, `pkts`, `state` and
  `last`, with the types and ranges §2 gives those keys.
- a `retract` carries exactly `op`, `seq` and `fid`.

The operations that stand are applied in **ascending `seq`**; two operations with
the same `seq` are applied in file-name order, and within one file in line order.
Each is applied to the flows as they stand **at that moment**:

- an `admit` puts its flow among them.
- an `amend` whose `fid` is not among them is an **orphan amend** and is dropped.
- an `amend` whose `last` is not greater than the `first` of the flow it names is
  **incoherent** and is dropped.
- any other `amend` writes its `bytes`, `pkts`, `state` and `last` onto the flow
  it names, and sets that flow's `seq` to the operation's `seq`.
- a `retract` whose `fid` is not among them is an **orphan retract** and is
  dropped; otherwise it takes that flow away.

## 5. Co-observations

Two sensors watching the same wire report the same flow twice. After the fold,
flows that agree on `src`, `dst`, `sport`, `dport` **and** `first` are
observations of one flow and become one record:

- `fid` is the lowest `fid` among them;
- `last`, `bytes` and `pkts` are each the greatest among them;
- `src`, `dst`, `sport`, `dport` and `first` they already agree on;
- `sensor`, `label`, `state` and `seq` are those of the observation with the
  greatest `seq`, and the lowest `fid` among those settles a tie. Two sensors may
  attribute the same wire differently, so the observations of one flow need not
  agree on `label`; the one that carries is the same one that carries `sensor`.

Flows that differ in any of the five are separate flows even when the same pair
of hosts is involved. Every surviving flow's `sum` is then re-taken over its
canonical payload, whatever it carried before.

## 6. Segments and `CONTACT.tsv`

The surviving flows are ordered by ascending `first`, and equal `first` by
ascending `fid`. In that order they are laid into `segments/0001.jsonl`,
`0002.jsonl`, … A segment holds **at most 13 records and at most 3450 bytes**,
counting the `\n` that closes each record; a record that would carry a segment
past either bound opens the next one instead, and a record that alone exceeds the
byte bound still gets a segment of its own. A record is written as

    json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"

`CONTACT.tsv` is a header row of `fid`, `segment`, `offset`, `src`, `dst`,
`state`, `first`, `last` joined by TAB, then one row per surviving flow **in the
order the flows were laid down**, each field rendered as it appears above and
integers in decimal. `segment` is the file name the record landed in. `offset` is
the number of bytes between the start of that file and the first byte of the
record — so it starts again from zero in every segment. The file ends with `\n`.

## 7. The contact graph, `REACH.tsv` and `PIVOT.tsv`

Only a flow that `closed` is a **contact**; a contact runs from its `src` to its
`dst` and occupies the window from its `first` to its `last`.

A host holds what a contact brought it for a **relay window** of `380000`, and
no longer. A **trail** out of a host h is a run of contacts c₁, c₂, …, c_k where
c₁ starts at h, each contact starts at the host the one before it ended at, and
each contact's `first` is **not below** the `last` of the one before it and **not
above that `last` by more than the relay window**. Nothing constrains when c₁
opens. Host x is **reached** from h when some trail out of h ends at x, and the
time x is reached is the lowest `last` over every trail out of h that ends at x.

`REACH.tsv` is a header row of `origin`, `reach`, `horizon`, `farthest` joined by
TAB, then one row for every host that is the `src` of at least one contact, in
ascending host order:

- `reach` — how many **distinct** hosts are reached from `origin`;
- `horizon` — the greatest of the times those hosts are reached, in decimal;
- `farthest` — the host reached at that time, the lowest host id settling a tie.

The file ends with `\n`. Note that a trail may lead back to the host it started
from, and that a host reached by more than one trail is one host.

`REACH.tsv` looks forward from a host. `PIVOT.tsv` looks back at one. A host y
**approaches** a host t when some trail out of y ends at t, and the **opening** of
that approach is the `first` of the trail's own first contact — the moment the
approach began, not the moment it landed. `PIVOT.tsv` is a header row of `target`,
`sources`, `opened`, `origin` joined by TAB, then one row for every host that at
least one contact arrives at, in ascending host order:

- `sources` — how many **distinct** hosts approach `target`;
- `opened` — the **least** opening over every approach to `target`, in decimal;
- `origin` — the host whose approach opened then, the lowest host id settling a
  tie. Where one host has several approaches, its opening is the least of them.

The file ends with `\n`. `sources` counts the same pairs `REACH.tsv` does, read
the other way round, so the two tables' totals agree; `opened` does not follow
from `REACH.tsv` at all, because that table records when a host is *reached* and
this one records when the approach to it *began*. Reversing the contacts and
walking them the way §7 walks them forward answers a different question, since the
order the times must respect reverses with them.

## 8. `refused/`

Every line turned away is written into `refused/`, into a file named for the file
it came from: the source file's name with its extension dropped, then `.rej`. The
first source file to have a line turned away takes that name as it stands; a
later source file whose name would collide takes `-2`, then `-3`, and so on
before the `.rej` — counted over the reading order of §3 and only over files that
actually had a line turned away. Each turned-away line is one row of that file:

    json.dumps({"cause": …, "line": …, "source": …, "text": …},
               sort_keys=True, separators=(",", ":")) + "\n"

where `cause` is one of the six names of §3, `line` is the line's number within
its source file counting from 1, `source` is the source file's path relative to
the dragnet directory (`segments/0002.jsonl`, `inbox/0001.ndjson`), and `text` is
the line as it was read, without its closing newline. Rows keep the reading
order.

## 9. `restitch_report.json`

One JSON object of exactly these thirty-five keys, every value an integer,
written as `json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"`.
Each is counted at the point in the passes above that its name refers to.

| key | what it counts |
|---|---|
| `segment_files_read` | files in `segments/` |
| `segment_lines_read` | lines read from them |
| `inbox_files_read` | files in `inbox/` |
| `inbox_lines_read` | lines read from them |
| `lines_refused` | lines turned away, from both |
| `refused_unparsable` | lines turned away as `unparsable` |
| `refused_incomplete` | lines turned away as `incomplete` |
| `refused_malformed` | lines turned away as `malformed` |
| `refused_unknown_sensor` | lines turned away as `unknown_sensor` |
| `refused_tampered` | lines turned away as `tampered` |
| `refused_duplicate_id` | lines turned away as `duplicate_id` |
| `refused_from_segments` | of those, the ones from `segments/` |
| `refused_from_inbox` | of those, the ones from `inbox/` |
| `refused_files_written` | files written into `refused/` |
| `refused_files_ordinalled` | of those, the ones that needed `-2`, `-3`, … |
| `ops_admitted` | admits that stood and were applied |
| `ops_amended` | amends that wrote onto a flow |
| `ops_retracted` | retracts that took a flow away |
| `orphan_amends` | amends dropped for naming no flow |
| `orphan_retracts` | retracts dropped for naming no flow |
| `amends_incoherent` | amends dropped as incoherent |
| `observations_settled` | flows standing after the fold, before §5 |
| `merge_groups` | groups of §5 holding more than one observation |
| `observations_merged_away` | observations §5 absorbed |
| `flows_settled` | flows standing after §5 |
| `sums_rewritten` | surviving flows whose re-taken `sum` differs from the one carried by the line that claimed their `fid` |
| `segments_written` | segment files written |
| `bytes_written` | bytes written into them, newlines counted |
| `contacts` | surviving flows that `closed` |
| `reach_origins` | rows of `REACH.tsv` |
| `reach_pairs` | the `reach` column of `REACH.tsv`, added up |
| `pivot_targets` | rows of `PIVOT.tsv` |
| `pivot_pairs` | the `sources` column of `PIVOT.tsv`, added up |
| `inbox_consumed` | files removed with `inbox/` |
| `scratch_consumed` | files removed with `scratch/` |

## 10. What a restitch spends, and settling

A restitch consumes the evidence it folds: `inbox/` and `scratch/` are removed,
directory and all. Restitching a dragnet that has already been restitched leaves
`segments/`, `CONTACT.tsv`, `REACH.tsv` and `PIVOT.tsv` byte-for-byte as they
were.

A restitch writes only inside the dragnet directory it was given, and it neither
reads nor writes through a symbolic link: a dragnet is a tree of real files and
directories, and one that is not may be refused outright.

## 11. What is supplied

`/app/dragnet_io.py` is read-only and holds the mechanical half of a restitch, so
none of it has to be written again: `listing`, `read_lines` and `parse_line` for
the source order of §3, `load_fleet` for the roster, `flow_sum` for the check
value of §2, `render_record` and `record_size` for the segment text of §6,
`refusal_row` for the row shape of §8, `render_report` for the report of §9, and
`discard` for a directory §10 consumes.

Every decision this charter asks for is outside it: what stands and what is
turned away and under which of the six causes, the order the operations fold in
and what they mean against the flows as they stand, what makes two observations
one flow, how a segment is bounded and where the offsets restart, what a trail
through the contact graph is, what the three reach columns and the three pivot
columns hold, what each of the thirty-five counters counts, and how the files
under `refused/` are named.

## 12. Format sheet

These fragments pin the conventions and nothing else. They come from a dragnet
you do not have; reproducing them proves nothing about a restitch.

One line of `segments/0002.jsonl`, the second record in that segment:

    {"bytes":9126008,"dport":4444,"dst":"h-004","fid":"f-50003","first":798382,"label":"mssql/tds-login/tunnel-established/epmapper","last":808734,"pkts":389743,"sensor":"tap-05","seq":0,"sport":48860,"src":"h-012","state":"closed","sum":"ea55c65b615ef39f"}

The two rows of `CONTACT.tsv` that name that segment first, which is where the
offset column starts again:

    f-00008	0002.jsonl	0	h-012	h-004	closed	798382	808734
    f-50003	0002.jsonl	255	h-012	h-004	closed	798382	808734

Two rows of `REACH.tsv`, following its header row:

    h-002	2	837268	h-014
    h-004	3	1269117	h-001

Two rows of `PIVOT.tsv`, following its header row:

    h-001	1	1247594	h-004
    h-002	1	879099	h-009

One row of a file under `refused/`:

    {"cause":"tampered","line":5,"source":"inbox/0001.ndjson","text":"{\"bytes\":59098,\"dport\":8080,\"dst\":\"h-009\",\"fid\":\"f-60013\",\"first\":51400,\"label\":\"edge/witness\",\"last\":55721,\"op\":\"admit\",\"pkts\":702,\"sensor\":\"tap-03\",\"seq\":524,\"sport\":40002,\"src\":\"h-008\",\"state\":\"closed\",\"sum\":\"755fbaf0562ee70a\"}"}
