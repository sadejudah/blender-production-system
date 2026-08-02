bl_info = {
    "name": "Blender Production System",
    "author": "Patrice Newson",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > BPS",
    "description": (
        "Production auditing, certification, and workflow tools for Blender."
    ),
    "category": "Pipeline",
}


def register():
    print("Blender Production System loaded.")


def unregister():
    print("Blender Production System unloaded.")


if __name__ == "__main__":
    register()
