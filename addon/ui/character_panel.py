
import bpy


class BPS_PT_CharacterPanel(bpy.types.Panel):
    """Character Studio panel."""

    bl_idname = "BPS_PT_character_panel"
    bl_label = "Character Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        studio = layout.box()
        studio.label(
            text="CHARACTER STUDIO",
            icon="OUTLINER_OB_ARMATURE",
        )

        studio.separator()

        studio.label(text="Character Name")
        studio.prop(
            scene,
            "bps_character_name",
            text="",
        )

        studio.separator()

        studio.label(text="Project Destination")
        studio.prop(
            scene,
            "bps_character_project_root",
            text="",
        )

        help_box = studio.box()
        help_box.label(
            text="BPS will create the character folder",
            icon="INFO",
        )
        help_box.label(text="inside the selected destination.")

        studio.separator()

        create_button = studio.row()
        create_button.scale_y = 1.5
        create_button.operator(
            "bps.create_character",
            text="CREATE CHARACTER PROJECT",
            icon="ADD",
        )

        active_character = scene.get("bps_active_character", "")

        if active_character:
            status_box = layout.box()
            status_box.label(
                text="ACTIVE CHARACTER",
                icon="CHECKMARK",
            )
            status_box.label(text=active_character)
            status_box.label(
                text=scene.get(
                    "bps_character_status",
                    "Ready for Setup",
                ),
                icon="INFO",
            )


classes = (
    BPS_PT_CharacterPanel,
)


def register():
    bpy.types.Scene.bps_character_name = bpy.props.StringProperty(
        name="Character Name",
        description="Name of the new character",
        default="",
    )

    bpy.types.Scene.bps_character_project_root = bpy.props.StringProperty(
        name="Project Destination",
        description="Folder where the character project will be created",
        subtype="DIR_PATH",
        default="",
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types.Scene, "bps_character_project_root"):
        del bpy.types.Scene.bps_character_project_root

    if hasattr(bpy.types.Scene, "bps_character_name"):
        del bpy.types.Scene.bps_character_name
