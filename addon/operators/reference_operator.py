import bpy
from pathlib import Path


class BPS_OT_ImportCharacterReferences(bpy.types.Operator):
    """Import character reference images into Blender."""

    bl_idname = "bps.import_character_references"
    bl_label = "Import Character References"
    bl_description = "Import front, side, and back character reference images"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        character_name = scene.get("bps_active_character", "")

        if not character_name:
            self.report(
                {"ERROR"},
                "Create or activate a character project first.",
            )
            return {"CANCELLED"}

        reference_paths = {
            "Front": scene.bps_character_front_reference.strip(),
            "Side": scene.bps_character_side_reference.strip(),
            "Back": scene.bps_character_back_reference.strip(),
        }

        selected_references = {
            view_name: file_path
            for view_name, file_path in reference_paths.items()
            if file_path
        }

        if not selected_references:
            self.report(
                {"ERROR"},
                "Choose at least one reference image.",
            )
            return {"CANCELLED"}

        reference_collection_name = f"{character_name}_Reference"
        reference_collection = bpy.data.collections.get(
            reference_collection_name
        )

        if reference_collection is None:
            self.report(
                {"ERROR"},
                f"Collection '{reference_collection_name}' was not found.",
            )
            return {"CANCELLED"}

        imported_count = 0

        for view_name, file_path in selected_references.items():
            image_path = Path(bpy.path.abspath(file_path))

            if not image_path.is_file():
                self.report(
                    {"WARNING"},
                    f"{view_name} reference file was not found.",
                )
                continue

            object_name = f"{character_name}_{view_name}_Reference"

            existing_object = bpy.data.objects.get(object_name)
            if existing_object:
                bpy.data.objects.remove(existing_object, do_unlink=True)

            image = bpy.data.images.load(
                str(image_path),
                check_existing=True,
            )

            reference_object = bpy.data.objects.new(
                object_name,
                None,
            )

            reference_object.empty_display_type = "IMAGE"
            reference_object.data = image
            reference_object.empty_display_size = 2.0
            reference_object.color[3] = 0.65
            reference_object.show_in_front = True
            reference_object.hide_render = True

            reference_collection.objects.link(reference_object)

            reference_transforms = {
                "Front": {
                    "location": (0.0, 0.0, 1.0),
                    "rotation": (
                        1.57079632679,
                        0.0,
                        0.0,
                    ),
                    "size": 2.0,
                },
                "Side": {
                    "location": (-2.5, 0.0, 1.0),
                    "rotation": (
                        1.57079632679,
                        0.0,
                        0.0,
                    ),
                    "size": 2.0,
                },
                "Back": {
                    "location": (2.5, 0.0, 1.0),
                    "rotation": (
                        1.57079632679,
                        0.0,
                        0.0,
                    ),
                    "size": 2.0,
                },
            }

            transform = reference_transforms[view_name]

            reference_object.location = transform["location"]
            reference_object.rotation_euler = transform["rotation"]
            reference_object.empty_display_size = transform["size"]

            reference_object.lock_location = (True, True, True)
            reference_object.lock_rotation = (True, True, True)
            reference_object.lock_scale = (True, True, True)

            imported_count += 1

        if imported_count == 0:
            self.report(
                {"ERROR"},
                "No valid reference images were imported.",
            )
            return {"CANCELLED"}

        scene["bps_character_status"] = "References Imported"

        self.report(
            {"INFO"},
            f"Imported {imported_count} character reference image(s).",
        )

        return {"FINISHED"}


classes = (
    BPS_OT_ImportCharacterReferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
