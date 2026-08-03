import bpy

REQUIRED_COLLECTIONS = (
    "CHARACTERS",
    "PROPS",
    "ENVIRONMENTS",
    "CAMERAS",
    "LIGHTS",
)


def run_collection_check():
    """Validate required production collections."""

    results = []

    existing = {collection.name for collection in bpy.data.collections}

    for name in REQUIRED_COLLECTIONS:

        if name in existing:
            status = "PASS"
            issues = []
        else:
            status = "FAIL"
            issues = [
                f"Missing required collection: {name}"
            ]

        results.append({
            "object": f"Collection: {name}",
            "status": status,
            "issues": issues,
        })

    return results
