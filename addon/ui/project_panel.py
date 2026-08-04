import bpy


class BPS_PT_ProjectPanel(bpy.types.Panel):
    """Character project controls."""

    bl_idname = "BPS_PT_project_panel"
    bl_label = "Project"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"
    bl_parent_id = "BPS_PT_character_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(
            text="Project Destination",
            icon="FILE_FOLDER",
        )

        layout.prop(
            scene,
            "bps_character_project_root",
            text="",
        )

        help_box = layout.box()
        help_box.label(
            text="BPS creates the character folder",
            icon="INFO",
        )
        help_box.label(
            text="inside the selected destination.",
        )

        create_button = layout.row()
        create_button.scale_y = 1.4
        create_button.operator(
            "bps.create_character",
            text="CREATE CHARACTER PROJECT",
            icon="ADD",
        )


classes = (
    BPS_PT_ProjectPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
