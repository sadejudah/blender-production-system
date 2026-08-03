import bpy


class BPS_OT_AutoMirrorModel(bpy.types.Operator):
    """Prepare a mesh for mirrored character modeling."""

    bl_idname = "bps.auto_mirror_model"
    bl_label = "Auto Mirror Model"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        obj = context.active_object

        if obj is None:
            self.report({"ERROR"}, "Select a mesh object.")
            return {"CANCELLED"}

        if obj.type != "MESH":
            self.report({"ERROR"}, "Active object must be a mesh.")
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode="OBJECT")

        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=True,
        )

        mirror = obj.modifiers.get("Mirror")

        if mirror is None:
            mirror = obj.modifiers.new(
                name="Mirror",
                type="MIRROR",
            )

        mirror.use_axis[0] = True
        mirror.use_clip = True
        mirror.use_mirror_merge = True

        bpy.ops.object.mode_set(mode="EDIT")

        bpy.ops.mesh.select_all(action="SELECT")

        bpy.ops.mesh.bisect(
            plane_co=(0, 0, 0),
            plane_no=(1, 0, 0),
            clear_inner=False,
            clear_outer=True,
        )

        tool = context.scene.tool_settings

        tool.use_mesh_automerge = True

        self.report(
            {"INFO"},
            "Mirror modeling enabled.",
        )

        return {"FINISHED"}


classes = (
    BPS_OT_AutoMirrorModel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
