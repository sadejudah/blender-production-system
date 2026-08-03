def print_report(asset_name, results):
    """Print a formatted Blender Production System report."""

    print("=" * 60)
    print(" Blender Production System")
    print(" Production Readiness Audit")
    print("=" * 60)

    print()
    print(f"Asset: {asset_name}")
    print("-" * 60)
    print()

    passes = 0
    failures = 0

    for result in results:
        status = result["status"]

        if status == "PASS":
            icon = "✓"
            passes += 1
        else:
            icon = "✖"
            failures += 1

        print(f"{icon} {result['object']}: {status}")

        for issue in result["issues"]:
            print(f"    - {issue}")

    print()
    print("-" * 60)
    print("Summary")
    print()

    print(f"Passes : {passes}")
    print(f"Failures: {failures}")

    if failures == 0:
        overall = "PASS"
    else:
        overall = "CONDITIONAL PASS"

    print(f"Status : {overall}")

    print("=" * 60)
