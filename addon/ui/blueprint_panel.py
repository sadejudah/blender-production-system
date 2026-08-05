"""Blueprint Panel."""

import bpy


class BPS_PT_BlueprintPanel(bpy.types.Panel):
    """Blueprint generation tools."""

    bl_label = "Blueprint"
    bl_idname = "BPS_PT_blueprint_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):

        layout = self.layout

        box = layout.box()

        box.label(
            text="BLUEPRINT",
            icon="GRID",
        )

        row = box.row()

        row.scale_y = 1.4

        row.operator(
            "bps.generate_blueprint",
            icon="GRID",
        )


classes = (
    BPS_PT_BlueprintPanel,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
