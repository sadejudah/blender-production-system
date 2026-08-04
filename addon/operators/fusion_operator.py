import bpy


# ---------------------------------------------------------
# OBJECT HELPERS
# ---------------------------------------------------------

def deselect_everything():
    """Deselect all objects without depending on the current selection."""

    for obj in bpy.context.selected_objects:
        obj.select_set(False)


def remove_existing_fused_mesh(
    model_collection,
    fused_object_name,
):
    """Remove a previously generated fused mesh."""

    existing_object = bpy.data.objects.get(
        fused_object_name
    )

    if existing_object is None:
        return

    mesh_data = (
        existing_object.data
        if existing_object.type == "MESH"
        else None
    )

    bpy.data.objects.remove(
        existing_object,
        do_unlink=True,
    )

    if (
        mesh_data is not None
        and mesh_data.users == 0
    ):
        bpy.data.meshes.remove(mesh_data)


def duplicate_generated_parts(
    model_collection,
    character_name,
):
    """Duplicate the generated mannequin parts for fusion."""

    prefix = f"{character_name}_Base_"

    source_objects = [
        obj
        for obj in model_collection.objects
        if (
            obj.type == "MESH"
            and obj.name.startswith(prefix)
            and obj.get(
                "bps_generated_base_mesh",
                False,
            )
        )
    ]

    duplicated_objects = []

    for source_object in source_objects:
        duplicate = source_object.copy()
        duplicate.data = source_object.data.copy()

        duplicate.name = (
            f"{source_object.name}_FusionCopy"
        )

        model_collection.objects.link(
            duplicate
        )

        duplicate.hide_viewport = False
        duplicate.hide_render = False
        duplicate.hide_set(False)

        duplicated_objects.append(
            duplicate
        )

    return duplicated_objects


def delete_objects(objects):
    """Safely remove temporary objects and unused mesh data."""

    for obj in list(objects):
        if obj is None:
            continue

        mesh_data = (
            obj.data
            if obj.type == "MESH"
            else None
        )

        bpy.data.objects.remove(
            obj,
            do_unlink=True,
        )

        if (
            mesh_data is not None
            and mesh_data.users == 0
        ):
            bpy.data.meshes.remove(mesh_data)


# ---------------------------------------------------------
# FUSION OPERATOR
# ---------------------------------------------------------

class BPS_OT_FuseBaseMesh(bpy.types.Operator):
    """Fuse generated mannequin pieces into one sculpt-ready mesh."""

    bl_idname = "bps.fuse_base_mesh"
    bl_label = "Fuse Base Mesh"
    bl_description = (
        "Duplicate the generated mannequin, join the duplicated parts, "
        "and voxel-remesh them into one sculpt-ready mesh"
    )
    bl_options = {
        "REGISTER",
        "UNDO",
    }

    def execute(self, context):
        scene = context.scene

        character_name = scene.get(
            "bps_active_character",
            "",
        )

        if not character_name:
            self.report(
                {"ERROR"},
                "Create or activate a character project first.",
            )
            return {"CANCELLED"}

        character_height = scene.bps_character_height

        if character_height <= 0.0:
            self.report(
                {"ERROR"},
                "Character height must be greater than zero.",
            )
            return {"CANCELLED"}

        model_collection_name = (
            f"{character_name}_Model"
        )

        model_collection = bpy.data.collections.get(
            model_collection_name
        )

        if model_collection is None:
            self.report(
                {"ERROR"},
                (
                    f"Collection '{model_collection_name}' "
                    "was not found."
                ),
            )
            return {"CANCELLED"}

        fused_object_name = (
            f"{character_name}_Fused_Base_Mesh"
        )

        remove_existing_fused_mesh(
            model_collection=model_collection,
            fused_object_name=fused_object_name,
        )

        duplicated_objects = duplicate_generated_parts(
            model_collection=model_collection,
            character_name=character_name,
        )

        if not duplicated_objects:
            self.report(
                {"ERROR"},
                (
                    "No generated base-mesh parts were found. "
                    "Click Generate Base Mesh first."
                ),
            )
            return {"CANCELLED"}

        deselect_everything()

        for obj in duplicated_objects:
            obj.select_set(True)

        context.view_layer.objects.active = (
            duplicated_objects[0]
        )

        try:
            bpy.ops.object.join()
        except RuntimeError as error:
            delete_objects(
                duplicated_objects
            )

            self.report(
                {"ERROR"},
                f"Could not join the mannequin parts: {error}",
            )
            return {"CANCELLED"}

        fused_object = context.active_object
        fused_object.name = fused_object_name

        # -------------------------------------------------
        # VOXEL REMESH SETTINGS
        # -------------------------------------------------

        voxel_size = max(
            character_height * 0.012,
            0.004,
        )

        fused_object.data.remesh_mode = "VOXEL"
        fused_object.data.remesh_voxel_size = voxel_size
        fused_object.data.remesh_voxel_adaptivity = 0.0
        fused_object.data.use_remesh_fix_poles = True
        fused_object.data.use_remesh_preserve_volume = True

        try:
            bpy.ops.object.voxel_remesh()
        except RuntimeError as error:
            bpy.data.objects.remove(
                fused_object,
                do_unlink=True,
            )

            self.report(
                {"ERROR"},
                f"Voxel remesh failed: {error}",
            )
            return {"CANCELLED"}

        # -------------------------------------------------
        # FINALIZE THE FUSED MESH
        # -------------------------------------------------

        fused_object.name = fused_object_name

        for polygon in fused_object.data.polygons:
            polygon.use_smooth = True

        fused_object["bps_fused_base_mesh"] = True
        fused_object["bps_fusion_version"] = "0.8"
        fused_object["bps_character_name"] = character_name
        fused_object["bps_character_height"] = (
            character_height
        )
        fused_object["bps_voxel_size"] = voxel_size

        model_collection[
            "bps_fused_base_mesh_generated"
        ] = True

        model_collection[
            "bps_fused_base_mesh_name"
        ] = fused_object_name

        scene[
            "bps_character_status"
        ] = "Fused Base Mesh Generated"

        context.view_layer.objects.active = (
            fused_object
        )

        fused_object.select_set(True)

        self.report(
            {"INFO"},
            (
                f"Fused sculpt mesh generated for "
                f"{character_name}."
            ),
        )

        return {"FINISHED"}


classes = (
    BPS_OT_FuseBaseMesh,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
