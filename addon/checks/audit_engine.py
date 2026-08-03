from .naming_check import run_naming_check
from .transform_check import run_transform_check


def run_production_audit():
    """Run every available production check."""

    all_results = []

    # Transform inspection
    all_results.extend(run_transform_check())

    # Object naming inspection
    all_results.extend(run_naming_check())

    return all_results
