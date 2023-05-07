from sympy import Poly, symbols, Symbol
from poly_util import get_symbols
from typing import List, Union


def get(polynomial: Poly, n: int) -> List[Union[Symbol, int]]:
    symbol_candidate = symbols('a:z')
    poly_symbols = get_symbols(polynomial)
    filtered_symbol_candidate = [s for s in symbol_candidate if s not in poly_symbols]
    return filtered_symbol_candidate[:n]
