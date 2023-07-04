# MIT License

# Copyright (c) 2023 Gizmo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy
import math

bl_info = {
	"name": "unity-rotation-fix",
	"author": "gizmo-ds",
	"description": "Fix Armature Rotation (Blender to Unity)",
	"blender": (2, 80, 0),
	"version": (0, 0, 1),
	"location": "",
	"warning": "",
	"category": "Generic"
}

class URF_Panel(bpy.types.Panel):
	bl_label = "Unity Rotation Fix"
	bl_idname = "urf.panel"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "URF"

	def draw(self, context):
		layer = self.layout
		layer.row().operator('urf.operator', text='Unity Rotation Fix', icon='MODIFIER')

class URF_Operator(bpy.types.Operator):
	bl_idname = 'urf.operator'
	bl_label = 'Operator'
	
	def execute(self, context):
		'''Unity Rotation Fix'''
		armature = None
		all_objects = bpy.context.collection.all_objects
		for obj in all_objects:
			if obj.type == 'ARMATURE':
					# 检测是否存在多个 Armature
					if armature != None:
							self.report({'ERROR'}, 'Multiple armatures found.')
							return {'CANCELLED'}
					armature = obj
			else:
					# 检测是否已经旋转
					x = math.floor(math.degrees(obj.rotation_euler.x))
					if x != 0:
							self.report({'ERROR'}, 'Object ' + obj.name + ' already rotated.')
							return {'CANCELLED'}
		bpy.ops.object.select_all(action='SELECT')
		bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
		bpy.ops.transform.rotate(value=math.radians(-90), orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		bpy.ops.transform.rotate(value=math.radians(90), orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
		armature.select_set(False)
		bpy.context.view_layer.objects.active = armature
		bpy.ops.object.parent_set(type='ARMATURE')
		self.report({'INFO'}, 'Rotation fixed.')
		return {'FINISHED'}

def register():
	bpy.utils.register_class(URF_Operator)
	bpy.utils.register_class(URF_Panel)

def unregister():
	pass

if __name__ == "__main__":
	register()
