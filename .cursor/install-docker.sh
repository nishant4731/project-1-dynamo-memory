#!/usr/bin/env bash
# Idempotent Cloud Agent install: Docker + Compose + Harbor for Dynamo tasks.
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  ca-certificates curl git sudo python3 python3-pip \
  docker.io docker-compose-v2

# Harbor CLI used by Dynamo oracle/nop validation
python3 -m pip install --user --upgrade pip >/dev/null
python3 -m pip install --user 'harbor>=0.20.0' || pip3 install --user 'harbor>=0.20.0' || true
if ! command -v harbor >/dev/null 2>&1; then
  if [ -x "$HOME/.local/bin/harbor" ]; then
    sudo ln -sfn "$HOME/.local/bin/harbor" /usr/local/bin/harbor || true
  fi
fi

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json >/dev/null <<'EOF'
{
  "storage-driver": "vfs",
  "iptables": false,
  "ip-forward": false,
  "bridge": "none"
}
EOF

# Nested Cloud VMs: prefer vfs; overlay often fails.
if id ubuntu >/dev/null 2>&1; then
  sudo usermod -aG docker ubuntu || true
fi

# Do not leave dockerd running across the Build snapshot; start it in "start".
sudo service docker stop 2>/dev/null || true
sudo pkill dockerd 2>/dev/null || true
sudo rm -f /var/run/docker.pid || true

docker --version
docker compose version || true
harbor --version || true
