import bpy


class BPS_PT_ReferencePanel(bpy.types.Panel):
    """Character reference image controls."""

    bl_idname = "BPS_PT_reference_panel"
    bl_label = "References"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"
    bl_parent_id = "BPS_PT_character_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(
            text="Front View",
            icon="IMAGE_DATA",
        )
        layout.prop(
            scene,
            "bps_character_front_reference",
            text="",
        )

        layout.label(text="Side View")
        layout.prop(
            scene,
            "bps_character_side_reference",
            text="",
        )

        layout.label(text="Back View")
        layout.prop(
            scene,
            "bps_character_back_reference",
            text="",
        )

        import_button = layout.row()
        import_button.scale_y = 1.3
        import_button.operator(
            "bps.import_character_references",
            text="IMPORT REFERENCES",
            icon="IMPORT",
        )

        view_buttons = layout.row(align=True)

        front_button = view_buttons.operator(
            "bps.open_blueprint_view",
            text="FRONT",
        )
        front_button.view_axis = "FRONT"

        side_button = view_buttons.operator(
            "bps.open_blueprint_view",
            text="SIDE",
        )
        side_button.view_axis = "RIGHT"

        back_button = view_buttons.operator(
            "bps.open_blueprint_view",
            text="BACK",
        )
        back_button.view_axis = "BACK"


classes = (
    BPS_PT_ReferencePanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
