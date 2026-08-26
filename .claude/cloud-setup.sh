#!/usr/bin/env bash
# Setup script for Claude Code cloud sessions (claude.ai/code).
#
# Paste the contents of this file into the environment's "Setup script" field
# at claude.ai/code -> environment selector -> settings icon.
#
# Contract imposed by the platform (see CLAUDE_CLOUD_SETUP.md):
#   - runs as ROOT on Ubuntu 24.04 x86_64, before Claude Code launches
#   - MUST exit 0, or the session refuses to start
#   - MUST finish in ~5 min, or the environment cache fails to build
#   - result is snapshotted to disk and reused; running processes are NOT kept
#
# Deliberately does NOT do what .cursor/install-docker.sh does:
#   - no docker.io install: docker, dockerd and compose are pre-installed
#   - no /etc/docker/daemon.json rewrite: the stock daemon works here, and the
#     Cursor vfs + "bridge": "none" config would downgrade storage and break
#     container networking. Only fall back to vfs if the stock daemon is dead.
#   - no GH_TOKEN plumbing: GitHub goes through a proxy and gh is pre-authed.

set -x
export DEBIAN_FRONTEND=noninteractive

# --- Harbor CLI + apt extras, in parallel to stay inside the time budget -----
(
  python3 -m pip install --break-system-packages --upgrade 'harbor>=0.20.0' \
    || pip3 install --break-system-packages 'harbor>=0.20.0' \
    || true
) &
HARBOR_PID=$!

(
  apt-get update -qq \
    && apt-get install -y -qq --no-install-recommends jq rsync \
    || true
) &
APT_PID=$!

wait "$HARBOR_PID" "$APT_PID" 2>/dev/null || true

# harbor may land in a --user style path depending on the pip resolution above
if ! command -v harbor >/dev/null 2>&1; then
  for cand in "$HOME/.local/bin/harbor" /usr/local/bin/harbor; do
    [ -x "$cand" ] && ln -sfn "$cand" /usr/local/bin/harbor && break
  done
fi

# --- Docker: verify, don't reinstall ----------------------------------------
if ! docker info >/dev/null 2>&1; then
  # Daemon not up yet. Try the stock config first.
  (dockerd >/tmp/dockerd.log 2>&1 &)
  for _ in $(seq 1 15); do
    docker info >/dev/null 2>&1 && break
    sleep 1
  done
fi

if ! docker info >/dev/null 2>&1; then
  # Stock daemon genuinely failed. NOW the nested-VM fallback earns its place.
  # Note: no "bridge": "none" here, so compose networking still works.
  mkdir -p /etc/docker
  cat > /etc/docker/daemon.json <<'EOF'
{
  "storage-driver": "vfs"
}
EOF
  pkill dockerd 2>/dev/null || true
  rm -f /var/run/docker.pid
  (dockerd --config-file /etc/docker/daemon.json >/tmp/dockerd.log 2>&1 &)
  for _ in $(seq 1 20); do
    docker info >/dev/null 2>&1 && break
    sleep 1
  done
fi

chmod 666 /var/run/docker.sock 2>/dev/null || true

# --- Standing context: clone the memory repo and point CLAUDE.md at it -------
# A cloud session clones ONLY the task repo, so none of the Dynamo playbooks
# load by default. Cloning here puts them on the VM without adding anything to
# the task repo, so nothing can leak into a PR diff to handshake-project-dynamo.
MEMDIR=/opt/dynamo-memory
if [ -d "$MEMDIR/.git" ]; then
  git -C "$MEMDIR" pull --ff-only >/dev/null 2>&1 || true
else
  git clone --depth 50 https://github.com/nishant4731/project-1-dynamo-memory.git \
    "$MEMDIR" >/dev/null 2>&1 || true
fi

# User-level CLAUDE.md loads in every session and is NOT part of any repo.
# Written to each plausible home so it applies whichever user Claude runs as.
for H in /root "$HOME" /home/ubuntu /home/node; do
  [ -n "$H" ] && [ -d "$H" ] || continue
  mkdir -p "$H/.claude"
  cat > "$H/.claude/CLAUDE.md" <<'CLAUDEMD'
# Dynamo task session (cloud)

The Dynamo playbooks and per-lesson memory are checked out at
`/opt/dynamo-memory`. They are NOT part of the task repo you are working in.

**Before touching the task, read, in this order:**

1. `/opt/dynamo-memory/AGENTS.md` — the canonical list of what else to read.
2. `/opt/dynamo-memory/memory/MEMORY.md` — one-line index of 157 lessons. Open
   only the entries relevant to this task; do not read them all.
3. The `## <Category> / <Subcategory>` section of
   `/opt/dynamo-memory/PROJECT_MEMORY.md` matching this task's `task.toml`
   `[metadata]`, plus
   `/opt/dynamo-memory/memory/dynamo-<category>-<subcategory>-playbook.md`
   if it exists. What clears the gates is subcategory-specific.

`PROJECT_MEMORY.md` is ~686KB. Never read it whole; grep or jump to the section.

**Docker validation in a cloud session.** It works, but not with a plain
`docker build`. Outbound TLS is intercepted by Anthropic's egress gateway CA,
which the VM host trusts but a build container does not, so the Dockerfile's
`pip` layer fails. The procedure, which never modifies the committed Dockerfile,
is in `/opt/dynamo-memory/CLAUDE_CLOUD_SETUP.md`. In short: copy the build
context to `/tmp/ctx`, insert a CA layer into `/tmp/ctx/Dockerfile` only
(install `ca-certificates` first, the base image ships no CA store), keep the
`FROM` digest byte-identical, and build with `-f /tmp/ctx/Dockerfile`. Never use
`--trusted-host` and never disable certificate verification. Start `dockerd`
with `setsid` or it gets reaped when its background task ends.

**Never create a `CLAUDE.md`, `AGENTS.md`, or notes file inside the task repo.**
Those ship to reviewers in the PR diff. This file lives outside every repo for
exactly that reason.
CLAUDEMD
done

# --- Report what the session actually got -----------------------------------
{
  echo "=== cloud-setup report ==="
  docker --version        2>&1 || echo "docker: MISSING"
  docker compose version  2>&1 || echo "compose: MISSING"
  harbor --version        2>&1 || echo "harbor: MISSING"
  python3 --version       2>&1
  gh --version            2>&1 | head -1
  docker info >/dev/null 2>&1 \
    && echo "dockerd: UP ($(docker info --format '{{.Driver}}' 2>/dev/null))" \
    || echo "dockerd: DOWN - see /tmp/dockerd.log"
} > /tmp/cloud-setup-report.txt 2>&1
cat /tmp/cloud-setup-report.txt

# The platform kills the session on any non-zero exit. Never fail here:
# a missing tool is something Claude can diagnose in-session from the report.
exit 0
