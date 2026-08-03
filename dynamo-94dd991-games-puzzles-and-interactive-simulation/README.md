# Relayforge Replay

This repository contains a Project Dynamo Harbor task in the Games, Puzzles, and Interactive Simulation category. The agent receives a Relayforge text-game circuit at `/app/relayforge/circuit.json` with rooms, items, calibration turns, fixed quests, and route-planning puzzles. The circuit-local engine constants are intentionally omitted but are recoverable from the calibration rows.

The required submission writes `/app/relay_report.json` for the visible quests and route solutions and `/app/replay_relay.py`, a reusable Python script that can infer constants, replay fixed quests, and solve route-planning puzzles for another valid circuit from `INPUT_CIRCUIT_JSON OUTPUT_JSON`.

Verification checks the visible output exactly, pins the shipped input hash, rejects malformed or symlinked artifacts, and runs the submitted replay script against protected circuits with different worlds, constants, action horizons, and edge cases.
