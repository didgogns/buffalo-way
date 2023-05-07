from .base_check import BaseCheckStrategy
from sympy import Poly
from typing import List


class NoCheck(BaseCheckStrategy):
    @classmethod
    def check(cls, inequality: Poly, proof: List[str]) -> bool:
        return True
