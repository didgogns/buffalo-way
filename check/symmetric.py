from .base_check import BaseCheckStrategy
from poly_util import get_symbols

from sympy import Poly
from itertools import permutations
from typing import List


class SymmetricCheck(BaseCheckStrategy):
    @classmethod
    def check(cls, inequality: Poly, proof: List[str]) -> bool:
        symbols = get_symbols(inequality)
        for symbol_iteration in permutations(symbols):
            subbed_inequality = inequality.subs({
                key: val for key, val in zip(symbols, symbol_iteration)
            }, simultaneous=True)
            if not (inequality - subbed_inequality).is_zero:
                proof.append('This polynomial is not symmetric.')
                return False

        proof.append('This polynomial is symmetric.')
        return True
