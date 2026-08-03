# Cloud Agent Docker And Harbor Setup

Use this on Cursor Cloud Agent VMs for every Dynamo task when local Harbor oracle/nop is required.

Cloud Agent environments are often nested containers (`/.dockerenv` present) with cgroup v2 quirks. Docker Desktop assumptions from a laptop do not apply.

## Install

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2
# Harbor CLI (example)
pip install --user harbor
# confirm
harbor --version
docker --version
docker compose version
```

Add the user to the `docker` group when possible, or chmod the socket after dockerd starts:

```bash
sudo chmod 666 /var/run/docker.sock
```

## Start dockerd (vfs storage)

Default overlay/storage often fails on these VMs. Prefer `vfs`:

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json >/dev/null <<'EOF'
{
  "storage-driver": "vfs",
  "iptables": false,
  "ip-forward": false,
  "bridge": "none"
}
EOF

sudo pkill dockerd 2>/dev/null || true
sudo rm -f /var/run/docker.pid
sudo dockerd --config-file /etc/docker/daemon.json >/tmp/dockerd.log 2>&1 &
sleep 4
sudo chmod 666 /var/run/docker.sock
docker info
docker run --rm --privileged --cgroupns=host hello-world
```

Notes:

- `--storage-driver=vfs` is slower/larger but reliable when overlay is unavailable.
- Nested cgroup v2 can break plain `docker run` / Compose with:
  `cannot enter cgroupv2 ... with domain controllers -- it is in threaded mode`.
- Prefer `--privileged --cgroupns=host` for manual validation containers when that error appears.
- Do not treat a Harbor Compose cgroup failure as a task defect if the same image passes a manual oracle/nop container run.

## Harbor oracle / nop

From the task repo root:

```bash
harbor run -p task --agent oracle
harbor run -p task --agent nop
```

Expected:

- Oracle reward `1.0`
- Nop reward `0.0` (or below full reward)

If Harbor Compose fails only on cgroup start, use the manual fallback below and record that limitation in the PR/notes. Remote Dynamo CI still runs real Harbor.

## Manual Docker fallback (oracle / nop)

When Harbor cannot start Compose containers on the Cloud VM:

```bash
# build the task image
docker build -t dynamo-task-local task/environment

# ORACLE: mount solution RO, tests RW (verifier may chmod /tests)
docker run --rm --privileged --cgroupns=host \
  -v "$PWD/task/solution:/solution:ro" \
  -v "$PWD/task/tests:/tests" \
  dynamo-task-local bash -lc '
set -euo pipefail
bash /solution/solve.sh
bash /tests/test.sh
echo REWARD:$(cat /logs/verifier/reward.txt)
'

# NOP: no solve.sh
docker run --rm --privileged --cgroupns=host \
  -v "$PWD/task/solution:/solution:ro" \
  -v "$PWD/task/tests:/tests" \
  dynamo-task-local bash -lc '
set +e
mkdir -p /app/output
bash /tests/test.sh
echo REWARD:$(cat /logs/verifier/reward.txt)
'
```

Mount `/tests` read-write. Read-only mounts break verifiers that `chmod /tests` before dropping privileges.

## Pre-push checklist for Cloud Agents

1. Memory repo loaded (`nishant4731/project-1-dynamo-memory`).
2. Task edits complete; visible fixtures regenerated if generators changed.
3. Local/static checks (`py_compile`, `git diff --check`, base-image script when present).
4. Docker oracle reward `1` and nop reward `0` (Harbor or manual fallback).
5. Commit only intended task files; keep `jobs/` ignored.
6. Push the fork `submission` branch; do not force-push unless required and explained.
7. If a reusable infra lesson appeared, update `PROJECT_MEMORY.md` here and push `main`.

## GitHub auth reminder

- Cloud Agents may start as `cursor` bot. Private upstream Dynamo org repos need the human fork owner account (`nishant4731` or the task owner).
- `gh auth login --web` device codes expire / get overwritten when the bot token becomes active again. Re-check `gh api user --jq .login` before private PR/check queries.
- Fork git remotes may already include an `x-access-token` for push even when `gh` is bot-scoped; verify with a dry `git push` rather than assuming `gh` identity equals git push identity.
