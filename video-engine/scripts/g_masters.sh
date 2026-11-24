#!/usr/bin/env bash
# Serie G: ricostruisce i master (uno alla volta) dopo una modifica a sorgente, mappa delle inquadrature o tagli; poi lampi e mento.
# Uso: scripts/g_masters.sh G1-brivido G2-strati ...
cd "$(dirname "$0")/.."
for ID in "$@"; do
  echo "=== MASTER $ID $(date +%H:%M:%S)"
  npx tsx scripts/f_cfg.ts "$ID" | tail -1
  python3 scripts/cn_master_shots.py "work/ytcn26/$ID.json" > "work/ytcn26/${ID}_master.log" 2>&1; head -1 "work/ytcn26/${ID}_master.log"
  python3 scripts/f_flash.py "public/ytcn26/masters/$ID.mp4" | tail -1
  case "$ID" in G5*|G6*|G7*|G8*) ;; *) ../.claude/skills/effects/.venv/bin/python scripts/cn_facecheck.py "public/ytcn26/masters/$ID.mp4" 0.52 2>/dev/null | tail -1;; esac
done
echo "=== MASTERS FINISHED $(date +%H:%M:%S)"
