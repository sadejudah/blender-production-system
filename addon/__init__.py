bl_info = {
    "name": "Blender Production System",
    "author": "Patrice Newson",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > BPS",
    "description": (
        "Production auditing, certification, and workflow tools for Blender."
    ),
    "category": "Pipeline",
}

from .operators import audit_operator
from .operators import character_operator
from .operators import reference_operator
from .operators import view_operator
from .operators import blueprint_operator
from .ui import audit_panel
from .ui import character_panel


modules = (
    audit_operator,
    character_operator,
    reference_operator,
    blueprint_operator,
    audit_panel,
    character_panel,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":
    register()
