import bpy
from pathlib import Path


class BPS_OT_CreateCharacter(bpy.types.Operator):
    """Create the initial Blender collections for a new character."""

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