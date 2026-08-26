---
name: docker-cp-into-existing-dir-nests
description: "`docker cp src_dir container:/dest` NESTS when /dest already exists, so re-copying a tests directory into a live container silently leaves the old code running."
metadata:
  type: reference
---

`docker cp "$G/task/tests" NAME:/tests` behaves differently depending on whether
`/tests` exists in the container:

- **absent** → creates `/tests` with the contents. What you meant.
- **present** → creates `/tests/tests`. The old `/tests/*.py` keeps running, and
  every test, probe sweep and measurement silently reports on **stale code**.

This cost several confusing rounds on `dynamo-2d0d4c3`: a forge fix measured as
having no effect at all (51 malformed records "still" present), a seed search
that returned segment sizes disagreeing with the same slot measured moments
later, and a probe that "survived" against a file that already killed it.

**Use one of these instead:**

    docker cp "$G/task/tests/." NAME:/tests/     # merge into the existing dir
    docker rm -f NAME && docker run -d --name NAME ...   # or just recreate it

Recreating is safest for a measurement container: it also clears any module-level
cache the rig keeps (`rig._CACHE`), which otherwise pins plans built from the
previous corpus.

**The tell:** a change you can see in the repo and in the staged copy but whose
effect does not move at all. Verify with
`docker exec NAME grep -c '<a string from the edit>' /tests/<file>` before
believing any measurement — a zero there means you are measuring the old build,
not a failed fix. Related: [[dynamo-rebuild-base-before-validation-image]], the
same class of stale-layer error one level up.
