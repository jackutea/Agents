import sys
import json
import socket
from typing import Any
from mcp.server.fastmcp import FastMCP

# Setup FastMCP Server
mcp = FastMCP("BlenderMCP")

BLENDER_HOST = '127.0.0.1'
BLENDER_PORT = 8081

def send_to_blender(command: str) -> dict:
    """Send raw python code to the blender socket server and wait for response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((BLENDER_HOST, BLENDER_PORT))
            payload = json.dumps({"command": command})
            s.sendall(payload.encode('utf-8'))
            
            data = s.recv(4096)
            return json.loads(data.decode('utf-8'))
        except ConnectionRefusedError:
            return {"status": "error", "output": "Connection refused. Make sure blender_listener.py is running in Blender."}
        except Exception as e:
            return {"status": "error", "output": str(e)}

@mcp.tool()
def execute_blender_python(code: str) -> str:
    """
    Execute raw Python code in the connected Blender instance. 
    The code has access to `bpy` module automatically.
    """
    res = send_to_blender(code)
    if res.get("status") == "success":
        return "Executed successfully."
    else:
        return f"Error executing code in Blender:\n{res.get('output')}"

@mcp.tool()
def create_mesh(mesh_type: str, name: str = "NewMesh"):
    """
    Create a standard mesh object in Blender (e.g. cube, sphere, monkey).
    Valid mesh_type: 'cube', 'sphere', 'monkey', 'plane', 'cylinder'.
    """
    commands_map = {
        'cube': "bpy.ops.mesh.primitive_cube_add()",
        'sphere': "bpy.ops.mesh.primitive_uv_sphere_add()",
        'monkey': "bpy.ops.mesh.primitive_monkey_add()",
        'plane': "bpy.ops.mesh.primitive_plane_add()",
        'cylinder': "bpy.ops.mesh.primitive_cylinder_add()"
    }
    cmd = commands_map.get(mesh_type.lower(), "bpy.ops.mesh.primitive_cube_add()")
    
    code = f"""
{cmd}
bpy.context.active_object.name = "{name}"
    """
    res = send_to_blender(code)
    return str(res)

@mcp.tool()
def create_armature(name: str = "Armature"):
    """
    Create a new empty armature in Blender.
    """
    code = f"""
bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "{name}"
"""
    res = send_to_blender(code)
    return str(res)

@mcp.tool()
def add_bone(armature_name: str, bone_name: str, head_pos: list[float], tail_pos: list[float]):
    """
    Add a new bone to a specific armature. 
    head_pos and tail_pos must be lists of 3 floats [x,y,z].
    """
    code = f"""
import bpy
arm_obj = bpy.data.objects.get('{armature_name}')
if arm_obj and arm_obj.type == 'ARMATURE':
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    eb = arm_obj.data.edit_bones.new('{bone_name}')
    eb.head = {head_pos}
    eb.tail = {tail_pos}
    
    bpy.ops.object.mode_set(mode='OBJECT')
"""
    res = send_to_blender(code)
    return str(res)

@mcp.tool()
def parent_with_automatic_weights(mesh_name: str, armature_name: str):
    """
    Parent a mesh to an armature using Automatic Weights.
    """
    code = f"""
import bpy
mesh = bpy.data.objects.get('{mesh_name}')
arm = bpy.data.objects.get('{armature_name}')

if mesh and arm:
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
"""
    res = send_to_blender(code)
    return str(res)

@mcp.tool()
def insert_keyframe(object_name: str, frame: int, data_path: str = "location"):
    """
    Insert a keyframe for an object at a specific frame.
    data_path can be 'location', 'rotation_euler', 'scale'.
    """
    code = f"""
import bpy
obj = bpy.data.objects.get('{object_name}')
if obj:
    obj.keyframe_insert(data_path='{data_path}', frame={frame})
"""
    res = send_to_blender(code)
    return str(res)

if __name__ == "__main__":
    mcp.run()
