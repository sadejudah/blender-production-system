"""
Arm Generator

Creates upper arms and forearms for the Blender Production System.
"""

from mathutils import Vector

import bpy

from .mesh_helpers import prepare_object


def create_cylinder_between(
    context,
    collection,
    name,
    start_point,
    end_point,
    radius,
):
    """Create one cylinder aligned between two points."""

    start = Vector(start_point)
    end = Vector(end_point)

    direction = end - start
    length = direction.length

    if length <= 0.0001:
        return None

    midpoint = (start + end) / 2.0

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,
        radius=radius,
        depth=length,
        location=midpoint,
    )

    obj = context.active_object
    obj.name = name

    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = direction.to_track_quat(
        "Z",
        "Y",
    )

    prepare_object(
        obj,
        subdivision=1,
    )

    for current_collection in list(
        obj.users_collection
    ):
        current_collection.objects.unlink(obj)

    collection.objects.link(obj)

    obj[
        "bps_generated_base_mesh"
    ] = True

    obj[
        "bps_generator"
    ] = "Arm"

    return obj


def create_arms(
    context,
    collection,
    character_name,
    shoulder_half_width,
    shoulder_z,
    upper_arm_length,
    lower_arm_length,
    limb_radius,
    arm_spread=0.82,
    forearm_spread=0.74,
    arm_drop=0.42,
    forearm_drop=0.56,
):
    """Create both arms in a slight A-pose."""

    generated_objects = []

    for side_name, side_sign in (
        ("L", 1.0),
        ("R", -1.0),
    ):
        shoulder_point = (
            side_sign * shoulder_half_width,
            0.0,
            shoulder_z,
        )

        elbow_point = (
            side_sign
            * (
                shoulder_half_width
                + upper_arm_length * arm_spread
            ),
            0.0,
            shoulder_z
            - upper_arm_length * arm_drop,
        )

        wrist_point = (
            side_sign
            * (
                shoulder_half_width
                + upper_arm_length * arm_spread
                + lower_arm_length * forearm_spread
            ),
            0.0,
            shoulder_z
            - upper_arm_length * arm_drop
            - lower_arm_length * forearm_drop,
        )

        upper_arm = create_cylinder_between(
            context=context,
            collection=collection,
            name=(
                f"{character_name}_"
                f"Base_UpperArm_{side_name}"
            ),
            start_point=shoulder_point,
            end_point=elbow_point,
            radius=limb_radius * 1.08,
        )

        forearm = create_cylinder_between(
            context=context,
            collection=collection,
            name=(
                f"{character_name}_"
                f"Base_Forearm_{side_name}"
            ),
            start_point=elbow_point,
            end_point=wrist_point,
            radius=limb_radius * 0.88,
        )

        if upper_arm is not None:
            generated_objects.append(upper_arm)

        if forearm is not None:
            generated_objects.append(forearm)

    return generated_objects
