import bpy

from ..checks.transform_check import run_transform_check


class BPS_OT_RunAudit(bpy.types.Operator):
    """Run the Blender Production System production audit."""

    bl_idname = "bps.run_audit"
    bl_label = "Run Production Audit"
    bl_description = "Inspect the current Blender scene for production issues"
    bl_options = {"REGISTER"}

    def execute(self, context):
        results = run_transform_check()

        print("=" * 60)
        print("Blender Production System")
        print("Transform Inspection")
        print("=" * 60)

        passes = 0
        fails = 0

        for result in results:
            if result["status"] == "PASS":
                passes += 1
            else:
                fails += 1

            print(result["object"])
            print("Status:", result["status"])

            for issue in result["issues"]:
                print(" -", issue)

        print("=" * 60)
        print("PASS:", passes)
        print("FAIL:", fails)
        print("=" * 60)

        self.report(
            {"INFO"},
            f"{passes} Passed | {fails} Failed",
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
