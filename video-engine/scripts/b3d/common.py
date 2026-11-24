"""Scene 3D per le rappresentazioni dei reel (Ross 24/11: «animazioni più realistiche, anche in 3D»). Blender headless, Cycles su CPU.
Modello: manichino articolato «Xbot» (scheletro Mixamo, dagli esempi di three.js) in work/b3d/models/Xbot.glb; testa realistica
LeePerrySmith.glb (CC-BY 3.0, Lee Perry-Smith). Uso: blender -b -P scripts/b3d/<scena>.py -- [argomenti]"""
import bpy, math, os, sys
from mathutils import Vector, Euler, Matrix

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS = os.path.join(ROOT, "work", "b3d", "models")
BRAND = {"green": (0.067, 0.181, 0.027), "lime": (0.30, 1.0, 0.0), "ink": (0.004, 0.005, 0.003), "cream": (0.91, 0.87, 0.78), "ice": (0.48, 0.68, 0.82), "coral": (1.0, 0.15, 0.07)}

def reset(res=512, samples=40, fps=30):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples
    sc.cycles.use_denoising = False   # questa build non ha il filtro antirumore: più campioni
    sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.03
    sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transparent_max_bounces = 6
    sc.render.resolution_x = sc.render.resolution_y = res; sc.render.resolution_percentage = 100
    sc.render.film_transparent = True; sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
    sc.render.fps = fps; sc.render.threads_mode = "AUTO"
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.07, 0.05, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    return sc

def mat(name, color, rough=0.55, metal=0.0, emit=None, emit_strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = emit_strength
    if alpha < 1: b.inputs["Alpha"].default_value = alpha; m.blend_method = "BLEND"
    return m

def light(name, loc, energy, size=2.0, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = color
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    look_at(o, Vector((0, 0, 1.0))); return o

def look_at(o, target):
    d = Vector(target) - o.location; o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(loc, target, lens=70, ortho=None):
    d = bpy.data.cameras.new("cam"); d.lens = lens
    if ortho: d.type = "ORTHO"; d.ortho_scale = ortho
    o = bpy.data.objects.new("cam", d); bpy.context.scene.collection.objects.link(o); o.location = loc; look_at(o, target)
    bpy.context.scene.camera = o; return o

def studio():
    light("key", (-2.2, -3.0, 3.0), 330, 2.5, (1.0, 0.96, 0.9)); light("fill", (2.6, -2.2, 1.6), 160, 3.0, (0.85, 0.95, 1.0)); light("rim", (0.6, 2.8, 2.6), 620, 1.6, (0.75, 1.0, 0.6))

def xbot(action=None):
    """Importa il manichino: ritorna (armatura, superficie, giunture). Guarda verso -Y (la camera sta a -Y)."""
    bpy.ops.import_scene.gltf(filepath=os.path.join(MODELS, "Xbot.glb"))
    arm = bpy.data.objects["Armature"]; surf = bpy.data.objects["Beta_Surface"]; joints = bpy.data.objects["Beta_Joints"]
    ico = bpy.data.objects.get("Icosphere")
    if ico: bpy.data.objects.remove(ico)
    arm.animation_data_create(); arm.animation_data.action = bpy.data.actions.get(action) if action else None
    if not action:
        for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    for o in (surf, joints):
        for p in o.data.polygons: p.use_smooth = True
    return arm, surf, joints

def bone(arm, name): return arm.pose.bones["mixamorig:" + name]

def rot(arm, name, x=0, y=0, z=0):
    """Ruota un osso (gradi, assi locali dell'osso) rispetto alla posa di riposo."""
    pb = bone(arm, name); pb.rotation_mode = "XYZ"; pb.rotation_euler = (math.radians(x), math.radians(y), math.radians(z)); return pb

def render(path, frame=None):
    sc = bpy.context.scene
    if frame is not None: sc.frame_set(frame)
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)

def args(): return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
