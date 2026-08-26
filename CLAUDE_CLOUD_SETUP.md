# Claude Cloud Setup (claude.ai/code)

Companion to `CLOUD_AGENT_DOCKER_HARBOR.md`, which covers **Cursor** Cloud Agent
VMs. This file covers **Claude Code cloud sessions** — Anthropic-hosted VMs
started from claude.ai/code, `claude --cloud`, the mobile app, or a routine.

The two platforms are not interchangeable. Assumptions carried over from the
Cursor setup are the main failure mode; the divergences are listed below.

## One-time setup

Prerequisites: a Pro/Max/Team plan (research preview; Enterprise needs premium
or Chat + Claude Code seats), and a claude.ai login in the CLI — an API key does
not qualify. `/status` must show a claude.ai account under **Login method**.

`gh` is already authenticated as `nishant4731` on this laptop, so use the
terminal path rather than browser onboarding:

```bash
env -u GH_TOKEN -u GITHUB_TOKEN gh auth status
```

Unset `GH_TOKEN` first. An empty `GH_TOKEN` from the
`${GH_TOKEN:-$NISHANT_GH_TOKEN}` preamble overrides the keyring and surfaces as
a bogus 401 (see memory: "Empty GH_TOKEN masquerades as 401").

Then, inside `claude`, run `/web-setup`. It links the local `gh` token to the
Claude account, creates a `Default` environment if none exists, and opens
claude.ai/code. Afterwards `claude --cloud` starts cloud sessions from the
terminal.

## Environment configuration

Set the environment's **Setup script** to the contents of
[.claude/cloud-setup.sh](.claude/cloud-setup.sh).

Platform contract for that script:

- runs as **root** on Ubuntu 24.04 x86_64, before Claude Code launches
- **must exit 0** — a non-zero exit means the session refuses to start
- **must finish in ~5 min** — over budget, the environment cache fails to build
  and sessions hang or die with a generic container error
- the result is snapshotted to disk and reused by later sessions; installed
  packages and pulled images persist, **running processes do not**

Network access: set to **Custom**, tick **Also include default list**, and list
`*.docker.com` and `*.docker.io`. **Trusted alone is not enough** — it reaches
Docker Hub's registry but not its blob CDN, so every image pull dies with a 403.
Measured, see below.

Do **not** put `GH_TOKEN`, `NISHANT_GH_TOKEN`, or any PAT in the environment
variables box. There is no secrets store: anyone using the environment can read
those values. GitHub auth is handled by the platform proxy instead.

## Resource ceilings

4 vCPU / 16 GB RAM / 30 GB disk per session. Large image builds and
memory-hungry verifiers can be stopped by the VM. For anything past that, use
Remote Control to run on this laptop instead.

## Divergences from the Cursor setup — read before reusing anything

**Docker is pre-installed.** `docker`, `dockerd`, and `docker compose` all ship
on the VM. The whole `apt-get install docker.io` step in
`.cursor/install-docker.sh` is dead weight here.

**Do not copy the Cursor `daemon.json`.** That file sets `"storage-driver":
"vfs"` plus `"bridge": "none"` and `"iptables": false`. On a VM where the stock
daemon works, that downgrades storage for no reason and **breaks container
networking**, which will take down Harbor Compose. `.claude/cloud-setup.sh`
therefore verifies the stock daemon first and only falls back to vfs (without
`bridge: none`) if the daemon is genuinely dead.

**GitHub auth is not your problem here.** `gh` is pre-installed and reads a
proxy-supplied `GH_TOKEN` automatically; real credentials never reach the VM.
There is no `gh auth login`, no Runtime Secret, and no Cursor `url.*.insteadOf`
rewrite injecting `x-access-token` for `cursor[bot]`. Sections 2 and 6 of
`FORK_AND_PUSH_GUIDE.md` do not apply to Claude cloud sessions.

**Push protection changes the fork workflow.** `git push` works only against the
session's *current working branch*, and GitHub API requests reach only the
repositories *attached to the session*. Consequences:

- Attach the **fork** (`utkarsha01/<task-repo>` or `nishant4731/<task-repo>`) as
  a session repository and start the session on the `submission` branch. The
  clone-upstream-then-add-a-`fork`-remote variant in `FORK_AND_PUSH_GUIDE.md`
  §3 will not push.
- Attach `nishant4731/project-1-dynamo-memory` as a second repository in the
  same session if the task needs the memory repo. Sessions support multiple
  repositories; unattached repos return 403.

**GraphQL is restricted.** Only a pinned set of pull-request operations is
served; everything else returns 403 with `This GraphQL query is not enabled for
this session`. A `GH_TOKEN` you supply yourself gets the same 403. Use the REST
fallback, `gh api repos/{owner}/{repo}/...`. Any Dynamo tooling reaching for
Projects v2 or other GraphQL-only APIs needs rewriting.

**Nothing from `~/.claude/` carries over.** User-level skills, agents, commands,
and the auto-memory playbooks under
`~/.claude/projects/-Users-utkarsha-Documents-Project-1/memory/` do not exist in
a cloud session. Only committed repo files load. This is exactly why
`CLAUDE.md` requires every accepted playbook to be written into
`PROJECT_MEMORY.md` and pushed — that copy is the only one a cloud session sees.

## Measured on Anthropic-hosted VMs (2026-08-26)

Two sessions on `nishant4731/project-1-dynamo-memory`, environment `Default`.

**`--privileged --cgroupns=host` works.** `docker run --rm --privileged
--cgroupns=host hello-world` printed `Hello from Docker!`. The Dynamo manual
oracle/nop fallback in `CLOUD_AGENT_DOCKER_HARBOR.md` is therefore viable in a
cloud session; validation does not have to stay on the laptop.

**The stock daemon uses overlayfs**, reported as `dockerd: UP (overlayfs)`. The
vfs fallback in `.claude/cloud-setup.sh` never fires, which confirms that
copying the Cursor `daemon.json` would have downgraded storage and disabled
container networking for nothing.

Versions seen: Docker 29.3.1, Docker Compose v5.1.1, Python 3.11.15.

### Trusted network access is NOT enough to pull from Docker Hub

First run failed with exit 125:

```
docker: unknown: failed to copy: httpReadSeeker: failed open: unexpected status
from GET request to https://production.cloudfront.docker.com/registry-v2/... :
403 Forbidden
```

The manifest fetch succeeded and only the blob fetch was refused: Docker Hub's
registry host is on the Trusted allowlist but its CloudFront blob CDN is not.
Note this failure aborts before container creation, so it is **not** evidence
about `--privileged`; it only looks like one.

Fix applied to the `Default` environment — network access **Custom**, with
**Also include default list** checked, and:

```
*.docker.com
*.docker.io
```

The same pull then succeeded. Any environment used for Dynamo work needs this;
a fresh environment left on Trusted will fail every image pull.

### harbor is not installed, and that is not a regression

The setup script reports `harbor: MISSING`. The `harbor` PyPI package does not
provide the Dynamo Harbor CLI, `harbor` is not installed on the laptop either,
and the local gate (`.tools/vitrail/gate.sh`) drives oracle/nop with plain
`docker run`. The `pip install harbor || true` line in
`.cursor/install-docker.sh` has always been failing silently. Use the manual
Docker fallback, not `harbor run`.

### gh is missing from the setup script's PATH

The setup script logged `gh: command not found`, even though `gh` is
pre-installed for the session itself. The init script runs in a different PATH
context, so **a setup script cannot call `gh`**. Do GitHub work in the session,
where `gh` resolves and reads the proxy-supplied token.

### The memory mirror works

`ls memory/*.md | wc -l` returned **157**, and `head -5 memory/MEMORY.md`
rendered the index. The auto-memory mirror is readable from cloud sessions.


## Docker builds do NOT work in cloud sessions (measured 2026-08-26)

Establishing this took ~11 minutes of session time on `dynamo-79656fb`. Do not
re-derive it. Three layers, in the order they block:

1. **`dockerd` has no `HTTPS_PROXY`.** It egresses directly instead of through
   the agent proxy, so the environment's Allowed-domains list does not apply to
   `docker pull`. `curl` through the proxy reaches a host that `docker` cannot.
2. **ECR Public rate-limits the shared egress IP**, returning
   `429 TOOMANYREQUESTS / "Data limit exceeded"` for anonymous pulls.
3. **The blocker: TLS interception breaks in-container installs.** Outbound TLS
   is intercepted by `Anthropic ... sandbox-egress-gateway-production Egress
   Gateway CA`. The VM **host** trusts that CA; a **build container** carries
   only its own CA bundle. So the `pip install pytest==8.4.1 ...` layer in
   `task/environment/Dockerfile` dies on an untrusted certificate.

Fixing (3) needs either an exemption from TLS interception for `pypi.org` and
`files.pythonhosted.org`, which is not a user-configurable setting, or injecting
the egress CA into the build container, which means editing the Dockerfile that
ships to Handshake in the PR diff. Neither is acceptable.

What *does* work: running containers. `--privileged --cgroupns=host` is fine and
an image already on disk runs normally. It is specifically **building** an image
that performs network installs that cannot be done.

**Therefore: Harbor/Docker oracle-nop validation stays on the laptop.**

## The cloud middle path: run the gate on the VM host

TLS interception only bites *inside build containers*. The host trusts the
gateway CA and already has Python, so the task's own scripts can run there. A
cloud session runs as root, so the container's absolute paths can be recreated
exactly. For the `dynamo-79656fb` shape:

```bash
pip install --break-system-packages pytest==8.4.1 pytest-json-ctrf==0.3.5
mkdir -p /app/data /logs/verifier /solution /tests
cp -r task/environment/data/. /app/data/
install -m 0444 /app/data/dykework.py \
  "$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')/dykework.py"
cp task/solution/. /solution/ -r
cp task/tests/. /tests/ -r

# ORACLE
bash /solution/solve.sh && bash /tests/test.sh; cat /logs/verifier/reward.txt   # expect 1

# NOP - solve.sh mutates the live reach in place, so restore it first
rm -rf /app/data && mkdir -p /app/data && cp -r task/environment/data/. /app/data/
bash /tests/test.sh; cat /logs/verifier/reward.txt                             # expect 0
```

Adapt the copy steps to whatever the task's own Dockerfile does; read it rather
than assuming this layout.

**This is a pre-flight, not validation. Never report it as a green gate.** It
catches engine bugs, wrong pins, verifier logic errors and missing fixtures. It
does **not** catch:

- the image build itself
- Python version drift (host 3.11 vs `ubuntu:24.04`'s 3.12)
- missing apt packages the image would have installed
- file permissions, the `X_OK` executable-bit abort, and privilege-drop
  behaviour, all of which have cost real cycles before

Do not push a task's first-ever version on a host-run alone; those misses are
exactly the ones that burn a full pipeline cycle.

## Give a cloud session the playbooks: attach this repo, never add CLAUDE.md

A cloud session on a task repo clones **only that repo**. It cannot see
`Project 1`, so none of the playbooks or `memory/` load by default.

**Attach `nishant4731/project-1-dynamo-memory` as a second repository on every
task cloud session.** Sessions support multiple repos, and this brings
`AGENTS.md`, `CLAUDE.md`, `PROJECT_MEMORY.md` and all 157 files in `memory/`
into the session.

**Do not solve this by committing a `CLAUDE.md` into a task repo.** That file
would appear in the PR diff to `handshake-project-dynamo` and expose the
authoring playbook to reviewers. The second-repo attachment achieves the same
thing and ships nothing.
