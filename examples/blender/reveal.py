"""Run with Blender's Python, not system Python."""
import bpy, sys, argparse
from pathlib import Path
from mathutils import Vector
parser=argparse.ArgumentParser()
parser.add_argument('--out',type=Path,required=True)
a=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
a.out.mkdir(parents=True,exist_ok=True)
target=(a.out/'reveal.blend').resolve()
if target.exists(): raise RuntimeError('Refusing to overwrite reveal.blend')
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def cube(name,location,scale,color):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    obj=bpy.context.object; obj.name=name; obj.scale=scale
    mat=bpy.data.materials.new(name+' material'); mat.diffuse_color=(*color,1)
    obj.data.materials.append(mat); return obj
cube('base',(0,0,0),(4,2.2,.25),(.1,.15,.22))
for i in range(3): cube('module '+str(i),(i-1,0,.6),(.65,1.4,.9),(.1,.65,.8))
cover=cube('cover',(0,0,1.2),(4,2.2,.2),(.75,.85,.9))
cover.keyframe_insert(data_path='location',frame=1)
cover.location.z=3; cover.keyframe_insert(data_path='location',frame=72)
bpy.ops.object.camera_add(location=(6,-8,6)); cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene; scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(1,-3,7)); bpy.context.object.data.energy=1500; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=5
scene.render.engine='CYCLES'; scene.cycles.samples=24
scene.render.resolution_x=960; scene.render.resolution_y=540; scene.render.resolution_percentage=100
scene.render.fps=24; scene.frame_start=1; scene.frame_end=96
scene.render.image_settings.file_format='PNG'; scene.render.filepath=str((a.out/'frame_').resolve())
bpy.ops.wm.save_as_mainfile(filepath=str(target))
print(target)
