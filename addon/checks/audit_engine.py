from .transform_check import run_transform_check


def run_production_audit():
    """Run every available production check."""

    all_results = []

    # Transform inspection
    transform_results = run_transform_check()
    all_results.extend(transform_results)

    return all_results
