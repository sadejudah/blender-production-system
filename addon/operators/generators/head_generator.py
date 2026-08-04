"""
Head Generator

Creates the character head for the Blender Production System.
"""

import bpy

from .mesh_helpers import prepare_object


def create_head(
    context,
    collection,
    character_name,
    location,
    scale,
):
    """
    Create a rounded production head.
    """

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24,
        ring_count=16,
        location=location,
    )

    obj = context.active_object

    obj.name = (
        f"{character_name}_Base_Head"
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
    ] = "Head"

    return obj
