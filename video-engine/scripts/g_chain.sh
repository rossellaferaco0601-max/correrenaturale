#!/usr/bin/env bash
# Serie G: catena di render che aspetta (a) la fine della coda precedente e (b) il master di ogni reel, poi lancia f_all.sh un reel alla volta.
# Uso: scripts/g_chain.sh "<testo da aspettare in pgrep, o ->" G5-climber:v2 G6-ponte:v3 ...
cd "$(dirname "$0")/.."
PREV="$1"; shift
if [ "$PREV" != "-" ]; then while pgrep -f "$PREV" >/dev/null; do sleep 4; done; fi
for item in "$@"; do
  ID="${item%%:*}"
  until grep -q "^$ID.mp4: ✓\|MASTERS FINISHED" out/ytcn26_masters.log; do sleep 4; done
  sleep 2
  scripts/f_all.sh "$item" | grep -v "ALL FINISHED"
done
echo "=== CHAIN FINISHED $(date +%H:%M)"
