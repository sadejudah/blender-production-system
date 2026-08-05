"""Base-mesh build adapter.

This module provides one stable engine entry point for generating the
active character's base mesh. The existing Blender operator remains
responsible for the proven geometry workflow for now.
"""

import bpy

from .build_context import BuildContext


class BaseMeshBuildError(RuntimeError):
    """Raised when the base-mesh build cannot be completed."""


def build_base_mesh(
    context: BuildContext,
) -> set[str]:
    """Run the existing BPS base-mesh operator through the engine."""

    character = context.character

    scene = bpy.context.scene

    # Synchronize the resolved character data with the scene properties
    # currently used by the existing base-mesh operator.
    scene.bps_character_height = character.height
    scene.bps_blueprint_preset = character.blueprint_preset

    scene["bps_selected_template"] = character.template_key
    scene["bps_selected_template_name"] = character.name
    scene["bps_selected_species"] = character.species

    result = bpy.ops.bps.generate_base_mesh_legacy()

    if "FINISHED" not in result:
        raise BaseMeshBuildError(
            f"Base-mesh generation failed for {character.name}."
        )

    return result
