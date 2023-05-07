from .base_substitution import BaseSubstitutionStrategy
from poly_util import get_symbols
from sympy import Poly, Symbol
from typing import Tuple, List, Dict


class NoSubstitution(BaseSubstitutionStrategy):
    @classmethod
    def get_map(cls, inequality: Poly) -> Tuple[Dict, Symbol, str]:
        symbols = get_symbols(inequality)

        substitution_map = {x: x for x in symbols}
        return substitution_map, symbols[0], ''
