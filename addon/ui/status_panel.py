import bpy


class BPS_PT_StatusPanel(bpy.types.Panel):
    """Active character status display."""

    bl_idname = "BPS_PT_status_panel"
    bl_label = "Status"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"
    bl_parent_id = "BPS_PT_character_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        active_character = scene.get(
            "bps_active_character",
            "",
        )

        if not active_character:
            info_box = layout.box()
            info_box.label(
                text="No active character",
                icon="INFO",
            )
            info_box.label(
                text="Create a character project to begin.",
            )
            return

        status_box = layout.box()

        status_box.label(
            text="ACTIVE CHARACTER",
            icon="CHECKMARK",
        )

        status_box.label(
            text=active_character,
        )

        status_box.separator()

        status_box.label(
            text="Production Status",
        )

        status_box.label(
            text=scene.get(
                "bps_character_status",
                "Ready for Setup",
            ),
            icon="INFO",
        )

        active_template = getattr(
            scene,
            "bps_character_template",
            "GENERIC",
        )

        status_box.separator()

        status_box.label(
            text="Template",
        )

        status_box.label(
            text=active_template.replace(
                "_",
                " ",
            ).title(),
        )


classes = (
    BPS_PT_StatusPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
