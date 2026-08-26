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
