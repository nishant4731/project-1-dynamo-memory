# Charged Marble Lattice

This repository contains a Project Dynamo Harbor task in `task/`. The task asks an agent to tune a deterministic charged-marble lattice, simulate signed-charge packet flow, render the resulting flux mosaic as an ASCII PPM image, and ship a reusable solver module.

The fixture is synthetic but models realistic game-tools and rendering QA work: exact tick ordering, packet batching, stateful tile behavior, delayed releases, placement optimization, reports, and raster output must all agree.

Local validation:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```
