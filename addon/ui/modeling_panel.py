"""Modeling Studio."""

import bpy


class BPS_PT_ModelingPanel(bpy.types.Panel):
    """Modeling Studio."""

    bl_label = "Modeling Studio"
    bl_idname = "BPS_PT_modeling_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):

        layout = self.layout

        # -----------------------------------------
        # FOUNDATION
        # -----------------------------------------

        foundation = layout.box()

        foundation.label(
            text="FOUNDATION",
            icon="MESH_CUBE",
        )

        row = foundation.row()
        row.scale_y = 1.3

        row.operator(
            "bps.generate_base_mesh",
            text="Generate Base Mesh",
            icon="MESH_UVSPHERE",
        )

        row = foundation.row()
        row.scale_y = 1.3

        row.operator(
            "bps.fuse_base_mesh",
            text="Fuse Base Mesh",
            icon="MOD_REMESH",
        )

        # -----------------------------------------
        # TOOLS
        # -----------------------------------------

        tools = layout.box()

        tools.label(
            text="TOOLS",
            icon="TOOL_SETTINGS",
        )

        row = tools.row()
        row.scale_y = 1.3

        row.operator(
            "bps.auto_mirror_model",
            text="Auto Mirror Model",
            icon="MOD_MIRROR",
        )


classes = (
    BPS_PT_ModelingPanel,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
