# Wardline chart vault — mend handbook

The vault took a crash partway through an ingest run. This is the standing description of
what a vault holds, how a document is rebuilt from what survived, and what filing, disposal
and the mend report must contain. It does not tell you what any station's clock was doing;
that is the one thing the mend has to work out for itself, and §4 says where the evidence is.

## 1. What a vault directory holds

* `vault.json` — an object with the string `vault_id`, the integer `as_of`, `serviced`, an
  object giving the instant each station was last serviced, and `declared_offsets`, an object
  giving each station's clock offset **as the station declared it at commissioning**. Two of those declarations have since drifted out of true
  and were never corrected; the receipts are the record of what the clocks actually did.
* `registry.tsv` — one row per document the vault is supposed to hold, header
  `doc_id  encounter  title  station  bytes  sha256  retention  gateway_stamp`.
  `bytes` is the document's exact length, `sha256` its lowercase hex digest, `retention` one
  of `transient`, `standard`, `extended`, `station` the station that ingested it, and
  `gateway_stamp` either an integer or a single `-`.
* `receipts/<station>.tsv` — one file per station, header
  `stamp  doc_id  fragment  ordinal`, one row per fragment that station wrote, `stamp` read
  off that station's own clock.
* `holds.tsv` — header `encounter`, then one encounter per line, each under legal hold.
* `spool/` — the fragments themselves, one file each, raw bytes.
* `filed/` — where rebuilt documents go. It starts empty.

All times in a vault are integer **minutes**. A day is 1440 of them.

## 2. Rebuilding a document

Take the registry in ascending `doc_id`. For each document:

**From its receipts.** A document belongs to the station the registry names for it, and only
that station's rows are its evidence: an ingest that failed and was picked up elsewhere leaves
receipt rows, and fragments, under another station, and neither is part of this document.
Gather that station's rows naming it and sort them by `ordinal`. They are usable only when the ordinals run 1, 2, 3 … with no gap and every
fragment they name is still in the spool. Concatenate those fragments in ordinal order.

**By search.** When the receipts are unusable — the crash lost rows — the document has to be
found among the fragments no receipt accounts for. A document's fragments were spooled in
the order they were written, so their names ascend in that order; what is unknown is which
of the loose fragments are its. Any set whose total length is the registered `bytes` and
whose concatenation in ascending name order has the registered `sha256` is the document.
Fragments a search consumes are no longer loose for later documents.

**Then check.** A rebuilt document whose digest does not match the registry is *quarantined*:
it is not filed, not disposed, and nothing of it is written into `filed/`. A document that
can be rebuilt neither way is quarantined too.

## 3. Filing, disposal and holds

A rebuilt document is either filed or disposed, decided by its retention:

* `transient` keeps for 30 days, `standard` for 365, `extended` for 2555.
* The document's instant on the gateway clock is its `gateway_stamp` when the registry
  carries one, and otherwise the **latest** of its receipt stamps once each has been moved
  onto the gateway clock (§4).
* Its disposal falls due at that instant plus its retention in minutes. A document whose
  disposal is due at or before the vault's `as_of` is *disposed*: it is not written into
  `filed/`. Anything else is *filed*.
* A disposal is stopped by a legal hold: when the document's `encounter` is in `holds.tsv`
  it is *held* instead — and a held document **is** written into `filed/`, exactly as a
  filed one is.

A filed or held document is written to `filed/<encounter>/<name>`, where `<name>` comes from
its `title`:

* the name is the title lowercased, and nothing else;
* when that name is already taken **within that encounter**, the next free `~2`, `~3`, … is
  inserted before the extension — `discharge_summary~2.pdf`. The extension is whatever
  follows the **last** dot, except that a dot in first position never begins one, so a name
  like `.discharge_summary` has none and takes the ordinal at the end
  (`.discharge_summary~2`);
* documents are considered in ascending `doc_id` — which is **not** the order the registry
  file happens to list them in — so the first one to claim a name keeps it.

## 4. What the clocks were doing

Each station stamps its receipts from its own clock, which runs a whole number of minutes
off the gateway's; that difference is what you subtract from a station's stamp to read it on
the gateway clock. A station's clock is not constant across a vault, though. Every station
has been serviced once, at the instant `vault.json` records for it, and came back on a
different offset — so each station has **two** offsets, the one it ran on before its service
and the one it has run on since, and which applies to a receipt depends on which side of that
instant the receipt falls.

The evidence is the anchored documents. When the registry carries a `gateway_stamp`, that is
the true instant the document's ingest began, and the same instant appears — read off the
station's own clock — as the stamp on that station's receipt for the document's **first**
fragment. An anchor is evidence only for the side of the service instant it falls on, and
every station in a vault has at least one anchored document on each side.

`declared_offsets` in `vault.json` is what each station reported at commissioning. It is not
evidence, and for two stations in every vault it is wrong.

## 5. The mend, in order

1. Rebuild, file, dispose or quarantine every registered document as §2 and §3 describe,
   taking the registry in ascending `doc_id`.
2. Write `mend_report.json` into the vault directory, exactly as §6 describes.
3. Consume the evidence: the `spool/` and `receipts/` directories are removed from the vault
   directory, whole. A mended vault holds `vault.json`, `registry.tsv`, `holds.tsv`,
   `filed/` and `mend_report.json`, and cannot be mended a second time.

## 6. `mend_report.json`

A JSON object serialised with keys sorted ascending by Unicode code point, `,` and `:` as
separators with no spaces, and one trailing newline. Every number in it is an integer.

| key | value |
|---|---|
| `schema` | the fixed string `wardline-chartvault/v1` |
| `vault_id` | from `vault.json` |
| `as_of` | from `vault.json` |
| `documents` | rows in the registry |
| `station_offsets` | object keyed by station, holding `[before, after]` — the two offsets §4 mines for it |
| `stations_mined` | how many stations the vault has receipts for |
| `stations_declared_wrong` | stations whose `declared_offsets` entry differs from the offset they run on now |
| `anchors_used` | registry rows carrying a `gateway_stamp` |
| `filed` | documents written to `filed/` and not under hold |
| `held` | documents whose disposal was stopped by a legal hold |
| `disposed` | documents whose disposal had fallen due |
| `quarantined` | documents that could not be rebuilt, or rebuilt wrong |
| `rebuilt_from_receipts` | documents the mend **kept** — filed, held or disposed — that it rebuilt from their receipts. A document whose receipts were usable but whose digest then disagreed is quarantined, and is not counted here |
| `rebuilt_by_search` | documents the mend kept that it recovered from the loose fragments |
| `receipt_gaps` | documents whose receipts were not usable, whether or not the search then found them |
| `digest_failures` | rebuilt documents whose digest disagreed with the registry |
| `collisions` | filed or held documents that had to take a `~n` name |
| `fragments_used` | spool fragments that went into a document the mend **kept** — one it filed, held or disposed. A quarantined document's fragments are not used, whether it was assembled and failed its digest or could not be assembled at all |
| `fragments_orphaned` | every other fragment on the spool |
| `outcomes` | array, ascending by `doc_id`, of objects `{"doc_id", "outcome", "filed_as"}` |

`outcome` is `filed`, `held`, `disposed` or `quarantined`. `filed_as` is the name under
`filed/<encounter>/` for a filed or held document and a single `-` for the others.

## 7. What the conventions look like

`/app/data/wardline/example_vault` is a small vault you can run against. The bytes below are
not its answer — they are three fragments of one, shown because prose is a poor way to pin a
byte layout.

A station's pair of offsets is written `[before, after]`, in that order:

```
<<SAMPLE_OFFSET>>
```

Two rows of an `outcomes` array — the shape of an entry, and how a name already taken inside
an encounter takes its ordinal before the extension:

```
<<SAMPLE_ROWS>>
```

Nothing else about that vault's mend is published here: not its counters, not the rest of
its outcomes, not its filed tree. §2 to §6 are the account of every rule, and what a vault
mends to follows from them.
