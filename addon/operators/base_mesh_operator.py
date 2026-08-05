"""Base Mesh Operators.

The public operator routes generation through the BPS engine.
The legacy operator preserves the proven geometry-building workflow.
"""

import bpy

from ..engine import create_build_context
from ..engine.base_mesh_builder import (
    BaseMeshBuildError,
    build_base_mesh,
)


# ---------------------------------------------------------
# BASE-MESH PRESETS
# ---------------------------------------------------------

BASE_MESH_PRESETS = {
    "PRESCHOOL": {
        "head_radius": 0.16,
        "head_z": 0.80,
        "torso_width": 0.30,
        "torso_depth": 0.20,
        "torso_height": 0.27,
        "torso_z": 0.53,
        "pelvis_width": 0.25,
        "pelvis_depth": 0.19,
        "pelvis_height": 0.13,
        "pelvis_z": 0.34,
        "arm_radius": 0.045,
        "arm_length": 0.30,
        "arm_x": 0.19,
        "arm_z": 0.52,
        "leg_radius": 0.055,
        "leg_length": 0.30,
        "leg_x": 0.08,
        "leg_z": 0.16,
    },
    "CHILD": {
        "head_radius": 0.14,
        "head_z": 0.83,
        "torso_width": 0.28,
        "torso_depth": 0.19,
        "torso_height": 0.30,
        "torso_z": 0.55,
        "pelvis_width": 0.23,
        "pelvis_depth": 0.18,
        "pelvis_height": 0.14,
        "pelvis_z": 0.35,
        "arm_radius": 0.040,
        "arm_length": 0.34,
        "arm_x": 0.18,
        "arm_z": 0.53,
        "leg_radius": 0.050,
        "leg_length": 0.34,
        "leg_x": 0.075,
        "leg_z": 0.17,
    },
    "STANDARD": {
        "head_radius": 0.12,
        "head_z": 0.88,
        "torso_width": 0.27,
        "torso_depth": 0.18,
        "torso_height": 0.34,
        "torso_z": 0.57,
        "pelvis_width": 0.22,
        "pelvis_depth": 0.17,
        "pelvis_height": 0.15,
        "pelvis_z": 0.36,
        "arm_radius": 0.036,
        "arm_length": 0.38,
        "arm_x": 0.17,
        "arm_z": 0.55,
        "leg_radius": 0.045,
        "leg_length": 0.40,
        "leg_x": 0.07,
        "leg_z": 0.20,
    },
}


# ---------------------------------------------------------
# COLLECTION HELPERS
# ---------------------------------------------------------

def move_object_to_collection(
    obj,
    collection,
):
    """Move an object into one specific Blender collection."""

    for current_collection in list(
        obj.users_collection
    ):
        current_collection.objects.unlink(obj)

    collection.objects.link(obj)


def remove_existing_base_mesh(
    model_collection,
    character_name,
):
    """Remove previously generated BPS base-mesh objects."""

    prefix = f"{character_name}_Base_"

    for obj in list(model_collection.objects):
        if not obj.name.startswith(prefix):
            continue

        mesh_data = (
            obj.data
            if obj.type == "MESH"
            else None
        )

        bpy.data.objects.remove(
            obj,
            do_unlink=True,
        )

        if (
            mesh_data is not None
            and mesh_data.users == 0
        ):
            bpy.data.meshes.remove(mesh_data)


# ---------------------------------------------------------
# OBJECT HELPERS
# ---------------------------------------------------------

def mark_generated_object(
    obj,
    generator_name,
):
    """Attach standard BPS metadata to a generated object."""

    obj["bps_generated_base_mesh"] = True
    obj["bps_generator"] = generator_name
    obj["bps_generator_version"] = "1.1.1"

    return obj


def create_uv_sphere(
    context,
    collection,
    name,
    location,
    scale,
    generator_name,
):
    """Create one generated UV sphere."""

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24,
        ring_count=16,
        location=location,
    )

    obj = context.active_object
    obj.name = name
    obj.scale = scale

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True,
    )

    move_object_to_collection(
        obj,
        collection,
    )

    for polygon in obj.data.polygons:
        polygon.use_smooth = True

    return mark_generated_object(
        obj,
        generator_name,
    )


def create_cube(
    context,
    collection,
    name,
    location,
    dimensions,
    generator_name,
):
    """Create one generated cube form."""

    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=location,
    )

    obj = context.active_object
    obj.name = name
    obj.dimensions = dimensions

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True,
    )

    move_object_to_collection(
        obj,
        collection,
    )

    return mark_generated_object(
        obj,
        generator_name,
    )


def create_cylinder(
    context,
    collection,
    name,
    location,
    radius,
    depth,
    generator_name,
):
    """Create one generated cylinder form."""

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=radius,
        depth=depth,
        location=location,
    )

    obj = context.active_object
    obj.name = name

    move_object_to_collection(
        obj,
        collection,
    )

    for polygon in obj.data.polygons:
        polygon.use_smooth = True

    return mark_generated_object(
        obj,
        generator_name,
    )


# ---------------------------------------------------------
# ENGINE-ROUTED PUBLIC OPERATOR
# ---------------------------------------------------------

class BPS_OT_GenerateBaseMesh(bpy.types.Operator):
    """Generate the active character base mesh through the BPS engine."""

    bl_idname = "bps.generate_base_mesh"
    bl_label = "Generate Base Mesh"
    bl_description = (
        "Generate the selected character's base mesh "
        "through the Blender Production System engine"
    )
    bl_options = {
        "REGISTER",
        "UNDO",
    }

    def execute(self, context):
        scene = context.scene

        active_character = scene.get(
            "bps_active_character",
            "",
        )

        if not active_character:
            self.report(
                {"ERROR"},
                "Create or activate a character project first.",
            )
            return {"CANCELLED"}

        try:
            build_context = create_build_context(
                scene
            )

            result = build_base_mesh(
                build_context
            )

        except BaseMeshBuildError as error:
            self.report(
                {"ERROR"},
                str(error),
            )
            return {"CANCELLED"}

        except (
            AttributeError,
            KeyError,
            RuntimeError,
            TypeError,
            ValueError,
        ) as error:
            self.report(
                {"ERROR"},
                (
                    "The BPS engine could not generate "
                    f"the base mesh: {error}"
                ),
            )
            return {"CANCELLED"}

        if "FINISHED" not in result:
            self.report(
                {"ERROR"},
                "Base-mesh generation did not finish.",
            )
            return {"CANCELLED"}

        scene[
            "bps_character_status"
        ] = "Engine Base Mesh Generated"

        scene[
            "bps_base_mesh_engine"
        ] = "GeneratorEngine"

        self.report(
            {"INFO"},
            (
                f"Engine-routed base mesh generated for "
                f"{active_character}."
            ),
        )

        return {"FINISHED"}


# ---------------------------------------------------------
# LEGACY GEOMETRY OPERATOR
# ---------------------------------------------------------

class BPS_OT_GenerateBaseMeshLegacy(bpy.types.Operator):
    """Run the proven internal base-mesh geometry workflow."""

    bl_idname = "bps.generate_base_mesh_legacy"
    bl_label = "Generate Base Mesh Legacy"
    bl_description = (
        "Internal geometry builder used by the "
        "Blender Production System engine"
    )
    bl_options = {
        "INTERNAL",
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
                "Create or activate a character project first.",
            )
            return {"CANCELLED"}

        character_height = scene.bps_character_height

        if character_height <= 0.0:
            self.report(
                {"ERROR"},
                "Character height must be greater than zero.",
            )
            return {"CANCELLED"}

        preset_key = scene.bps_blueprint_preset

        preset = BASE_MESH_PRESETS.get(
            preset_key,
            BASE_MESH_PRESETS["PRESCHOOL"],
        )

        model_collection_name = (
            f"{character_name}_Model"
        )

        model_collection = bpy.data.collections.get(
            model_collection_name
        )

        if model_collection is None:
            self.report(
                {"ERROR"},
                (
                    f"Collection '{model_collection_name}' "
                    "was not found."
                ),
            )
            return {"CANCELLED"}

        remove_existing_base_mesh(
            model_collection=model_collection,
            character_name=character_name,
        )

        height = character_height

        # -------------------------------------------------
        # HEAD
        # -------------------------------------------------

        head_radius = (
            height
            * preset["head_radius"]
        )

        create_uv_sphere(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Head",
            location=(
                0.0,
                0.0,
                height * preset["head_z"],
            ),
            scale=(
                head_radius,
                head_radius * 0.92,
                head_radius * 1.08,
            ),
            generator_name="Head",
        )

        # -------------------------------------------------
        # TORSO
        # -------------------------------------------------

        create_cube(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Torso",
            location=(
                0.0,
                0.0,
                height * preset["torso_z"],
            ),
            dimensions=(
                height * preset["torso_width"],
                height * preset["torso_depth"],
                height * preset["torso_height"],
            ),
            generator_name="Torso",
        )

        # -------------------------------------------------
        # PELVIS
        # -------------------------------------------------

        create_cube(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Pelvis",
            location=(
                0.0,
                0.0,
                height * preset["pelvis_z"],
            ),
            dimensions=(
                height * preset["pelvis_width"],
                height * preset["pelvis_depth"],
                height * preset["pelvis_height"],
            ),
            generator_name="Pelvis",
        )

        # -------------------------------------------------
        # ARMS
        # -------------------------------------------------

        arm_radius = (
            height
            * preset["arm_radius"]
        )

        arm_length = (
            height
            * preset["arm_length"]
        )

        arm_x = (
            height
            * preset["arm_x"]
        )

        arm_z = (
            height
            * preset["arm_z"]
        )

        create_cylinder(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Arm_L",
            location=(
                arm_x,
                0.0,
                arm_z,
            ),
            radius=arm_radius,
            depth=arm_length,
            generator_name="Arm",
        )

        create_cylinder(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Arm_R",
            location=(
                -arm_x,
                0.0,
                arm_z,
            ),
            radius=arm_radius,
            depth=arm_length,
            generator_name="Arm",
        )

        # -------------------------------------------------
        # LEGS
        # -------------------------------------------------

        leg_radius = (
            height
            * preset["leg_radius"]
        )

        leg_length = (
            height
            * preset["leg_length"]
        )

        leg_x = (
            height
            * preset["leg_x"]
        )

        leg_z = (
            height
            * preset["leg_z"]
        )

        create_cylinder(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Leg_L",
            location=(
                leg_x,
                0.0,
                leg_z,
            ),
            radius=leg_radius,
            depth=leg_length,
            generator_name="Leg",
        )

        create_cylinder(
            context=context,
            collection=model_collection,
            name=f"{character_name}_Base_Leg_R",
            location=(
                -leg_x,
                0.0,
                leg_z,
            ),
            radius=leg_radius,
            depth=leg_length,
            generator_name="Leg",
        )

        # -------------------------------------------------
        # METADATA
        # -------------------------------------------------

        selected_template = getattr(
            scene,
            "bps_character_template",
            "GENERIC",
        )

        model_collection[
            "bps_base_mesh_generated"
        ] = True

        model_collection[
            "bps_base_mesh_preset"
        ] = preset_key

        model_collection[
            "bps_base_mesh_height"
        ] = character_height

        model_collection[
            "bps_character_template"
        ] = selected_template

        model_collection[
            "bps_base_mesh_builder"
        ] = "LegacyGeometryAdapter"

        model_collection[
            "bps_base_mesh_version"
        ] = "1.1.1"

        scene[
            "bps_character_status"
        ] = "Base Mesh Generated"

        self.report(
            {"INFO"},
            (
                f"Base mesh generated for "
                f"{character_name} at "
                f"{character_height:.2f} meters."
            ),
        )

        return {"FINISHED"}


# ---------------------------------------------------------
# REGISTRATION
# ---------------------------------------------------------

classes = (
    BPS_OT_GenerateBaseMeshLegacy,
    BPS_OT_GenerateBaseMesh,
)


def register():
    """Register the internal builder before the public operator."""

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister the public operator before the internal builder."""

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
