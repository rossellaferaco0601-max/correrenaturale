"""Render delle rappresentazioni 3D della serie G: ogni «set» ha la sua inquadratura e le sue fasi (cicli di N fotogrammi che si chiudono).
Uso: blender -b -P scripts/b3d/render.py -- <set> cartella_uscita [fase ...] [--still]     set: g1 g3 g4 g9 g10 g12
Fotogrammi già presenti non vengono rifatti (ripresa dopo un'interruzione). B3D_SAMPLES regola i campioni (default 64)."""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import mh, runner, poses
A = args(); SET, out = A[0], A[1]; still = "--still" in A; want = [a for a in A[2:] if not a.startswith("--")]
N = 40
sc = reset(res=600, samples=int(os.environ.get("B3D_SAMPLES", 64)))
r = runner.build(); arm = r["arm"]
key = light("key", (-2.2, -3.0, 2.2), 300, 2.5, (1.0, 0.96, 0.9)); fill = light("fill", (2.6, -2.2, 0.8), 130, 3.0, (0.85, 0.95, 1.0))
rim = light("rim", (0.8, 2.6, 1.8), 520, 1.6, (0.75, 1.0, 0.6)); rim2 = light("rim2", (-1.6, 2.2, 1.2), 420, 1.6, (0.9, 1.0, 0.85))
for l in (key, fill, rim, rim2): look_at(l, (0, 0, 0.35))
cam = camera((0.78, -2.95, 0.5), (0, 0, 0.33), lens=66)
CAMS = {
    "bust": ((0.56, -2.05, 0.60), (0, 0, 0.405)),      # dalla coscia in su: si leggono capi, mani, testa
    "body": ((0.78, -2.9, 0.42), (0, 0, 0.2)),         # fino sotto il ginocchio: corsa sul posto
    "full": ((1.1, -3.95, 0.32), (0, 0, 0.2)),          # figura intera con le braccia sopra la testa (jumping jack)
    "low": ((1.6, -3.75, 0.12), (0, -0.05, 0.05)),      # figura intera accovacciata (squat), di tre quarti
    "side": ((3.9, -1.5, 0.2), (0, 0, 0.05)),          # figura intera quasi di profilo (camminata, corsa leggera)
    "head": ((0.95, -0.36, 0.82), (0, -0.085, 0.795)),  # testa e collo di profilo (respirazione dal naso)
}
skin = bpy.data.materials["pelle"].node_tree.nodes["Principled BSDF"]
def mood(kind):
    skin.inputs["Base Color"].default_value = (*{"hot": (0.62, 0.17, 0.10), "cold": (0.36, 0.26, 0.24)}.get(kind, runner.SKIN), 1)
    rim.data.color = {"hot": (1.0, 0.25, 0.08), "cold": (0.45, 0.72, 1.0), "warm": (1.0, 0.55, 0.12)}.get(kind, (0.75, 1.0, 0.6))
    rim.data.energy = {"hot": 900, "cold": 800, "warm": 900}.get(kind, 520)
    fill.data.color = {"cold": (0.6, 0.8, 1.0), "hot": (1.0, 0.8, 0.7), "warm": (1.0, 0.9, 0.75)}.get(kind, (0.85, 0.95, 1.0))
br = lambda p: 0.5 - 0.5 * math.cos(2 * math.pi * p); sw = lambda p, a=1.2: a * math.sin(2 * math.pi * p)
# fase: (inquadratura, capi, atmosfera, posa in funzione della fase 0..1 del ciclo)
SETS = {
    "g1": {
        "over_0": ("bust", [], None, lambda p: poses.stand(arm, br(p), sw(p))),
        "over_1": ("bust", ["gilet"], None, lambda p: poses.stand(arm, br(p), sw(p), a=44)),
        "over_2": ("bust", ["giacca", "guanti", "fascia"], None, lambda p: poses.bulky(arm, br(p), sw(p))),
        "over_3": ("bust", ["piumino", "guanti", "cappello"], None, lambda p: poses.bulky(arm, br(p), sw(p, 1.5))),
        "over_4": ("bust", ["piumino", "guanti", "cappello"], "hot", lambda p: poses.hot(arm, p)),
        "warm_0": ("body", [], "cold", lambda p: poses.cold(arm, p)),
        "warm_1": ("body", [], None, lambda p: poses.run(arm, (p * 2) % 1.0, 0.7)),
        "warm_2": ("body", [], "warm", lambda p: poses.run(arm, (p * 2) % 1.0, 1.0)),
    },
    "g3": {
        "mani_0": ("bust", [], "cold", lambda p: poses.show_hands(arm, p)),
        "mani_1": ("bust", ["guanti", "fascia"], None, lambda p: poses.show_hands(arm, p)),
        "mani_2": ("bust", ["guanti", "cappello"], "warm", lambda p: poses.show_hands(arm, p)),
    },
    "g4": {
        "casa_0": ("full", [], "cold", lambda p: poses.stand(arm, br(p), sw(p))),
        "casa_1": ("full", [], None, lambda p: poses.jack(arm, (p * 2) % 1.0)),
        "casa_2": ("full", [], "warm", lambda p: poses.jack(arm, (p * 2) % 1.0)),
    },
    "g9": {
        "passo_0": ("side", ["guanti", "fascia"], None, lambda p: poses.run(arm, (p * 1) % 1.0, 0.32, lean=2)),
        "passo_1": ("side", ["guanti", "fascia"], "warm", lambda p: poses.run(arm, (p * 2) % 1.0, 0.62, lean=5)),
    },
    "g10": {
        "naso_0": ("head", [], "cold", lambda p: poses.stand(arm, br(p), 0)),
        "naso_1": ("head", [], "warm", lambda p: poses.stand(arm, br(p), 0)),
    },
    "g12": {
        "squat_0": ("low", [], None, lambda p: poses.squat(arm, 0.04 * br(p))),
        "squat_1": ("low", [], None, lambda p: poses.squat(arm, 0.5 - 0.5 * math.cos(math.pi * min(1.0, p * 1.6)))),      # scende una volta sola (non è un ciclo)
        "squat_2": ("low", [], "warm", lambda p: poses.squat(arm, 1.0 - 0.035 * br(p))),
    },
}
os.makedirs(out, exist_ok=True)
for name, (cm, wear, m, pose) in SETS[SET].items():
    if want and name not in want: continue
    runner.show(r, *wear); mood(m); cam.location, tgt = CAMS[cm]; look_at(cam, tgt)
    for f in ([0, 8, 20] if still else range(N)):
        fp = os.path.join(out, f"{name}_{f:03d}.png")
        if os.path.exists(fp) and not still: continue
        pose(f / N); render(fp)
    print("FASE", name, flush=True)
