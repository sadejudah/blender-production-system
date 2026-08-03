import bpy
from pathlib import Path


class BPS_OT_CreateCharacter(bpy.types.Operator):
    """Create a complete Blender workspace for a new character."""

    bl_idname = "bps.create_character"
    bl_label = "Create Character"
    bl_description = "Create a structured Blender workspace for a new character"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        character_name = context.scene.bps_character_name.strip()
        project_root = context.scene.bps_character_project_root.strip()

        if not character_name:
            self.report(
                {"ERROR"},
                "Enter a character name before creating the character.",
            )
            return {"CANCELLED"}

        if not project_root:
            self.report(
                {"ERROR"},
                "Choose a project destination.",
            )
            return {"CANCELLED"}

        root_name = character_name
        project_path = Path(project_root) / root_name

        if project_path.exists():
            self.report(
                {"ERROR"},
                f"A project folder named '{root_name}' already exists.",
            )
            return {"CANCELLED"}

        if bpy.data.collections.get(root_name):
            self.report(
                {"ERROR"},
                f"A collection named '{root_name}' already exists.",
            )
            return {"CANCELLED"}

        folder_names = (
            "00_Project_Admin",
            "01_Reference",
            "02_Model",
            "03_Rig",
            "04_Textures",
            "05_Materials",
            "06_Animation",
            "07_Render",
            "08_Exports",
            "09_Deliverables",
            "10_Backups",
        )

        try:
            project_path.mkdir(parents=True, exist_ok=False)

            for folder_name in folder_names:
                (project_path / folder_name).mkdir(exist_ok=False)

        except OSError as error:
            self.report(
                {"ERROR"},
                f"Could not create the project folders: {error}",
            )
            return {"CANCELLED"}

        scene_collection = context.scene.collection

        root_collection = bpy.data.collections.new(root_name)
        scene_collection.children.link(root_collection)

        subcollection_names = (
            "Reference",
            "Model",
            "Rig",
            "Textures",
            "Materials",
            "Animation",
            "Render",
            "Hidden",
        )

        for subcollection_name in subcollection_names:
            full_name = f"{character_name}_{subcollection_name}"
            new_collection = bpy.data.collections.new(full_name)
            root_collection.children.link(new_collection)

        # -------------------------------------------------
        # Create Ground Collection
        # -------------------------------------------------

        ground_collection = bpy.data.collections.new(
            f"{character_name}_Ground"
        )
        root_collection.children.link(ground_collection)

        # -------------------------------------------------
        # Create Ground Plane
        # -------------------------------------------------

        bpy.ops.mesh.primitive_plane_add(
            size=10.0,
            location=(0.0, 0.0, 0.0),
        )

        ground_plane = context.active_object
        ground_plane.name = f"{character_name}_Ground_Plane"

        # Move the plane out of its default collection.
        for collection in list(ground_plane.users_collection):
            collection.objects.unlink(ground_plane)

        ground_collection.objects.link(ground_plane)

        # Lock transforms.
        ground_plane.lock_location = (True, True, True)
        ground_plane.lock_rotation = (True, True, True)
        ground_plane.lock_scale = (True, True, True)

        # Keep it visible in the viewport but out of final renders.
        ground_plane.hide_render = True
        ground_plane.display_type = "SOLID"

        # -------------------------------------------------
        # Create Gray Ground Material
        # -------------------------------------------------

        material_name = f"{character_name}_Ground_Material"
        ground_material = bpy.data.materials.new(material_name)
        ground_material.diffuse_color = (
            0.18,
            0.18,
            0.18,
            1.0,
        )

        ground_plane.data.materials.append(ground_material)

        # -------------------------------------------------
        # Store Character Metadata
        # -------------------------------------------------

        context.scene["bps_active_character"] = character_name
        context.scene["bps_character_status"] = "Ready for Setup"
        context.scene["bps_character_project_path"] = str(project_path)

        self.report(
            {"INFO"},
            f"Character project created for {character_name}.",
        )

        return {"FINISHED"}


classes = (
    BPS_OT_CreateCharacter,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)