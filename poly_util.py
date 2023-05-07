from sympy import Poly, Symbol, degree
from sympy.printing import latex


def get_symbols(polynomial: Poly) -> list:
    symbols = polynomial.free_symbols
    symbols = sorted(symbols, key=lambda x: x.name)
    return symbols


def get_deg_map(polynomial: Poly, symbol: Symbol) -> dict:
    poly_as_expr = polynomial.as_expr()
    deg_map = poly_as_expr.collect(symbol, evaluate=False)
    deg_map = {degree(key, symbol): val for key, val in deg_map.items()}
    return deg_map


def print_latex(polynomial: Poly) -> str:
    result = latex(polynomial)
    start_idx = len('\\operatorname{Poly}{\\left( ')
    end_idx = result.index(',')
    return result[start_idx:end_idx]


def cyclic_sum(polynomial: Poly) -> Poly:
    from sympy.abc import x, y, z
    poly_yzx = polynomial.subs({x: y, y: z, z: x}, simultaneous=True)
    poly_zxy = polynomial.subs({x: z, y: x, z: y}, simultaneous=True)
    return Poly(polynomial + poly_yzx + poly_zxy)
