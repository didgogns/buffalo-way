from sympy import real_roots
from sympy.abc import X
from sympy import Poly, diff, Interval, oo


def is_positive_poly(func: Poly, interval: Interval = Interval(0, oo)):
    d1 = diff(func, X)
    if func.subs(X, interval.inf).is_negative:
        return False
    if func.subs(X, interval.sup).is_negative:
        return False
    extrema = real_roots(d1)
    for ex in extrema:
        if interval.contains(ex) and func.subs(X, ex).is_negative:
            return False
    return True


def binary_search_best_number(func: Poly, degree_in_question: int, interval: Interval = Interval(0, oo)):
    if degree_in_question % 2:
        func = Poly(func.subs(X, X ** 2).as_expr())
        interval = Interval(interval.inf ** 0.5, interval.sup ** 0.5)
    else:
        degree_in_question //= 2
    if is_positive_poly(func, interval):
        low = 0
        high = 1
        while True:
            if not is_positive_poly(func - high * X ** degree_in_question, interval):
                break
            high *= 2
    else:
        low = -1
        high = 0
        while True:
            if is_positive_poly(func - low * X ** degree_in_question, interval):
                break
            low *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        if is_positive_poly(func - mid * X ** degree_in_question, interval):
            low = mid
        else:
            high = mid
    return low


if __name__ == '__main__':
    f = Poly(156*X**8+531*X**7+2*X**6-632*X**5-152*X**4+867*X**3+834*X**2+299*X+40)
    print(is_positive_poly(f))

    f = Poly(X**2 - 1)
    print(is_positive_poly(f, Interval(1, oo)))

    f = Poly(390 * X ** 3 + 1134 * X ** 2 - 1056 * X + 390)
    print(is_positive_poly(f))
    print(binary_search_best_number(f, 3))
