
"""Character Studio parent panel and shared character properties."""

import bpy

from ..templates import get_template
from ..templates import get_template_items


# ---------------------------------------------------------
# TEMPLATE UPDATE
# ---------------------------------------------------------

def apply_character_template(scene, context):
    """Apply basic production settings from the selected template."""

    template_key = scene.bps_character_template
    template = get_template(template_key)

    template_name = template.get(
        "name",
        "Generic",
    )

    # Keep Generic characters freely nameable.
    # Named templates automatically apply their production name.
    if template_key != "GENERIC":
        scene.bps_character_name = template_name

    scene.bps_character_height = float(
        template.get(
            "height",
            1.0,
        )
    )

    blueprint_preset = template.get(
        "blueprint_preset",
        "STANDARD",
    )

    valid_blueprint_presets = {
        "PRESCHOOL",
        "CHILD",
        "STANDARD",
    }

    if blueprint_preset not in valid_blueprint_presets:
        blueprint_preset = "STANDARD"

    scene.bps_blueprint_preset = blueprint_preset

    # Store template information for operators and status displays.
    scene["bps_selected_template"] = template_key
    scene["bps_selected_template_name"] = template_name
    scene["bps_selected_species"] = template.get(
        "species",
        "Generic",
    )


# ---------------------------------------------------------
# CHARACTER STUDIO PARENT PANEL
# ---------------------------------------------------------

class BPS_PT_CharacterPanel(bpy.types.Panel):
    """Character Studio parent panel."""

    bl_idname = "BPS_PT_character_panel"
    bl_label = "Character Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # -------------------------------------------------
        # CHARACTER INFORMATION
        # -------------------------------------------------

        character_box = layout.box()

        character_box.label(
            text="CHARACTER INFORMATION",
            icon="OUTLINER_OB_ARMATURE",
        )

        character_box.label(
            text="Character Name",
        )

        character_box.prop(
            scene,
            "bps_character_name",
            text="",
        )

        character_box.separator()

        character_box.label(
            text="Character Template",
        )

        character_box.prop(
            scene,
            "bps_character_template",
            text="",
        )

        character_box.separator()

        character_box.label(
            text="Character Height",
        )

        character_box.prop(
            scene,
            "bps_character_height",
            text="Meters",
        )

        character_box.separator()

        character_box.label(
            text="Blueprint Preset",
        )

        character_box.prop(
            scene,
            "bps_blueprint_preset",
            text="",
        )

        # -------------------------------------------------
        # BLUEPRINT
        # Temporary home until blueprint_panel.py is added.
        # -------------------------------------------------

        blueprint_box = layout.box()

        blueprint_box.label(
            text="BLUEPRINT",
            icon="GRID",
        )

        blueprint_button = blueprint_box.row()
        blueprint_button.scale_y = 1.3

        blueprint_button.operator(
            "bps.generate_blueprint",
            text="GENERATE BLUEPRINT",
            icon="GRID",
        )

        # -------------------------------------------------
        # CHARACTER GENERATOR
        # Temporary home until modeling_panel.py is added.
        # -------------------------------------------------

        generator_box = layout.box()

        generator_box.label(
            text="CHARACTER GENERATOR",
            icon="OUTLINER_OB_MESH",
        )

        base_mesh_button = generator_box.row()
        base_mesh_button.scale_y = 1.3

        base_mesh_button.operator(
            "bps.generate_base_mesh",
            text="GENERATE BASE MESH",
            icon="MESH_UVSPHERE",
        )

        fuse_button = generator_box.row()
        fuse_button.scale_y = 1.3

        fuse_button.operator(
            "bps.fuse_base_mesh",
            text="FUSE BASE MESH",
            icon="MOD_REMESH",
        )

        # -------------------------------------------------
        # SCULPT TOOLS
        # Temporary home until sculpt_panel.py is added.
        # -------------------------------------------------

        sculpt_box = layout.box()

        sculpt_box.label(
            text="SCULPT TOOLS",
            icon="SCULPTMODE_HLT",
        )

        sculpt_button = sculpt_box.row()
        sculpt_button.scale_y = 1.3

        sculpt_button.operator(
            "bps.prepare_for_sculpt",
            text="PREPARE FOR SCULPT",
            icon="SCULPTMODE_HLT",
        )

        # -------------------------------------------------
        # MODELING TOOLS
        # -------------------------------------------------

        modeling_box = layout.box()

        modeling_box.label(
            text="MODELING TOOLS",
            icon="MOD_MIRROR",
        )

        mirror_button = modeling_box.row()
        mirror_button.scale_y = 1.3

        mirror_button.operator(
            "bps.auto_mirror_model",
            text="AUTO MIRROR MODEL",
            icon="MOD_MIRROR",
        )


# ---------------------------------------------------------
# REGISTRATION
# ---------------------------------------------------------

classes = (
    BPS_PT_CharacterPanel,
)


def register():
    """Register Character Studio properties and its parent panel."""

    bpy.types.Scene.bps_character_name = bpy.props.StringProperty(
        name="Character Name",
        description="Production name of the character",
        default="",
    )

    bpy.types.Scene.bps_character_template = bpy.props.EnumProperty(
        name="Character Template",
        description="Predefined production template for the character",
        items=get_template_items(),
        default="GENERIC",
        update=apply_character_template,
    )

    bpy.types.Scene.bps_character_height = bpy.props.FloatProperty(
        name="Character Height",
        description="Production height of the character in meters",
        default=1.0,
        min=0.1,
        max=20.0,
        precision=2,
    )

    bpy.types.Scene.bps_blueprint_preset = bpy.props.EnumProperty(
        name="Blueprint Preset",
        description="Proportion system used by the blueprint and generators",
        items=(
            (
                "PRESCHOOL",
                "Stylized Preschool",
                "Large head, compact torso, and shorter limbs",
            ),
            (
                "CHILD",
                "Child",
                "Balanced child proportions",
            ),
            (
                "STANDARD",
                "Standard",
                "Neutral general-purpose proportions",
            ),
        ),
        default="PRESCHOOL",
    )

    bpy.types.Scene.bps_character_project_root = bpy.props.StringProperty(
        name="Project Destination",
        description="Folder where the character project will be created",
        subtype="DIR_PATH",
        default="",
    )

    bpy.types.Scene.bps_character_front_reference = bpy.props.StringProperty(
        name="Front Reference",
        description="Front-view character reference image",
        subtype="FILE_PATH",
        default="",
    )

    bpy.types.Scene.bps_character_side_reference = bpy.props.StringProperty(
        name="Side Reference",
        description="Side-view character reference image",
        subtype="FILE_PATH",
        default="",
    )

    bpy.types.Scene.bps_character_back_reference = bpy.props.StringProperty(
        name="Back Reference",
        description="Back-view character reference image",
        subtype="FILE_PATH",
        default="",
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister the parent panel and Character Studio properties."""

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    property_names = (
        "bps_character_back_reference",
        "bps_character_side_reference",
        "bps_character_front_reference",
        "bps_character_project_root",
        "bps_blueprint_preset",
        "bps_character_height",
        "bps_character_template",
        "bps_character_name",
    )

    for property_name in property_names:
        if hasattr(
            bpy.types.Scene,
            property_name,
        ):
            delattr(
                bpy.types.Scene,
                property_name,
            )
