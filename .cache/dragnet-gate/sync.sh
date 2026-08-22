#!/bin/bash
set -eu
G="/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate"
R="/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security"
rsync -a --delete "$R/task/" "$G/task/"
cd "$G/task/environment" && docker build -q -t dragnet-restitch:local . >/dev/null
echo "image rebuilt from $R"
