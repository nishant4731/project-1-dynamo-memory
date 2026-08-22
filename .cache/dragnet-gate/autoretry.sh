#!/bin/bash
# Watch the Dynamo Review run; auto close/reopen on infrastructure failures only.
cd "/Users/utkarsha/Documents/Project 1/dynamo-2d0d4c3-security"
REPO=handshake-project-dynamo/dynamo-2d0d4c3-security
RID="$1"
for attempt in $(seq 1 12); do
  echo "=== attempt $attempt · run $RID · $(date +%H:%M) ==="
  while :; do
    st=$(gh run view "$RID" --repo $REPO --json status --jq .status 2>/dev/null)
    [ "$st" = "completed" ] && break
    sleep 180
  done
  concl=$(gh run view "$RID" --repo $REPO --json conclusion --jq .conclusion)
  echo "run $RID concluded: $concl"
  gh run view "$RID" --repo $REPO --json jobs \
    --jq '.jobs[] | select(.name|startswith("review /")) | .name + "=" + (.conclusion // .status)'
  if [ "$concl" = "success" ]; then echo "STATE:PIPELINE-GREEN"; break; fi
  JID=$(gh run view "$RID" --repo $REPO --json jobs --jq '.jobs[]|select(.name=="review / pass2")|.databaseId')
  LOG=$(gh run view --job "$JID" --repo $REPO --log 2>/dev/null | grep -a '##\[error\]' | head -3)
  echo "$LOG"
  P2=$(gh run view "$RID" --repo $REPO --json jobs --jq '.jobs[]|select(.name=="review / pass2")|.conclusion')
  if [ "$P2" = "success" ]; then echo "STATE:PASS2-OK-BUT-LATER-GATE-RED"; break; fi
  if echo "$LOG" | grep -qiE "did not finish within|0 of 0 runs"; then
    REASON="infra: harbor status never reported"
  else
    BD=$(gh pr view 1 --repo $REPO --comments 2>/dev/null | grep -o "Breakdown: [^<]*" | tail -1)
    echo "breakdown: $BD"
    if echo "$BD" | grep -qE "[1-9] infra/setup-timeout"; then
      REASON="infra: sandbox setup"
    else
      echo "STATE:REAL-VERDICT :: $BD"; break
    fi
  fi
  echo "retrigger ($REASON)"
  gh pr close 1 --repo $REPO --comment "Auto-retrigger: \`review / pass2\` failed for an infrastructure reason ($REASON); no task bytes change." >/dev/null 2>&1
  until [ "$(gh pr view 1 --repo $REPO --json state --jq .state)" = "CLOSED" ]; do sleep 5; done
  sleep 15
  gh pr reopen 1 --repo $REPO >/dev/null 2>&1
  OLD=$RID
  until [ "$(gh run list --repo $REPO --workflow 'Dynamo Review' --limit 1 --json databaseId --jq '.[0].databaseId')" != "$OLD" ]; do sleep 10; done
  RID=$(gh run list --repo $REPO --workflow "Dynamo Review" --limit 1 --json databaseId --jq '.[0].databaseId')
  echo "reopened -> new run $RID"
done
echo "AUTORETRY-EXIT"
