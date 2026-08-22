A dragnet correlator died part way through folding a shift of sensor traffic, and
the dragnet it was writing is stranded. Write the tool that restitches it.

Deliver `/app/dragnet_restitch.py`. It is run as

`python3 /app/dragnet_restitch.py <dragnet_dir>`

and it restitches that dragnet where it stands: it sifts the packed segments and
the unfolded inbox, folds the operations in, merges the observations that turn
out to be the same flow, re-takes every check value, repacks the segments and
rebuilds `CONTACT.tsv`, walks the contact graph forward into `REACH.tsv` and back
into `PIVOT.tsv`, files what it turned away under `refused/`, consumes the inbox
and the scratch directory, and writes `restitch_report.json`. Keep it to that one
file, the Python standard library and `/app/dragnet_io.py` — we lift it out on its
own, beside that module, and run it from an empty directory — and have it exit
zero.

`/app/dragnet_io.py` is supplied read-only and already holds the mechanical half:
reading a dragnet's files in order, the canonical payload a check value is taken
over, the one canonical text of a settled record, of a refusal row and of the
report, and the removal of a directory the restitch consumes. None of that has to
be written again; every decision the charter asks for is outside it.

`/app/data/DRAGNET_CHARTER.md` is the contract. It gives the directory layout,
the thirteen keys of a flow record, the canonical payload the check value is
taken over, the six causes that turn a line away and the order they are tried in,
the three inbox operations and the order they are applied in, the rule that makes
two observations one flow, the bounds a segment is packed under, the byte layout
of `CONTACT.tsv`, what a trail through the contact graph is, the three numbers
`REACH.tsv` reports for each host that opens one and the three `PIVOT.tsv` reports
for each host that one arrives at, the naming of the files under `refused/`, all
thirty-five counters of the report, and what a restitch spends.
Its last two sections list what `/app/dragnet_io.py` supplies, and a format sheet: a handful of real lines that pin the
conventions. It quotes no answer, and reproducing it proves nothing.

`/app/data/dragnet` is the live dragnet and it is graded exactly as you leave it.
A restitch spends the evidence as it goes, so a run that stops half way leaves the
dragnet part folded — recoverable, not fatal. `/app/data/dragnet.spare.tar` is a
pristine archive of the same crashed dragnet, and

`rm -rf /app/data/dragnet && tar -C /app/data -xf /app/data/dragnet.spare.tar`

puts it back exactly as it shipped, as often as you like. So restitch it early and
restitch it again: get a first pass onto disk while you still have most of the
clock, then improve it. Holding the live run back until the tool is finished is the
one way to end with nothing written. Only the state you leave behind is read.

You are graded on two things: the state of `/app/data/dragnet` when you stop, and
your tool run against dragnets it has never seen. Both are compared file by file
and directory by directory — every byte of every segment, every row of
`CONTACT.tsv`, `REACH.tsv` and `PIVOT.tsv`, every file under `refused/`, every counter of
`restitch_report.json`, and nothing left lying about that the charter does not
name — so the tool has to restitch any conforming dragnet, not just this one, and
leave it in the shape the charter describes. It is also run twice over on the same
dragnet, because the charter says what a second restitch has to leave alone.

The dragnet in the image is a quiet shift on a small network. The ones your tool
will be run against are not: they are wider, they are busier, and the traffic on
them crosses over itself.
