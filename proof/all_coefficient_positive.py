from .base_proof import BaseProofStrategy
from buffalo_polynomial import BuffaloPolynomial
from sympy import Poly, Symbol, Interval, oo
from poly_util import get_deg_map
from typing import List


# TODO create some recursion for 4+ variable proof
class AllCoefficientPositiveProof(BaseProofStrategy):
    @classmethod
    def prove(
            cls, inequality: Poly, base_symbol: Symbol, proof: List[str], interval: Interval = Interval(0, oo)) -> bool:
        # Interval does not matter here
        deg_map = get_deg_map(inequality, base_symbol)
        all_positiveness = True
        for coefficient in deg_map.values():
            coefficient_inequality = BuffaloPolynomial()
            if not coefficient_inequality.proof():
                all_positiveness = False
                break
        if all_positiveness:
            return True
        return False
