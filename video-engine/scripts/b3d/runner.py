"""Il corridore 3D della serie G: corpo MakeHuman vestito da corsa (maglia termica scura, calzamaglia, scarpe), capelli scuri ricci.
build() -> dict con i pezzi; i capi in più (gilet, giacca, piumino, guanti, cappello, fascia) si creano nascosti e si mostrano per fase."""
import bpy, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import mh

SKIN = (0.40, 0.235, 0.15)
def _lin(y, pts):
    """interpolazione a tratti: pts = [(y, valore), ...] in ordine di y"""
    if y <= pts[0][0]: return pts[0][1]
    for (a, va), (b, vb) in zip(pts[:-1], pts[1:]):
        if y <= b: return va + (vb - va) * (y - a) / (b - a)
    return pts[-1][1]
# attaccatura dei capelli (quota minima in funzione di y: fronte a y negativo, nuca a y positivo); testa: naso a y -0,176, nuca +0,045, cima z 0,93
HAIRLINE = [(-0.11, 0.888), (-0.075, 0.852), (-0.035, 0.842), (-0.01, 0.80), (0.02, 0.775)]
CAPLINE = [(-0.11, 0.874), (-0.075, 0.842), (-0.045, 0.79), (0.02, 0.785)]

def noise_tex(name, kind="CLOUDS", scale=0.05):
    t = bpy.data.textures.new(name, kind); t.noise_scale = scale; return t

def build():
    h = mh.human(muscle=0.3); arm, body, suit = h["arm"], h["body"], h["suit"]
    body.data.materials.append(mat("pelle", SKIN, rough=0.55))
    h["eyes"].data.materials.append(mat("occhi", (0.03, 0.02, 0.015), rough=0.7))
    bpy.data.objects.remove(h["hair"])
    # capelli: calotta ricavata dal cuoio capelluto, gonfiata e mossa (ricci)
    scalp = lambda co: co.z > _lin(co.y, HAIRLINE)
    hair = mh.part(body, "capelli", scalp); hair.data.materials.clear(); hair.data.materials.append(mat("capelli", (0.012, 0.009, 0.007), rough=0.9))
    mh.thicken(hair, 0.02, sub=2)
    d = hair.modifiers.new("ricci", "DISPLACE"); d.texture = noise_tex("ricci", "CLOUDS", 0.022); d.strength = 0.03; d.mid_level = 0.35; d.texture_coords = "LOCAL"
    # barba corta: mento e mascella un po' più scuri
    beard = mh.part(body, "barba", lambda co: 0.69 < co.z < 0.781 and ((co.y < -0.05 and co.z < 0.772) or (abs(co.x) > 0.05 and -0.105 < co.y < -0.035)) and not (abs(co.x) < 0.026 and 0.742 < co.z < 0.764 and co.y < -0.148))
    beard.data.materials.clear(); beard.data.materials.append(mat("barba", (0.035, 0.024, 0.018), rough=0.95)); mh.thicken(beard, 0.003, sub=2)
    # abbigliamento di base dalla tuta: maglia termica, calzamaglia, scarpe
    top = mh.part(suit, "maglia", lambda co: co.z > 0.06); top.data.materials.append(mat("maglia", (0.035, 0.04, 0.038), rough=0.6)); mh.thicken(top, 0.004)
    legs = mh.part(suit, "calzamaglia", lambda co: -0.735 < co.z <= 0.13); legs.data.materials.append(mat("calzamaglia", (0.018, 0.02, 0.019), rough=0.5)); mh.thicken(legs, 0.0035)
    shoes = mh.part(suit, "scarpe", lambda co: co.z <= -0.725); shoes.data.materials.append(mat("scarpe", (0.75, 0.78, 0.72), rough=0.4)); mh.thicken(shoes, 0.012)
    torso = lambda co: 0.10 < co.z < 0.665 and abs(co.x) < 0.205 - max(0, 0.50 - co.z) * 0.0
    upper = lambda co: co.z > 0.07
    gilet = mh.part(suit, "gilet", torso); gilet.data.materials.append(mat("gilet", (0.16, 0.50, 0.04), rough=0.45)); mh.thicken(gilet, 0.016)
    jacket = mh.part(suit, "giacca", upper); jacket.data.materials.append(mat("giacca", (0.40, 0.62, 0.78), rough=0.35)); mh.thicken(jacket, 0.028)
    puffy = mh.part(suit, "piumino", upper); puffy.data.materials.append(mat("piumino", (0.85, 0.30, 0.10), rough=0.5)); mh.thicken(puffy, 0.062, sub=2)
    q = puffy.modifiers.new("trapunta", "DISPLACE"); tx = noise_tex("trapunta", "WOOD", 0.25); tx.wood_type = "BANDS"; q.texture = tx; q.strength = 0.03; q.mid_level = 0.5; q.texture_coords = "LOCAL"; q.direction = "NORMAL"
    hand = lambda co: abs(co.x) > 0.455 or (abs(co.x) > 0.40 and co.z < 0.335)
    gloves = mh.part(body, "guanti", hand); gloves.data.materials.clear(); gloves.data.materials.append(mat("guanti", (0.16, 0.50, 0.04), rough=0.5)); mh.thicken(gloves, 0.006, sub=1)
    cap = mh.part(body, "cappello", lambda co: co.z > _lin(co.y, CAPLINE)); cap.data.materials.clear(); cap.data.materials.append(mat("cappello", (0.16, 0.50, 0.04), rough=0.6)); mh.thicken(cap, 0.03, sub=2)
    band = mh.part(body, "fascia", lambda co: _lin(co.y, CAPLINE) - 0.004 < co.z < _lin(co.y, [(-0.11, 0.915), (-0.05, 0.885), (0.02, 0.865)])); band.data.materials.clear(); band.data.materials.append(mat("fascia", (0.16, 0.50, 0.04), rough=0.6)); mh.thicken(band, 0.016, sub=1)
    suit.hide_render = True
    extra = {"gilet": gilet, "giacca": jacket, "piumino": puffy, "guanti": gloves, "cappello": cap, "fascia": band}
    for o in extra.values(): o.hide_render = True
    return {"arm": arm, "body": body, "hair": hair, "beard": beard, "top": top, "legs": legs, "shoes": shoes, **extra}

def show(r, *names):
    for n in ("gilet", "giacca", "piumino", "guanti", "cappello", "fascia"): r[n].hide_render = n not in names
    r["hair"].hide_render = "cappello" in names

def rest(arm):
    for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
    bpy.context.view_layer.update()

def arms_down(arm, a=46, bend=14):
    """Dalla posa a braccia aperte: braccia lungo i fianchi, gomiti appena piegati."""
    for s, sg in (("L", 1), ("R", -1)):
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * a); mh.turn(arm, f"lowerarm01.{s}", "X", -bend)
