#!/usr/bin/env bash
# Serie F e G: render + finitura + controlli finali, un reel alla volta (un solo lavoro pesante per volta).
# Per ogni ID:VERSIONE: render grezzo (f_queue.sh), finitura (cn_finish.sh), controlli (f_qa.py: neri e audio; f_flash.py: lampi di un fotogramma).
# Uso: scripts/f_all.sh G2-strati:v2 G1-brivido:v1 ...   (log su stdout; riga finale «=== ALL FINISHED»)
set -uo pipefail
cd "$(dirname "$0")/.."
for item in "$@"; do
  ID="${item%%:*}"; V="${item##*:}"; case "$ID" in G*) Y=ytcn26;; *) Y=ytcn22;; esac
  scripts/f_queue.sh "$item" | grep -v "QUEUE FINISHED"
  # reel senza pannello CTA (24/11: i quattro esercizi G5-G8): niente clic di «Pubblica» da attenuare (CTA_S negativo = finestra oltre la fine)
  case "$ID" in G5-*|G6-*|G7-*|G8-*) export CTA_S=-10;; *) unset CTA_S;; esac
  OUT=out/$Y WK=work/$Y WMODEL=large-v3-turbo scripts/cn_finish.sh "$ID" "$V" 2>&1 | grep -v "^\s*at \|Memory\|docker\|lower amount" | tail -5
  python3 scripts/f_qa.py "out/$Y/consegna/${ID}_${V}.mp4"
  python3 scripts/f_flash.py "out/$Y/consegna/${ID}_${V}.mp4"
  echo "=== FINISHED $ID $V $(date +%H:%M)"
done
echo "=== ALL FINISHED"
