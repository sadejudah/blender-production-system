"""Shared build context for the Blender Production System."""

from dataclasses import dataclass

from ..data import CharacterData
from ..data import resolve_character_data


@dataclass(frozen=True)
class BuildContext:
    """Immutable context passed to all generators."""

    character: CharacterData


def create_build_context(scene) -> BuildContext:
    """
    Create a build context from the active Blender scene.
    """

    template_key = getattr(
        scene,
        "bps_character_template",
        "GENERIC",
    )

    character = resolve_character_data(
        template_key
    )

    return BuildContext(
        character=character,
    )
