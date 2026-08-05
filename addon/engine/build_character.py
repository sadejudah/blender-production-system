"""High-level character build entry point."""

from .build_context import create_build_context
from .generator_engine import GeneratorEngine


def build_character(scene):
    """
    Build the active character.
    """

    context = create_build_context(scene)

    engine = GeneratorEngine(
        context=context,
    )

    engine.build()

    return engine
