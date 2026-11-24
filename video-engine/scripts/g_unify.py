#!/usr/bin/env python3
"""Stacchi dentro la stessa camera (Ross 24/11, G9: «ha degli scatti»). Il video di partenza ha molti tagli fatti restando sulla stessa
camera (pause tolte): se ogni pezzo ha il suo ritaglio, a ogni taglio l'inquadratura si sposta di qualche decina di pixel e sembra uno
scatto. Qui i pezzi consecutivi della stessa camera (volto di grandezza e posizione quasi uguali) ricevono lo STESSO volto medio, quindi
lo stesso ritaglio: al taglio resta solo il piccolo salto di posa dell'originale. Il volto misurato resta in `face0`.
Uso: python3 scripts/g_unify.py work/ytcn26_shots.json"""
import json, sys
p = sys.argv[1]; sh = json.load(open(p))
for s in sh:
    if s.get("face") and "face0" not in s: s["face0"] = list(s["face"])
def same(a, b):
    fa, fb = a.get("face0"), b.get("face0")
    return bool(fa and fb) and abs(fa[3] - fb[3]) / max(fa[3], fb[3]) < 0.085 and abs((fa[0] + fa[2] / 2) - (fb[0] + fb[2] / 2)) < 0.035 and abs(fa[1] - fb[1]) < 0.035
runs, cur = [], [sh[0]]
for a, b in zip(sh[:-1], sh[1:]):
    if same(a, b): cur.append(b)
    else: runs.append(cur); cur = [b]
runs.append(cur); n = 0; worst = 0
for r in runs:
    if len(r) < 2: continue
    w = [x["to"] - x["from"] for x in r]; tot = sum(w)
    m = [sum(x["face0"][i] * wi for x, wi in zip(r, w)) / tot for i in range(4)]
    for x in r:
        worst = max(worst, abs((x["face0"][0] + x["face0"][2] / 2) - (m[0] + m[2] / 2)) * 1920 * 1.78)
        x["face"] = [round(v, 4) for v in m]
    n += 1
json.dump(sh, open(p, "w"))
print(f"{len(sh)} inquadrature, {n} gruppi della stessa camera unificati; spostamento massimo tolto: {worst:.0f} px nel verticale")
