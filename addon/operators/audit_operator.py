import bpy

from ..checks.audit_engine import run_production_audit
from ..reports.report_formatter import print_report


class BPS_OT_RunAudit(bpy.types.Operator):
    """Run the Blender Production System production audit."""

    bl_idname = "bps.run_audit"
    bl_label = "Run Production Audit"
    bl_description = "Inspect the current Blender scene for production issues"
    bl_options = {"REGISTER"}

    def execute(self, context):
        results = run_production_audit()

        active_object = context.active_object
        asset_name = (
            active_object.name
            if active_object
            else "Current Scene"
        )

        summary = print_report(asset_name, results)

        # Store the latest audit results in the Blender scene.
        # The Studio Dashboard reads these values.
        scene = context.scene
        scene["bps_last_score"] = int(summary["score"])
        scene["bps_last_passes"] = int(summary["passes"])
        scene["bps_last_failures"] = int(summary["failures"])
        scene["bps_last_status"] = str(summary["status"])
        scene["bps_audit_has_run"] = True

        # Refresh the Blender interface so the dashboard updates immediately.
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()

        self.report(
            {"INFO"},
            (
                f"Score: {summary['score']}% | "
                f"{summary['passes']} Passed | "
                f"{summary['failures']} Failed"
            ),
        )

        return {"FINISHED"}


classes = (
    BPS_OT_RunAudit,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
