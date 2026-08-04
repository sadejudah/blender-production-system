bl_info = {
    "name": "Blender Production System",
    "author": "Patrice Newson",
    "version": (1, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > BPS",
    "description": (
        "A modular production pipeline for creating "
        "animation-ready characters in Blender."
    ),
    "category": "Pipeline",
}


# ---------------------------------------------------------
# OPERATOR MODULES
# ---------------------------------------------------------

from .operators import audit_operator
from .operators import character_operator
from .operators import reference_operator
from .operators import view_operator
from .operators import blueprint_operator
from .operators import model_operator
from .operators import base_mesh_operator
from .operators import fusion_operator
from .operators import sculpt_operator


# ---------------------------------------------------------
# UI MODULES
# ---------------------------------------------------------

from .ui import audit_panel
from .ui import character_panel
from .ui import project_panel
from .ui import reference_panel
from .ui import status_panel


# ---------------------------------------------------------
# REGISTRATION ORDER
# ---------------------------------------------------------

modules = (
    # Operators
    audit_operator,
    character_operator,
    reference_operator,
    view_operator,
    blueprint_operator,
    model_operator,
    base_mesh_operator,
    fusion_operator,
    sculpt_operator,

    # Main panels
    audit_panel,
    character_panel,

    # Character-panel child panels
    project_panel,
    reference_panel,
    status_panel,
)


def register():
    """Register all Blender Production System modules."""

    for module in modules:
        module.register()


def unregister():
    """Unregister all modules in reverse order."""

    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":
    register()
