---
name: docker-kill-hits-other-sessions
description: "This machine runs several Dynamo task containers at once — never `docker ps -q | xargs docker kill`; filter by image or --name."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e718b780-7192-426b-b840-e8cfc51901c3
  modified: 2026-08-12T23:38:17.620Z
---

While validating `dynamo-d44c669`, a slow verifier run looked like a hang, and a
blanket `docker ps -q | xargs -r docker kill` cleaned up **six other sessions'**
containers (`shadecast-refit:dev`, `fabric-retime:dev`, `squash-stack:dev`,
`cairn-dev`, `evalgrid:dev`, `dynamo-ratechain-final`) along with mine.

**Why:** Dynamo work on this laptop is parallel — other Claude sessions keep
long-lived task containers alive (`sleep 3600`/`sleep 7200` holders and in-flight
oracle runs). Docker state is shared, unnamespaced, global.

**How to apply:** always name your own containers (`docker run --name atl-oracle
…`) and stop only those, or filter by your image
(`docker ps -q --filter ancestor=<your-image>`). Before assuming a container is
stuck, run `docker ps --format '{{.Names}}\t{{.Image}}'` — a verifier that took
910 s under six-way CPU contention finished in 143 s once the machine was quiet,
so contention, not a hang, is the usual explanation. Related:
[[dynamo-verifier-must-be-idempotent]].
