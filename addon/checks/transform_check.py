import bpy


def run_transform_check():

    results = []

    for obj in bpy.context.scene.objects:

        issues = []

        if obj.location.length > 0.0001:
            issues.append("Location not applied")

        if any(abs(r) > 0.0001 for r in obj.rotation_euler):
            issues.append("Rotation not applied")

        if any(abs(s - 1.0) > 0.0001 for s in obj.scale):
            issues.append("Scale not applied")

        if issues:
            results.append({
                "object": obj.name,
                "status": "FAIL",
                "issues": issues
            })
        else:
            results.append({
                "object": obj.name,
                "status": "PASS",
                "issues": []
            })

    return results
