from .base_proof import BaseProofStrategy
from sympy import Poly, Symbol, Interval, oo
from sympy.abc import X
from poly_util import get_symbols
from poly_extrema import is_positive_poly
from typing import List


class TwoVariableProof(BaseProofStrategy):
    @classmethod
    def prove(
            cls, inequality: Poly, base_symbol: Symbol, proof: List[str], interval: Interval = Interval(0, oo)) -> bool:
        symbols = get_symbols(inequality)
        num_symbol = len(symbols)
        if num_symbol >= 2:
            raise ValueError('For TwoVariableProof, number of symbols must be 2')
        elif num_symbol == 1:
            # trivial
            return True
        else:
            not_base_symbol = symbols[0] if symbols[0] != base_symbol else symbols[1]
            univariate_inequality = inequality.subs({
                base_symbol: X,
                not_base_symbol: 1
            })
            return is_positive_poly(univariate_inequality, interval)
