"""
Character Template Registry

Provides predefined production templates used by the
Blender Production System.
"""

from copy import deepcopy

from .generic import TEMPLATE as GENERIC_TEMPLATE
from .leafy import TEMPLATE as LEAFY_TEMPLATE


TEMPLATES = {
    "GENERIC": GENERIC_TEMPLATE,
    "LEAFY": LEAFY_TEMPLATE,
}


def get_template(template_key):
    """Return a safe copy of a registered character template."""

    template = TEMPLATES.get(
        template_key,
        GENERIC_TEMPLATE,
    )

    return deepcopy(template)


def get_template_items():
    """Return Blender EnumProperty items for registered templates."""

    items = []

    for template_key, template in TEMPLATES.items():
        items.append(
            (
                template_key,
                template.get(
                    "name",
                    template_key.title(),
                ),
                template.get(
                    "description",
                    "Character production template",
                ),
            )
        )

    return tuple(items)


__all__ = (
    "GENERIC_TEMPLATE",
    "LEAFY_TEMPLATE",
    "TEMPLATES",
    "get_template",
    "get_template_items",
)