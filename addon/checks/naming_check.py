import bpy


DEFAULT_NAMES = (
    "Cube",
    "Plane",
    "Sphere",
    "Cylinder",
    "Cone",
    "Circle",
    "Torus",
    "Suzanne",
    "BezierCurve",
    "Curve",
    "Camera",
    "Light",
    "Empty",
)


def run_naming_check():
    """Validate object names."""

    results = []

    for obj in bpy.data.objects:

        status = "PASS"
        issues = []

        # Default Blender names
        if obj.name.startswith(DEFAULT_NAMES):
            status = "FAIL"
            issues.append("Uses default Blender object name.")

        # Duplicate names (.001, .002, etc.)
        if "." in obj.name:
            suffix = obj.name.split(".")[-1]

            if suffix.isdigit():
                status = "FAIL"
                issues.append("Appears to be an automatically duplicated name.")

        results.append({
            "object": obj.name,
            "status": status,
            "issues": issues,
        })

    return results
