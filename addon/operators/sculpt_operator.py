import bpy


class BPS_OT_PrepareForSculpt(bpy.types.Operator):
    """Prepare the fused character for sculpting."""

    bl_idname = "bps.prepare_for_sculpt"
    bl_label = "Prepare For Sculpt"

    bl_options = {
        "REGISTER",
        "UNDO",
    }

    def execute(self, context):

        scene = context.scene

        character_name = scene.get(
            "bps_active_character",
            "",
        )

        if not character_name:

            self.report(
                {"ERROR"},
                "No active character.",
            )

            return {"CANCELLED"}

        object_name = (
            f"{character_name}_Fused_Base_Mesh"
        )

        obj = bpy.data.objects.get(
            object_name
        )

        if obj is None:

            self.report(
                {"ERROR"},
                "Generate a fused base mesh first.",
            )

            return {"CANCELLED"}

        bpy.ops.object.mode_set(
            mode="OBJECT"
        )

        bpy.ops.object.select_all(
            action="DESELECT"
        )

        obj.select_set(True)

        context.view_layer.objects.active = obj

        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=True,
        )

        bpy.ops.object.shade_smooth()

        multires = obj.modifiers.get(
            "Multires"
        )

        if multires is None:

            multires = obj.modifiers.new(
                name="Multires",
                type="MULTIRES",
            )

            bpy.ops.object.multires_subdivide(
                modifier=multires.name,
                mode="CATMULL_CLARK",
            )

            bpy.ops.object.multires_subdivide(
                modifier=multires.name,
                mode="CATMULL_CLARK",
            )

        bpy.ops.object.mode_set(
            mode="SCULPT"
        )

        for area in context.screen.areas:

            if area.type == "VIEW_3D":

                with context.temp_override(
                    area=area,
                    region=area.regions[-1],
                ):

                    bpy.ops.view3d.view_selected()

                break

        scene[
            "bps_character_status"
        ] = "Ready For Sculpt"

        self.report(
            {"INFO"},
            (
                f"{character_name} is ready "
                "for sculpting."
            ),
        )

        return {"FINISHED"}


classes = (
    BPS_OT_PrepareForSculpt,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
