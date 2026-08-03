from .score import calculate_score


def get_overall_status(score):
    """Return the production status for a readiness score."""

    if score == 100:
        return "CERTIFIED — PRODUCTION READY"

    if score >= 70:
        return "CONDITIONAL PASS"

    return "NOT PRODUCTION READY"


def print_report(asset_name, results):
    """Print a formatted Blender Production System report."""

    passes = sum(
        1 for result in results
        if result["status"] == "PASS"
    )
    failures = len(results) - passes

    score = calculate_score(results)
    overall_status = get_overall_status(score)

    print("=" * 60)
    print(" Blender Production System")
    print(" Production Readiness Audit")
    print("=" * 60)

    print()
    print(f"Asset: {asset_name}")
    print("-" * 60)
    print()

    for result in results:
        status = result["status"]
        icon = "[PASS]" if status == "PASS" else "[FAIL]"

        print(f"{icon} {result['object']}")

        for issue in result["issues"]:
            print(f"       - {issue}")

    print()
    print("-" * 60)
    print("Summary")
    print()

    print(f"Passed  : {passes}")
    print(f"Failed  : {failures}")
    print(f"Score   : {score}%")
    print(f"Status  : {overall_status}")

    print("=" * 60)

    return {
        "passes": passes,
        "failures": failures,
        "score": score,
        "status": overall_status,
    }
