#!/usr/bin/env bash
# Coda unica dei lavori pesanti (24/11: tre lavori insieme hanno fatto riavviare la macchina). Esegue UNA riga alla volta da work/queue.txt
# (ogni riga è un comando, lanciato da video-engine); le righe si possono aggiungere mentre gira. Log: out/runner.log. Si ferma con work/queue.stop.
cd "$(dirname "$0")/.."; touch work/queue.txt
while [ ! -f work/queue.stop ]; do
  L=$(head -n 1 work/queue.txt)
  if [ -z "$L" ]; then sleep 3; continue; fi
  sed -i '1d' work/queue.txt
  echo ">>> $(date +%H:%M:%S) $L" >> out/runner.log
  bash -c "$L" >> out/runner.log 2>&1
  echo "<<< $(date +%H:%M:%S) fatto: $L" >> out/runner.log
done
