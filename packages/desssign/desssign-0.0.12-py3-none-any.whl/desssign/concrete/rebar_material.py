from __future__ import annotations

import numpy as np

from framesss.pre.material import Material

from desssign.concrete.strength_classes import STEEL_STRENGTH_CLASSES
from desssign.concrete.constants import PARTIAL_FACTOR_STEEL


class RebarMaterial(Material):
    """
    Class for structural steel rebar material.

    Inherits from Material class and adds specific properties of steel rebar.

    :param steel_grade: Strength class of the rebar material.
    :ivar strength_class: Steel grade according to EN 1992-1-1:2004.
    :ivar f_yk: Characteristic yield strength of steel [MPa].
    :ivar k: Coefficient for the design yield strength of steel.
    :ivar epsilon_uk: Ultimate strain of steel.
    :ivar gamma_s: Partial safety factor for steel.
    :ivar e: Young's modulus of steel [MPa].
    """

    def __init__(
        self,
        steel_grade: str | None = None,
        f_yk: float | None = None,
        k: float = 1.08,
        epsilon_uk: float = 0.050,
        gamma_s: float = PARTIAL_FACTOR_STEEL,
    ) -> None:
        """Initialise concrete material properties."""
        self.strength_class = steel_grade

        if steel_grade is not None:
            if steel_grade not in STEEL_STRENGTH_CLASSES.keys():
                raise ValueError(
                    f"Steel grade '{steel_grade}' not recognised. "
                    f"Choose from: {[c for c in STEEL_STRENGTH_CLASSES.keys()]}."
                )
            self.f_yk = STEEL_STRENGTH_CLASSES.get(steel_grade).get("f_yk")
            self.k = STEEL_STRENGTH_CLASSES.get(steel_grade).get("k")
            self.epsilon_uk = STEEL_STRENGTH_CLASSES.get(steel_grade).get("epsilon_uk")
        else:
            if f_yk is None:
                raise ValueError("Steel grade or yield strength must be provided.")
            if f_yk <= 0:
                raise ValueError("Yield strength of steel must be positive.")
            self.f_yk = f_yk
            self.k = k
            self.epsilon_uk = epsilon_uk

        self.e: float = 200_000e6
        self.gamma_s = gamma_s

        poisson = 0.3  # TODO: Add Poisson's ratio

        super().__init__(
            label=steel_grade,
            elastic_modulus=self.e,  # Convert to Pa
            poissons_ratio=poisson,
            thermal_expansion_coefficient=10e-6,
            density=7850,
        )

    def __repr__(self) -> str:
        """Return the string representation of the SteelMaterial object."""
        return f"SteelMaterial({self.strength_class})"

    @property
    def f_yd(self) -> float:
        """Design yield strength of steel [MPa]."""
        return self.f_yk / self.gamma_s

    @property
    def f_yd2(self) -> float:
        """Design strength of steel [MPa]."""
        eps_uk = self.epsilon_uk
        eps_ud = self.epsilon_ud
        f_yd = self.f_yd
        eps_sy = self.epsilon_syd
        k = self.k
        f_yd2 = np.interp(
            x=eps_ud,
            xp=[eps_sy, eps_uk],
            fp=[f_yd, k * f_yd],
        )
        return f_yd2

    @property
    def f_yk2(self) -> float:
        """Characteristic strength of steel [MPa]."""
        return self.k * self.f_yk

    @property
    def epsilon_ud(self) -> float:
        """Design ultimate strain of steel."""
        return 0.9 * self.epsilon_uk

    @property
    def epsilon_syk(self) -> float:
        """Yield strain of steel."""
        return self.f_yk / self.e

    @property
    def epsilon_syd(self) -> float:
        return self.f_yd / self.e
