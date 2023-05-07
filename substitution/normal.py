from .base_substitution import BaseSubstitutionStrategy
from .free_symbol import get
from poly_util import get_symbols
from sympy import Poly, Symbol
from typing import Tuple, Dict


class NormalSubstitution(BaseSubstitutionStrategy):
    @classmethod
    def get_map(cls, inequality: Poly) -> Tuple[Dict, Symbol, str]:
        symbols = get_symbols(inequality)
        num_symbol = len(symbols)
        free_symbols = get(inequality, num_symbol - 1)
        free_symbols.insert(0, 0)
        first_symbol = symbols[0]

        substitution_map = dict()
        symbol_names = ', '.join([symbol.name for symbol in symbols])
        substitution_str = f'Let ${first_symbol.name} = \\min\\{{{symbol_names}\\}}$'
        for i in range(num_symbol):
            symbol = symbols[i]
            free_symbol = free_symbols[i]
            substitution_map[symbol] = first_symbol + free_symbol
            if symbol != first_symbol:
                substitution_str += f', ${symbol} = {first_symbol} + {free_symbol}$'
        substitution_str += '.'
        return substitution_map, first_symbol, substitution_str
