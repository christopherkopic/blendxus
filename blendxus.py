bl_info = {
    "name": "Blendxus",
    "author": "Christopher Kopic",
    "version": (1, 0),
    "blender": (2, 7, 8),
    "location": "",
    "description": "Adds Operator for creating edges between close vertices",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}


import bpy
import bmesh
import mathutils
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, BoolProperty


class Blendxus(bpy.types.Operator):
    """Blendxus"""
    bl_idname = "object.blendxus"
    bl_label = "Blendxus"
    bl_options = {'REGISTER', 'UNDO'}

    max_connects = IntProperty(
        name="Maximum Connections",
        default=3,
        min=1,
        description="Maximum number of connections per vertex"
    )

    max_distance = FloatProperty(
        name="Maximum Distance",
        default=0.2,
        min=0,
        description="Maximum distance for creating connetions"
    )

    del_edge_face = BoolProperty(
        name="Delete Initial Edges and Faces",
        default=True,
        description="Deletes all existing edges and faces to make the new connections visible"
    )

    convert_curve = BoolProperty(
        name="Export to Curve",
        default=False,
        options={'SKIP_SAVE'},
        description="Converts edgenet to curve for rendering. Effect won't be editable afterwards"
    )

    def execute(self, context):
        obj = context.active_object
        if obj.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()

        # prepare bmesh
        me = obj.data
        ori = bmesh.new()
        ori.from_mesh(me)

        # delete faces and edges
        if self.del_edge_face:
            ori.edges.ensure_lookup_table()
            bmesh.ops.delete(ori, geom=ori.edges, context=4)

        # create kd-Tree
        ori.verts.ensure_lookup_table()
        size = len(ori.verts)
        kd = mathutils.kdtree.KDTree(size)

        for i, v in enumerate(ori.verts):
            kd.insert(v.co, i)

        kd.balance()

        # create connections
        for vert in ori.verts:
            count = 0
            for (co, index, dist) in kd.find_range(vert.co, self.max_distance):
                if vert.index != index:
                    bmesh.ops.contextual_create(ori, geom=[vert, ori.verts[index]])
                    count += 1
                if count > self.max_connects:
                    break

        # apply changes
        ori.to_mesh(me)
        ori.free()

        # convert to curve
        if self.convert_curve:
            bpy.ops.object.convert(target='CURVE')
            obj.data.bevel_depth = 0.001
            obj.data.fill_mode = 'FULL'

        # update viewport
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob is not None and ob.mode == 'OBJECT' and ob.type == 'MESH'


def register():
    bpy.utils.register_class(Blendxus)


def unregister():
    bpy.utils.unregister_class(Blendxus)


if __name__ == "__main__":
    register()
