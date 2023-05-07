from .base_check import BaseCheckStrategy
from poly_util import get_symbols
from sympy import Poly
from typing import List


class CyclicCheck(BaseCheckStrategy):
    @classmethod
    def check(cls, inequality: Poly, proof: List[str]) -> bool:
        symbols = get_symbols(inequality)
        for idx in range(len(symbols)):
            rotated_variable = symbols[idx:] + symbols[:idx]
            subbed_inequality = inequality.subs({
                key: val for key, val in zip(symbols, rotated_variable)
            }, simultaneous=True)
            if not (inequality - subbed_inequality).is_zero:
                proof.append('This polynomial is not cyclic.')
                return False
        proof.append('This polynomial is symmetric.')
        return True
