# Atlas Rebuild

This Dynamo task asks the agent to implement `/app/rebuild_atlas.py`, a reusable Python tool that rebuilds RGBA design atlases from packet directories.

The packet format combines an event journal, mixed PNG/RLE tile sources, transform strings, opacity scaling, and exact layer-selection rules. The visible fixture is in `task/environment/data/packet-visible`; hidden verifier packets are generated at test time with varied dimensions and event combinations.

Verification runs the submitted tool on the visible packet and fresh hidden packets, then compares both the restored PNG bytes and `restored_manifest.json` against protected reference output.
