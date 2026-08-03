def calculate_score(results):
    """Calculate production readiness score."""

    total = len(results)

    if total == 0:
        return 100

    passed = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    return round((passed / total) * 100)
