
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

        references = studio.box()
        references.label(
            text="REFERENCE IMAGES",
            icon="IMAGE_DATA",
        )

        references.label(text="Front View")
        references.prop(
            scene,
            "bps_character_front_reference",
            text="",
        )

        references.label(text="Side View")
        references.prop(
            scene,
            "bps_character_side_reference",
            text="",
        )

        references.label(text="Back View")
        references.prop(
            scene,
            "bps_character_back_reference",
            text="",
        )

        import_button = references.row()
        import_button.scale_y = 1.3
        import_button.operator(
            "bps.import_character_references",
            text="IMPORT REFERENCES",
            icon="IMPORT",
        )

        studio.separator()

        create_button = studio.row()
        create_button.scale_y = 1.5
        create_button.operator(
            "bps.create_character",
            text="CREATE CHARACTER PROJECT",
            icon="ADD",
        )
        
        view_buttons = references.row(align=True)

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

    bpy.types.Scene.bps_character_front_reference = bpy.props.StringProperty(
        name="Front Reference",
        description="Front-view reference image",
        subtype="FILE_PATH",
        default="",
    )

    bpy.types.Scene.bps_character_side_reference = bpy.props.StringProperty(
        name="Side Reference",
        description="Side-view reference image",
        subtype="FILE_PATH",
        default="",
    )

    bpy.types.Scene.bps_character_back_reference = bpy.props.StringProperty(
        name="Back Reference",
        description="Back-view reference image",
        subtype="FILE_PATH",
        default="",
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    property_names = (
        "bps_character_back_reference",
        "bps_character_side_reference",
        "bps_character_front_reference",
        "bps_character_project_root",
        "bps_character_name",
    )

    for property_name in property_names:
        if hasattr(bpy.types.Scene, property_name):
            delattr(bpy.types.Scene, property_name)