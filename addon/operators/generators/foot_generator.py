"""
Foot Generator

Creates stylized feet for the Blender Production System.
"""

import bpy

from .mesh_helpers import prepare_object


def create_foot(
    context,
    collection,
    character_name,
    side_name,
    location,
    limb_radius,
    foot_length,
    foot_height,
    foot_scale=1.0,
):
    """Create one stylized foot."""

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20,
        ring_count=12,
        location=location,
    )

    obj = context.active_object

    obj.name = (
        f"{character_name}_"
        f"Base_Foot_{side_name}"
    )

    obj.scale = (
        limb_radius * 1.35 * foot_scale,
        foot_length * 0.60 * foot_scale,
        foot_height * 0.48 * foot_scale,
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
    ] = "Foot"

    return obj


def create_feet(
    context,
    collection,
    character_name,
    foot_locations,
    limb_radius,
    foot_length,
    foot_height,
    foot_scale=1.0,
):
    """Create left and right stylized feet."""

    generated_objects = []

    for side_name in (
        "L",
        "R",
    ):
        foot_location = foot_locations.get(
            side_name
        )

        if foot_location is None:
            continue

        foot = create_foot(
            context=context,
            collection=collection,
            character_name=character_name,
            side_name=side_name,
            location=foot_location,
            limb_radius=limb_radius,
            foot_length=foot_length,
            foot_height=foot_height,
            foot_scale=foot_scale,
        )

        generated_objects.append(foot)

    return generated_objects
