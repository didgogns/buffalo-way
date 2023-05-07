from .base_substitution import BaseSubstitutionStrategy
from .free_symbol import get
from poly_util import get_symbols
from sympy import Poly, Symbol
from typing import Tuple, Dict


class TriangleSubstitution(BaseSubstitutionStrategy):
    @classmethod
    def get_map(cls, inequality: Poly) -> Tuple[Dict, Symbol, str]:
        symbols = get_symbols(inequality)
        num_symbol = len(symbols)
        if num_symbol != 3:
            raise ValueError('For TriangleSubstitution, number of symbols must be 3')
        free_symbols = get(inequality, 3)
        substitution_str = f'Let ${symbols[0]} = {free_symbols[0]} + {free_symbols[1]}$, '
        substitution_str += f'${symbols[1]} = {free_symbols[1]} + {free_symbols[2]}$, '
        substitution_str += f'${symbols[2]} = {free_symbols[2]} + {free_symbols[0]}$.'
        return {
            symbols[0]: free_symbols[0] + free_symbols[1],
            symbols[1]: free_symbols[1] + free_symbols[2],
            symbols[2]: free_symbols[2] + free_symbols[0]
        }, free_symbols[0], substitution_str
