"""
Leg Generator

Creates thighs and calves for the Blender Production System.
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
    ] = "Leg"

    return obj


def create_legs(
    context,
    collection,
    character_name,
    hip_half_width,
    hip_z,
    knee_z,
    ankle_z,
    limb_radius,
):
    """Create both thighs and calves."""

    generated_objects = []

    for side_name, side_sign in (
        ("L", 1.0),
        ("R", -1.0),
    ):
        leg_x = (
            side_sign
            * hip_half_width
            * 0.55
        )

        hip_point = (
            leg_x,
            0.0,
            hip_z,
        )

        knee_point = (
            leg_x,
            0.0,
            knee_z,
        )

        ankle_point = (
            leg_x,
            0.0,
            ankle_z,
        )

        thigh = create_cylinder_between(
            context=context,
            collection=collection,
            name=(
                f"{character_name}_"
                f"Base_Thigh_{side_name}"
            ),
            start_point=hip_point,
            end_point=knee_point,
            radius=limb_radius * 1.18,
        )

        calf = create_cylinder_between(
            context=context,
            collection=collection,
            name=(
                f"{character_name}_"
                f"Base_Calf_{side_name}"
            ),
            start_point=knee_point,
            end_point=ankle_point,
            radius=limb_radius,
        )

        if thigh is not None:
            generated_objects.append(thigh)

        if calf is not None:
            generated_objects.append(calf)

    return generated_objects
