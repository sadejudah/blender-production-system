"""Character Studio parent panel and shared character properties."""

import bpy

from ..data import resolve_character_data
from ..templates import get_template_items


# ---------------------------------------------------------
# TEMPLATE UPDATE
# ---------------------------------------------------------

def apply_character_template(scene, context):
    """Apply resolved production data from the selected template."""

    character_data = resolve_character_data(
        scene.bps_character_template
    )

    # Generic characters remain freely nameable.
    if character_data.template_key != "GENERIC":
        scene.bps_character_name = character_data.name

    scene.bps_character_height = character_data.height
    scene.bps_blueprint_preset = (
        character_data.blueprint_preset
    )

    # Store resolved production information for other systems.
    scene[
        "bps_selected_template"
    ] = character_data.template_key

    scene[
        "bps_selected_template_name"
    ] = character_data.name

    scene[
        "bps_selected_species"
    ] = character_data.species

    scene[
        "bps_selected_head_style"
    ] = character_data.head_style

    scene[
        "bps_selected_torso_style"
    ] = character_data.torso_style

    scene[
        "bps_selected_arm_style"
    ] = character_data.arm_style

    scene[
        "bps_selected_leg_style"
    ] = character_data.leg_style

    scene[
        "bps_selected_hand_style"
    ] = character_data.hand_style

    scene[
        "bps_selected_foot_style"
    ] = character_data.foot_style

    scene[
        "bps_selected_eye_style"
    ] = character_data.eye_style

    scene[
        "bps_selected_mouth_style"
    ] = character_data.mouth_style

    scene[
        "bps_selected_rig_template"
    ] = character_data.rig_template or ""

    scene[
        "bps_selected_material_template"
    ] = character_data.material_template or ""

    scene[
        "bps_selected_primary_color"
    ] = character_data.primary_color

    scene[
        "bps_selected_secondary_color"
    ] = character_data.secondary_color

    scene[
        "bps_selected_accent_color"
    ] = character_data.accent_color


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

        selected_species = scene.get(
            "bps_selected_species",
            "Generic",
        )

        character_box.separator()

        character_box.label(
            text=f"Species: {selected_species}",
            icon="INFO",
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
    """Register Character Studio properties and parent panel."""

    bpy.types.Scene.bps_character_name = (
        bpy.props.StringProperty(
            name="Character Name",
            description="Production name of the character",
            default="",
        )
    )

    bpy.types.Scene.bps_character_template = (
        bpy.props.EnumProperty(
            name="Character Template",
            description=(
                "Predefined production template "
                "for the character"
            ),
            items=get_template_items(),
            default="GENERIC",
            update=apply_character_template,
        )
    )

    bpy.types.Scene.bps_character_height = (
        bpy.props.FloatProperty(
            name="Character Height",
            description=(
                "Production height of the character "
                "in meters"
            ),
            default=1.0,
            min=0.1,
            max=20.0,
            precision=2,
        )
    )

    bpy.types.Scene.bps_blueprint_preset = (
        bpy.props.EnumProperty(
            name="Blueprint Preset",
            description=(
                "Proportion system used by the "
                "blueprint and generators"
            ),
            items=(
                (
                    "PRESCHOOL",
                    "Stylized Preschool",
                    (
                        "Large head, compact torso, "
                        "and shorter limbs"
                    ),
                ),
                (
                    "CHILD",
                    "Child",
                    "Balanced child proportions",
                ),
                (
                    "STANDARD",
                    "Standard",
                    (
                        "Neutral general-purpose "
                        "proportions"
                    ),
                ),
            ),
            default="PRESCHOOL",
        )
    )

    bpy.types.Scene.bps_character_project_root = (
        bpy.props.StringProperty(
            name="Project Destination",
            description=(
                "Folder where the character project "
                "will be created"
            ),
            subtype="DIR_PATH",
            default="",
        )
    )

    bpy.types.Scene.bps_character_front_reference = (
        bpy.props.StringProperty(
            name="Front Reference",
            description=(
                "Front-view character reference image"
            ),
            subtype="FILE_PATH",
            default="",
        )
    )

    bpy.types.Scene.bps_character_side_reference = (
        bpy.props.StringProperty(
            name="Side Reference",
            description=(
                "Side-view character reference image"
            ),
            subtype="FILE_PATH",
            default="",
        )
    )

    bpy.types.Scene.bps_character_back_reference = (
        bpy.props.StringProperty(
            name="Back Reference",
            description=(
                "Back-view character reference image"
            ),
            subtype="FILE_PATH",
            default="",
        )
    )

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister the parent panel and shared properties."""

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