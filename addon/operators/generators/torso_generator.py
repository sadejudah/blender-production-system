"""
Torso Generator

Creates the torso for the Blender Production System.
"""

import bpy

from .mesh_helpers import prepare_object


def create_torso(
    context,
    collection,
    character_name,
    location,
    scale,
):
    """
    Create a rounded torso.
    """

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24,
        ring_count=16,
        location=location,
    )

    obj = context.active_object

    obj.name = (
        f"{character_name}_Base_Chest"
    )

    obj.scale = scale

    prepare_object(obj)

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
    ] = "Torso"

    return obj
