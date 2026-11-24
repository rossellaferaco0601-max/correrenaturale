"""Corpo umano realistico per le rappresentazioni 3D: mesh base di MakeHuman (CC0) con scheletro e pesi «default», costruito in Blender.
File in work/b3d/mh (scaricati dal repository makehumancommunity/makehuman: 3dobjs/base.obj, rigs/default.mhskel, rigs/default_weights.mhw,
targets/macrodetails/*). La mesh base porta anche le superfici d'aiuto: `helper-tights` (una tuta aderente su tutto il corpo: qui diventa
l'abbigliamento da corsa, a strati) e `helper-hair` (calotta dei capelli).
human() -> dict con armatura e oggetti: body, suit (tuta), hair, eyes. Unità: metri, Z in alto, la figura guarda verso -Y."""
import bpy, json, os, math
from mathutils import Vector, Matrix, Quaternion

MH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "work", "b3d", "mh")
S = 0.1   # decimetri -> metri
conv = lambda v: Vector((v[0] * S, -v[2] * S, v[1] * S))

def _load(targets):
    verts, groups, g = [], {}, None
    for l in open(os.path.join(MH, "3dobjs/base.obj")):
        if l.startswith("v "): verts.append([float(x) for x in l.split()[1:4]])
        elif l.startswith("g "): g = l.split()[1]; groups.setdefault(g, [])
        elif l.startswith("f "): groups[g].append([int(t.split("/")[0]) - 1 for t in l.split()[1:]])
    for name, w in targets:
        for l in open(os.path.join(MH, "targets", name)):
            if l.startswith("#") or not l.strip(): continue
            i, x, y, z = l.split(); i = int(i); verts[i][0] += w * float(x); verts[i][1] += w * float(y); verts[i][2] += w * float(z)
    return verts, groups

def _mesh(name, verts, faces, weights, arm):
    used = sorted({i for f in faces for i in f}); idx = {v: k for k, v in enumerate(used)}
    me = bpy.data.meshes.new(name); me.from_pydata([conv(verts[i]) for i in used], [], [[idx[i] for i in f] for f in faces]); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for b, lst in weights.items():
        vg = None
        for i, w in lst:
            if i in idx:
                if vg is None: vg = ob.vertex_groups.new(name=b)
                vg.add([idx[i]], w, "REPLACE")
    m = ob.modifiers.new("arm", "ARMATURE"); m.object = arm; ob.parent = arm
    ob["src"] = used   # indici della mesh base (per selezionare zone)
    return ob

def human(muscle=0.35, targets=()):
    T = [("macrodetails/caucasian-male-young.target", 1.0), ("macrodetails/universal-male-young-maxmuscle-averageweight.target", muscle), *targets]
    verts, groups = _load(T)
    sk = json.load(open(os.path.join(MH, "rigs/default.mhskel"))); W = json.load(open(os.path.join(MH, "rigs/default_weights.mhw")))["weights"]
    jpos = {j: sum((conv(verts[i]) for i in ids), Vector()) / len(ids) for j, ids in sk["joints"].items()}
    ad = bpy.data.armatures.new("uomo"); arm = bpy.data.objects.new("uomo", ad); bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
    done = set()
    def add(n):
        if n in done: return
        b = sk["bones"][n]
        if b["parent"]: add(b["parent"])
        eb = ad.edit_bones.new(n); eb.head = jpos[b["head"]]; eb.tail = jpos[b["tail"]]
        if (eb.tail - eb.head).length < 1e-4: eb.tail = eb.head + Vector((0, 0, 0.01))
        if b["parent"]: eb.parent = ad.edit_bones[b["parent"]]
        done.add(n)
    for n in sk["bones"]: add(n)
    bpy.ops.object.mode_set(mode="OBJECT")
    body = _mesh("corpo", verts, groups["body"], W, arm)
    suit = _mesh("tuta", verts, groups["helper-tights"], W, arm)
    hair = _mesh("capelli", verts, groups["helper-hair"], W, arm)
    eyes = _mesh("occhi", verts, groups["helper-l-eye"] + groups["helper-r-eye"], W, arm)
    # la tuta d'aiuto ha gli stessi pesi della pelle sotto? I suoi vertici non sono nel file dei pesi: si copiano dal vertice del corpo più vicino
    for ob in (suit, hair, eyes):
        if not any(len(v.groups) for v in ob.data.vertices): _copy_weights(body, ob)
    return {"arm": arm, "body": body, "suit": suit, "hair": hair, "eyes": eyes, "joints": jpos}

def _copy_weights(src, dst):
    from mathutils.kdtree import KDTree
    kd = KDTree(len(src.data.vertices))
    for v in src.data.vertices: kd.insert(v.co, v.index)
    kd.balance()
    names = [g.name for g in src.vertex_groups]; tg = {n: dst.vertex_groups.new(name=n) for n in names}
    for v in dst.data.vertices:
        near = kd.find_n(v.co, 3); tot = sum(1 / (d + 1e-5) for _, _, d in near); acc = {}
        for _, i, d in near:
            for ge in src.data.vertices[i].groups: acc[names[ge.group]] = acc.get(names[ge.group], 0) + ge.weight * (1 / (d + 1e-5)) / tot
        for n, w in acc.items():
            if w > 0.003: tg[n].add([v.index], w, "REPLACE")

def turn(arm, name, axis, deg):
    """Ruota un osso attorno a un asse del MONDO (x = verso la sinistra della figura... in pratica: 'X' piega avanti/indietro, 'Y' di lato, 'Z' torsione)
    con perno nella sua testa. Chiamare dalla radice verso le punte."""
    bpy.context.view_layer.update()
    pb = arm.pose.bones[name]; ax = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis] if isinstance(axis, str) else Vector(axis)
    M = arm.matrix_world @ pb.matrix; piv = M.to_translation()
    R = Matrix.Translation(piv) @ Matrix.Rotation(math.radians(deg), 4, ax) @ Matrix.Translation(-piv)
    pb.matrix = arm.matrix_world.inverted() @ R @ M
    bpy.context.view_layer.update()

def shift(arm, name, vec):
    """Sposta un osso (e i figli) di un vettore in coordinate del mondo."""
    bpy.context.view_layer.update()
    pb = arm.pose.bones[name]; M = arm.matrix_world @ pb.matrix
    pb.matrix = arm.matrix_world.inverted() @ Matrix.Translation(Vector(vec)) @ M
    bpy.context.view_layer.update()

def key(arm, frame, names=None):
    for pb in arm.pose.bones:
        if names and pb.name not in names: continue
        pb.keyframe_insert("rotation_quaternion", frame=frame); pb.keyframe_insert("location", frame=frame)

def part(ob, name, keep):
    """Copia di un oggetto con le sole facce che hanno TUTTI i vertici accettati da keep(co) (coordinate a riposo): serve a ricavare capi dalla tuta."""
    import bmesh
    new = ob.copy(); new.data = ob.data.copy(); new.name = name; bpy.context.scene.collection.objects.link(new)
    bm = bmesh.new(); bm.from_mesh(new.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not all(keep(v.co) for v in f.verts)], context="FACES")
    bm.to_mesh(new.data); bm.free(); return new

def thicken(ob, offset, sub=1):
    """Sposta il capo verso l'esterno (spessore dello strato) e lo ammorbidisce."""
    d = ob.modifiers.new("gonfia", "DISPLACE"); d.strength = offset; d.mid_level = 0
    ob.modifiers.move(len(ob.modifiers) - 1, 0)   # prima dell'armatura: lo spessore segue la posa
    if sub:
        s = ob.modifiers.new("liscio", "SUBSURF"); s.levels = s.render_levels = sub
    return ob
