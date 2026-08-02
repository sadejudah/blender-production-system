import bpy


class BPS_PT_AuditPanel(bpy.types.Panel):
    """Main Blender Production System panel."""

    bl_idname = "BPS_PT_audit_panel"
    bl_label = "Blender Production System"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Production Readiness Auditor")
        layout.separator()

        layout.operator(
            "bps.run_audit",
            text="Run Production Audit",
            icon="CHECKMARK",
        )

        layout.separator()
        layout.label(text="Version 0.1.0")


classes = (
    BPS_PT_AuditPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
