#!/usr/bin/env bash
# Modelli liberi per le rappresentazioni 3D (non stanno nel repository): corpo umano MakeHuman (CC0) con scheletro e pesi, più due
# modelli degli esempi di three.js. Uso: scripts/b3d/fetch.sh   (da video-engine; serve numpy nel Python di Blender:
#   python3.12 -m pip install --break-system-packages --target /usr/local/lib/python3.12/dist-packages numpy)
set -e; cd "$(dirname "$0")/../.."; mkdir -p work/b3d/mh work/b3d/models
B=https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data
for f in 3dobjs/base.obj rigs/default.mhskel rigs/default_weights.mhw targets/macrodetails/caucasian-male-young.target targets/macrodetails/universal-male-young-maxmuscle-averageweight.target; do
  mkdir -p "work/b3d/mh/$(dirname $f)"; [ -s "work/b3d/mh/$f" ] || curl -sSL --retry 3 -o "work/b3d/mh/$f" "$B/$f"
done
T=https://raw.githubusercontent.com/mrdoob/three.js/r160/examples/models/gltf
for f in Xbot.glb LeePerrySmith/LeePerrySmith.glb; do [ -s "work/b3d/models/$(basename $f)" ] || curl -sSL --retry 3 -o "work/b3d/models/$(basename $f)" "$T/$f"; done
ls -la work/b3d/mh/3dobjs work/b3d/models
