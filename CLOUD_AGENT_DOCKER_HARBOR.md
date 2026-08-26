# Cloud Agent Docker And Harbor Setup

Use this on Cursor Cloud Agent VMs for every Dynamo task when local Harbor oracle/nop is required.

**Scope: Cursor Cloud Agent VMs and this laptop.** Claude Code cloud
sessions (claude.ai/code) are a different platform — Docker is pre-installed,
GitHub auth goes through a proxy, and the `daemon.json` below would break
container networking there. See `CLAUDE_CLOUD_SETUP.md` for that path.

Cloud Agent environments are often nested containers (`/.dockerenv` present) with cgroup v2 quirks. Docker Desktop assumptions from a laptop do not apply.

## Make Docker available for ALL chats (required)

Docker is **not** global unless a Cloud Environment Build is saved and active.

Canonical config lives in this repo:

- `.cursor/environment.json`
- `.cursor/install-docker.sh`

### One-time dashboard steps (Nishant)

1. Open [Cloud Agents → Environments](https://cursor.com/dashboard/cloud-agents#environments).
2. Create or edit a **personal** environment (name e.g. `dynamo-docker`).
3. Add repos you use for Dynamo work:
   - `nishant4731/project-1-dynamo-memory`
   - each `nishant4731/dynamo-*` task fork you care about (multi-repo / repo group)
4. Set **Install** to: `bash .cursor/install-docker.sh`  
   (or paste the same script if the memory repo is not the workspace root)
5. Set **Start** to start `dockerd` with `vfs` (see `.cursor/environment.json` `start`).
6. Run a Build until it is **SUCCEEDED**, then **Enable / activate** that Build.
7. Confirm a **new** Cloud Agent chat shows the environment and `docker info` works immediately.

Notes:

- Draft / `trigger-environment-build` builds do **not** become the default until you save/activate in the dashboard.
- Repo `.cursor/environment.json` wins over personal/team envs for that repo.
- There is no automatic “every GitHub repo forever” switch; attach the Dynamo repos (or keep this config in each task template).

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

## GitHub auth (nishant only, all repos)

Policy for Nishant Dynamo Cloud Agents:

1. **Do not expect `gh auth login` from a previous chat to still work.** Each Cloud Agent VM is fresh.
2. Persist nishant with a dashboard Runtime Secret: `GH_TOKEN` or `NISHANT_GH_TOKEN` (PAT as `nishant4731`). See `FORK_AND_PUSH_GUIDE.md`.
3. At chat start: `export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"` then `gh api user --jq .login` → `nishant4731`.
4. Ask for interactive device login only if that secret is missing.
5. Remove Cursor managed `url.*.insteadof` rewrites that inject `x-access-token` for `cursor[bot]` on `github.com`.
6. Point remotes at plain `https://github.com/...` URLs and use `gh auth git-credential` / the PAT for pushes that must be nishant.

Quick verify:

```bash
export GH_TOKEN="${GH_TOKEN:-$NISHANT_GH_TOKEN}"
gh api user --jq .login                    # nishant4731
git config --global --get-regexp '^url\.'  # should be empty / no x-access-token rewrite
```

If managed rewrites reappear mid-session, clear them again before pushing.
