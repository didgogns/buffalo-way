from .base_proof import BaseProofStrategy
from sympy import Poly, Symbol, Interval, oo
from sympy.abc import X
from sympy.printing import latex
from poly_util import get_symbols, get_deg_map
from poly_extrema import is_positive_poly, binary_search_best_number
from typing import List


class StandardProof(BaseProofStrategy):
    @classmethod
    def prove(
            cls, inequality: Poly, base_symbol: Symbol, proof: List[str], interval: Interval = Interval(0, oo)) -> bool:
        symbols = get_symbols(inequality)
        max_deg = inequality.homogeneous_order()
        num_symbol = len(symbols)
        if num_symbol != 3:
            return False
        deg_map = get_deg_map(inequality, base_symbol)
        t_poly = Poly(0, X)
        a, b = [symbol for symbol in symbols if symbol != base_symbol]
        proof.append(f'If we let $X = \\frac{{{base_symbol}}}{{\\sqrt{{{a}}}\\sqrt{{{b}}}}}$,')
        if interval != Interval(0, oo):
            proof.append(f'For ${{{a}}}/{{{b}}}$ in range ${latex(interval)}$, the polynomial is larger than')
        else:
            proof.append('The polynomial is larger than')
        for deg, coefficient in deg_map.items():
            term = coefficient.subs({a: X, b: 1})
            best_number = binary_search_best_number(term, max_deg - deg, interval)
            t_poly += X ** deg * best_number
        t_poly_str = latex(t_poly.as_expr())
        proof.append(f'$$\\left({t_poly_str}\\right)\\left(\\sqrt{{{a}}}\\sqrt{{{b}}}\\right)^{{{max_deg}}}$$')
        if is_positive_poly(t_poly):
            proof.append(', which is positive.')
            return True
        return False
