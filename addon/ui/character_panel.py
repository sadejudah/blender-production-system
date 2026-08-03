
import bpy


class BPS_PT_CharacterPanel(bpy.types.Panel):
    """Character Studio"""

    bl_idname = "BPS_PT_character_panel"
    bl_label = "Character Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):
        layout = self.layout

        box = layout.box()

        box.label(
            text="CHARACTER STUDIO",
            icon="OUTLINER_OB_ARMATURE"
        )

        box.separator()

        box.label(text="Character Name")

        box.prop(
            context.scene,
            "bps_character_name",
            text=""
        )

        box.separator()

        box.operator(
            "bps.create_character",
            text="Create Character",
            icon="ADD"
        )


classes = (
    BPS_PT_CharacterPanel,
)


def register():

    bpy.types.Scene.bps_character_name = bpy.props.StringProperty(
        name="Character Name",
        default=""
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    del bpy.types.Scene.bps_character_name

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
