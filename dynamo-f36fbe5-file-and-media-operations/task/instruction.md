Deliver `/app/rebuild_atlas.py` as an executable Python 3 program.

`/app/data/FORMAT.md` is the authoritative contract for packet fields, replay selection, rendering math, counters, hashes, and restored file schemas. When run as `/app/rebuild_atlas.py PACKET_DIR`, repair that exact packet directory, create/update `PACKET_DIR/restored/` with the artifacts described by the format contract, and consume every regular file below `PACKET_DIR/pieces/` without deleting the `pieces/` directory.

Before submission, use your program to repair the bundled visible packet at `/app/data/packet-visible`. The required visible deliverables are:

- `/app/data/packet-visible/restored/restored_atlas.png`
- `/app/data/packet-visible/restored/restored_manifest.json`
- `/app/data/packet-visible/restored/restored_layer_audit.tsv`
- `/app/data/packet-visible/restored/restored_occupancy.pgm`
- `/app/data/packet-visible/restored/restored_cell_index.tsv`
