"""Resolved character production data.

This module converts a registered character template into one consistent
data object that operators and generators can use safely.
"""

from dataclasses import dataclass
from typing import Any

from ..templates import get_template


@dataclass(frozen=True)
class CharacterData:
    """Resolved production settings for one character."""

    template_key: str
    name: str
    description: str
    species: str
    height: float
    blueprint_preset: str

    head_style: str
    torso_style: str
    arm_style: str
    leg_style: str
    hand_style: str
    foot_style: str

    eye_style: str
    mouth_style: str

    rig_template: str | None
    material_template: str | None

    primary_color: tuple[float, float, float]
    secondary_color: tuple[float, float, float]
    accent_color: tuple[float, float, float]


def _string_value(
    template: dict[str, Any],
    key: str,
    fallback: str,
) -> str:
    """Return one clean string value from template data."""

    value = template.get(
        key,
        fallback,
    )

    if value is None:
        return fallback

    return str(value)


def _optional_string_value(
    template: dict[str, Any],
    key: str,
) -> str | None:
    """Return one optional string value."""

    value = template.get(key)

    if value in (
        None,
        "",
    ):
        return None

    return str(value)


def _color_value(
    template: dict[str, Any],
    key: str,
    fallback: tuple[float, float, float],
) -> tuple[float, float, float]:
    """Return a safe RGB color tuple."""

    value = template.get(
        key,
        fallback,
    )

    if not isinstance(
        value,
        (
            tuple,
            list,
        ),
    ):
        return fallback

    if len(value) < 3:
        return fallback

    try:
        return (
            float(value[0]),
            float(value[1]),
            float(value[2]),
        )

    except (
        TypeError,
        ValueError,
    ):
        return fallback


def resolve_character_data(
    template_key: str,
) -> CharacterData:
    """Resolve one registered template into CharacterData."""

    normalized_key = (
        template_key.strip().upper()
        if template_key
        else "GENERIC"
    )

    template = get_template(
        normalized_key
    )

    height = template.get(
        "height",
        1.0,
    )

    try:
        resolved_height = float(height)

    except (
        TypeError,
        ValueError,
    ):
        resolved_height = 1.0

    if resolved_height <= 0.0:
        resolved_height = 1.0

    blueprint_preset = _string_value(
        template,
        "blueprint_preset",
        "STANDARD",
    ).upper()

    if blueprint_preset not in {
        "PRESCHOOL",
        "CHILD",
        "STANDARD",
    }:
        blueprint_preset = "STANDARD"

    return CharacterData(
        template_key=normalized_key,
        name=_string_value(
            template,
            "name",
            "Generic",
        ),
        description=_string_value(
            template,
            "description",
            "Character production template",
        ),
        species=_string_value(
            template,
            "species",
            "Generic",
        ),
        height=resolved_height,
        blueprint_preset=blueprint_preset,
        head_style=_string_value(
            template,
            "head_style",
            "standard",
        ),
        torso_style=_string_value(
            template,
            "torso_style",
            "standard",
        ),
        arm_style=_string_value(
            template,
            "arm_style",
            "standard",
        ),
        leg_style=_string_value(
            template,
            "leg_style",
            "standard",
        ),
        hand_style=_string_value(
            template,
            "hand_style",
            "standard",
        ),
        foot_style=_string_value(
            template,
            "foot_style",
            "standard",
        ),
        eye_style=_string_value(
            template,
            "eye_style",
            "standard",
        ),
        mouth_style=_string_value(
            template,
            "mouth_style",
            "neutral",
        ),
        rig_template=_optional_string_value(
            template,
            "rig_template",
        ),
        material_template=_optional_string_value(
            template,
            "material_template",
        ),
        primary_color=_color_value(
            template,
            "primary_color",
            (
                0.50,
                0.50,
                0.50,
            ),
        ),
        secondary_color=_color_value(
            template,
            "secondary_color",
            (
                0.30,
                0.30,
                0.30,
            ),
        ),
        accent_color=_color_value(
            template,
            "accent_color",
            (
                0.80,
                0.80,
                0.80,
            ),
        ),
    )
