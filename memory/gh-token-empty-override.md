---
name: gh-token-empty-override
description: `export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"` in a fresh shell exports an empty token and breaks a working gh keyring login with 401.
metadata:
  type: feedback
---

In a shell where neither `GH_TOKEN` nor `NISHANT_GH_TOKEN` is set, the standard preamble
`export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"` exports `GH_TOKEN=""`. An empty `GH_TOKEN`
**overrides** the keyring credential, so every `gh` call returns `HTTP 401: Requires
authentication` even though `gh auth status` shows a logged-in account.

**Why:** it looks exactly like a private-repo permission problem or a platform-side auth outage,
and the Dynamo playbook trains you to read 401 as infrastructure.

**How to apply:** when `gh` starts 401-ing mid-session, first run `env | grep GH_TOKEN` and
`gh auth status`. If the token is empty, `unset GH_TOKEN` and retry before concluding anything
about the platform. Only use the export when the secret actually exists.
