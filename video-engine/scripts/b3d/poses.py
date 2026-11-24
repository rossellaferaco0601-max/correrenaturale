"""Pose e cicli del corridore 3D (funzioni pure della fase: nessun fotogramma chiave). Assi del mondo: la figura guarda verso -Y, la sua sinistra è +X.
Rotazione attorno a X per le ossa che puntano in BASSO (gambe, braccia lungo i fianchi): negativa = in avanti, positiva = indietro.
Per le ossa che puntano in ALTO (schiena, collo, testa) è il contrario: positiva = piegarsi in avanti."""
import math
import mh, runner

S = (("L", 1), ("R", -1))

def stand(arm, breath=0.0, sway=0.0, a=47, elbow=-10):
    """In piedi, braccia lungo i fianchi; breath 0..1 (torace che sale), sway = piccola oscillazione in gradi."""
    runner.rest(arm)
    mh.turn(arm, "spine03", "X", -1.5 * breath); mh.turn(arm, "spine05", "Y", sway)
    for s, sg in S:
        mh.turn(arm, f"clavicle.{s}", "Y", -sg * 3 * breath)
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * a); mh.turn(arm, f"upperarm01.{s}", "X", 4)
        mh.turn(arm, f"lowerarm01.{s}", "X", elbow)
    mh.turn(arm, "head", "X", -2 * breath)

def bulky(arm, breath=0.0, sway=0.0):
    """Imbacuccato: le braccia stanno larghe perché gli strati tengono scostato il braccio."""
    stand(arm, breath, sway, a=40, elbow=-14)

def hot(arm, ph):
    """Accaldato: spalle che salgono e scendono in affanno, testa che ciondola, una mano che si fa aria."""
    b = 0.5 - 0.5 * math.cos(2 * math.pi * ph * 2)
    runner.rest(arm)
    mh.turn(arm, "spine05", "X", 5); mh.turn(arm, "spine03", "X", -3 * b); mh.turn(arm, "head", "X", 9 - 4 * b); mh.turn(arm, "head", "Y", 5 * math.sin(2 * math.pi * ph))
    for s, sg in S:
        mh.turn(arm, f"clavicle.{s}", "Y", -sg * 7 * b)
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * 40)
    mh.turn(arm, "lowerarm01.L", "X", -14)
    # mano destra che sventola davanti al viso
    mh.turn(arm, "upperarm01.R", "X", -38); mh.turn(arm, "lowerarm01.R", "X", -118); mh.turn(arm, "lowerarm01.R", "Z", 28 + 10 * math.sin(2 * math.pi * ph * 4))

def cold(arm, ph, amount=1.0):
    """Infreddolito: braccia strette al petto, spalle alzate, testa incassata, tremito rapido."""
    j = math.sin(2 * math.pi * ph * 8) * amount
    runner.rest(arm)
    mh.shift(arm, "root", (0.004 * j, 0, 0))
    mh.turn(arm, "spine05", "X", 5); mh.turn(arm, "spine02", "X", 9); mh.turn(arm, "spine03", "Z", 1.6 * j)
    mh.turn(arm, "neck01", "X", 8); mh.turn(arm, "head", "X", 4); mh.turn(arm, "head", "Z", 1.2 * j)
    for s, sg in S:
        mh.turn(arm, f"clavicle.{s}", "Y", -sg * 10)
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * 54); mh.turn(arm, f"upperarm01.{s}", "X", -14); mh.turn(arm, f"upperarm01.{s}", "Z", -sg * 10)
        mh.turn(arm, f"lowerarm01.{s}", "X", -72 - (8 if s == "L" else -6)); mh.turn(arm, f"lowerarm01.{s}", "Z", -sg * (74 + 1.5 * j))
    for s, sg in S: mh.turn(arm, f"upperleg01.{s}", "X", -3); mh.turn(arm, f"lowerleg01.{s}", "X", 6)

def run(arm, ph, power=1.0, lean=6):
    """Corsa sul posto: ph 0..1 = un ciclo completo (due appoggi). power regola l'ampiezza (0,5 = corsetta, 1 = corsa)."""
    runner.rest(arm)
    bob = 0.022 * power * abs(math.sin(2 * math.pi * ph)); mh.shift(arm, "root", (0, 0, bob - 0.012))
    mh.turn(arm, "spine05", "X", lean); mh.turn(arm, "spine03", "Z", 7 * power * math.sin(2 * math.pi * ph)); mh.turn(arm, "head", "X", -lean * 0.6)
    for s, sg in S:
        p = 2 * math.pi * ph + (0 if s == "L" else math.pi)
        thigh = -18 - 34 * power * math.sin(p)                       # avanti (negativo) quando sale il ginocchio
        knee = 20 + 62 * power * max(0.0, math.sin(p + 0.9)) + 8
        mh.turn(arm, f"upperleg01.{s}", "X", thigh * 0.9 + 8); mh.turn(arm, f"lowerleg01.{s}", "X", knee)
        mh.turn(arm, f"foot.{s}", "X", -12 * max(0.0, math.sin(p + 0.9)))
        sw = 34 * power * math.sin(p)                                # braccio opposto alla gamba
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * 45); mh.turn(arm, f"upperarm01.{s}", "X", sw + 8)
        mh.turn(arm, f"lowerarm01.{s}", "X", -84 - 10 * math.sin(p))


def show_hands(arm, ph):
    """In piedi con le mani alzate davanti al busto (si devono vedere bene le mani): piccolo movimento delle dita/mani."""
    b = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
    runner.rest(arm); mh.turn(arm, "spine03", "X", -1.5 * b); mh.turn(arm, "head", "X", 6)
    for s, sg in S:
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * 44); mh.turn(arm, f"upperarm01.{s}", "X", -16)
        mh.turn(arm, f"lowerarm01.{s}", "X", -82 - 4 * b); mh.turn(arm, f"lowerarm01.{s}", "Z", -sg * 8)
        mh.turn(arm, f"wrist.{s}", "Z", sg * 10 * math.sin(2 * math.pi * ph))

def jack(arm, ph):
    """Jumping jack: ph 0..1 = un ciclo (chiuso → aperto → chiuso). Braccia che salgono sopra la testa, gambe che si aprono, piccolo salto."""
    u = 0.5 - 0.5 * math.cos(2 * math.pi * ph)          # 0 chiuso, 1 aperto
    runner.rest(arm); mh.shift(arm, "root", (0, 0, 0.05 * math.sin(math.pi * ((ph * 2) % 1.0)) - 0.02 * u))
    for s, sg in S:
        mh.turn(arm, f"upperleg01.{s}", "Y", -sg * 19 * u); mh.turn(arm, f"lowerleg01.{s}", "X", 6 * (1 - u))
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * (47 - 148 * u)); mh.turn(arm, f"lowerarm01.{s}", "X", -10)

def squat(arm, d):
    """Squat naturale profondo: d 0 = in piedi, 1 = accovacciato (talloni a terra, busto in avanti, braccia avanti per l'equilibrio).
    I piedi restano dove sono: dopo la posa il bacino viene riportato in modo che i piedi tornino alla quota e alla posizione di partenza."""
    runner.rest(arm)
    import bpy
    f0 = (arm.matrix_world @ arm.pose.bones["foot.L"].matrix).to_translation().copy()
    th, kn = 118 * d, 146 * d
    mh.turn(arm, "spine05", "X", 34 * d); mh.turn(arm, "spine02", "X", 10 * d); mh.turn(arm, "head", "X", -22 * d)
    for s, sg in S:
        mh.turn(arm, f"upperleg01.{s}", "Y", -sg * 16 * d); mh.turn(arm, f"upperleg01.{s}", "X", -th)
        mh.turn(arm, f"lowerleg01.{s}", "X", kn); mh.turn(arm, f"foot.{s}", "X", -(kn - th))
        mh.turn(arm, f"upperarm01.{s}", "Y", sg * (47 - 10 * d)); mh.turn(arm, f"upperarm01.{s}", "X", -62 * d - 4); mh.turn(arm, f"lowerarm01.{s}", "X", -10 - 30 * d); mh.turn(arm, f"lowerarm01.{s}", "Z", -sg * 20 * d)
    f1 = (arm.matrix_world @ arm.pose.bones["foot.L"].matrix).to_translation()
    mh.shift(arm, "root", (0, f0.y - f1.y, f0.z - f1.z))
