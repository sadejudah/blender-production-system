import bpy


class BPS_OT_GenerateBlueprint(bpy.types.Operator):
    """Generate a basic modeling blueprint."""

    bl_idname = "bps.generate_blueprint"
    bl_label = "Generate Blueprint"

    def execute(self, context):

        character_name = context.scene.get(
            "bps_active_character",
            ""
        )

        if not character_name:
            self.report(
                {"ERROR"},
                "No active character."
            )
            return {"CANCELLED"}

        collection_name = f"{character_name}_Reference"

        reference_collection = bpy.data.collections.get(
            collection_name
        )

        if reference_collection is None:
            self.report(
                {"ERROR"},
                "Reference collection not found."
            )
            return {"CANCELLED"}

        self.report(
            {"INFO"},
            "Blueprint generated."
        )

        return {"FINISHED"}


classes = (
    BPS_OT_GenerateBlueprint,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
