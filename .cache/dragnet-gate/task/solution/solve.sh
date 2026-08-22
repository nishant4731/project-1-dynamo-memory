#!/bin/bash
# Reference (Oracle) solution: install the restitch where the instruction says it
# goes, then run it against the live dragnet, which is restorable from the spare.
set -euo pipefail
install -m 0755 /solution/dragnet_restitch.py /app/dragnet_restitch.py
python3 /app/dragnet_restitch.py /app/data/dragnet
