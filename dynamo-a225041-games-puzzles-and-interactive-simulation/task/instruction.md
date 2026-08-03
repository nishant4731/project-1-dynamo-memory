Repair the Signal Bastion round resolver, cooperative route planner, relay stabilizer, replay controller, and effect VM in `/app/repo`.

The complete behavioral contract is in `/app/repo/RULES.md`. Every typed field constraint in that contract is exact (including attack `target` being exactly a string that names a start-snapshot unit). Repair the implementations under `/app/repo/bastion` while preserving the public `resolve_round(state, commands)`, `plan_routes(grid, agents)`, `stabilize_relays(relays, constraints, modulus, target)`, `replay_session(checkpoint, envelopes)`, and `run_program(code, variables, gas)` APIs. The repository includes a small visible pytest suite; run it from `/app/repo` while working.

Do not modify `RULES.md`, the visible tests, or project configuration. Leave the repaired code in `/app/repo` and do not add generated artifacts or dependencies.
