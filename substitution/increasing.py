from .base_substitution import BaseSubstitutionStrategy
from .free_symbol import get
from poly_util import get_symbols
from sympy import Poly, Symbol
from typing import Tuple, Dict


class IncreasingSubstitution(BaseSubstitutionStrategy):
    @classmethod
    def get_map(cls, inequality: Poly) -> Tuple[Dict, Symbol, str]:
        symbols = get_symbols(inequality)
        num_symbol = len(symbols)
        free_symbols = get(inequality, num_symbol - 1)
        free_symbols.insert(0, 0)
        first_symbol = symbols[0]

        substitution_map = {first_symbol: first_symbol}
        symbol_names = ', '.join([symbol.name for symbol in symbols])
        substitution_str = f'Let ${first_symbol} = \\min\\{{{symbol_names}\\}}$'
        value_string = first_symbol.name
        for idx in range(1, num_symbol):
            symbol = symbols[idx]
            last_symbol = symbols[idx - 1]
            last_value = substitution_map[last_symbol]
            value = last_value + free_symbols[idx]
            value_string += ' + '
            value_string += free_symbols[idx].name
            substitution_map[symbol] = value
            substitution_str += f', ${symbol} = {value_string}$'
        substitution_str += '.'
        return substitution_map, symbols[0], substitution_str
