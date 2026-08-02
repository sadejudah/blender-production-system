import bpy


class BPS_OT_RunAudit(bpy.types.Operator):
    """Run a production audit"""

    bl_idname = "bps.run_audit"
    bl_label = "Run Production Audit"
    bl_description = "Runs the Blender Production System audit"

    def execute(self, context):

        self.report({'INFO'}, "Production Audit Started")

        print("=" * 50)
        print("Blender Production System")
        print("Production Audit Started")
        print("=" * 50)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BPS_OT_RunAudit)


def unregister():
    bpy.utils.unregister_class(BPS_OT_RunAudit)
