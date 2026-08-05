"""Generator Engine for the Blender Production System."""

from dataclasses import dataclass

from .build_context import BuildContext


@dataclass
class GeneratorEngine:
    """Coordinates all character generators."""

    context: BuildContext

    def build(self):
        """Build the complete character."""

        self.build_head()
        self.build_torso()
        self.build_arms()
        self.build_legs()
        self.build_feet()

    # ---------------------------------------------------------
    # Individual Generators
    # ---------------------------------------------------------

    def build_head(self):
        print(
            f"[BPS] Head Generator -> "
            f"{self.context.character.head_style}"
        )

    def build_torso(self):
        print(
            f"[BPS] Torso Generator -> "
            f"{self.context.character.torso_style}"
        )

    def build_arms(self):
        print(
            f"[BPS] Arm Generator -> "
            f"{self.context.character.arm_style}"
        )

    def build_legs(self):
        print(
            f"[BPS] Leg Generator -> "
            f"{self.context.character.leg_style}"
        )

    def build_feet(self):
        print(
            f"[BPS] Foot Generator -> "
            f"{self.context.character.foot_style}"
        )
