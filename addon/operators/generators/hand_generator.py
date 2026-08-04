"""
Hand Generator

Creates stylized hand blockouts for the Blender Production System.
"""

import bpy

from .mesh_helpers import prepare_object


def create_hand(
    context,
    collection,
    character_name,
    side_name,
    location,
    hand_radius,
    hand_scale=1.0,
):
    """Create one rounded hand blockout."""

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20,
        ring_count=12,
        location=location,
    )

    obj = context.active_object

    obj.name = (
        f"{character_name}_"
        f"Base_Hand_{side_name}"
    )

    scale = hand_radius * hand_scale

    obj.scale = (
        scale * 0.72,
        scale * 0.45,
        scale,
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
    ] = "Hand"

    return obj


def create_hands(
    context,
    collection,
    character_name,
    wrist_points,
    hand_radius,
    hand_scale=1.0,
):
    """Create left and right stylized hands."""

    generated_objects = []

    for side_name in (
        "L",
        "R",
    ):
        wrist_point = wrist_points.get(
            side_name
        )

        if wrist_point is None:
            continue

        hand = create_hand(
            context=context,
            collection=collection,
            character_name=character_name,
            side_name=side_name,
            location=wrist_point,
            hand_radius=hand_radius,
            hand_scale=hand_scale,
        )

        generated_objects.append(hand)

    return generated_objects
