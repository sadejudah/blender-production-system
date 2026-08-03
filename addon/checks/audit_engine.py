from .transform_check import run_transform_check
from .naming_check import run_naming_check
from .collection_check import run_collection_check


def run_production_audit():
    """Run every available production check."""

    all_results = []

    # Transform inspection
    all_results.extend(run_transform_check())

    # Naming inspection
    all_results.extend(run_naming_check())

    # Collection inspection
    all_results.extend(run_collection_check())

    return all_results
