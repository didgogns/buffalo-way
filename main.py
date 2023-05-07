from sympy import Interval, oo
from sympy.abc import x, y, z
from poly_util import cyclic_sum

from buffalo_polynomial import BuffaloPolynomial
from check import CyclicCheck
from substitution import NormalSubstitution
from proof import StandardProof


def proof_1777075():
    denominator_x = 13 * x ** 2 + 5 * y ** 2
    denominator_y = 13 * y ** 2 + 5 * z ** 2
    denominator_z = 13 * z ** 2 + 5 * x ** 2
    inequality = cyclic_sum(18 * x ** 3 * denominator_y * denominator_z)
    inequality -= (x + y + z) * denominator_x * denominator_y * denominator_z

    buffalo_way = BuffaloPolynomial()
    buffalo_way.polynomial = inequality
    buffalo_way.check = CyclicCheck
    buffalo_way.substitution = NormalSubstitution
    buffalo_way.proof_strategy = StandardProof
    do_proof(buffalo_way)


def proof_3709646():
    denominator_x = 133 * x ** 3 + 81 * y ** 3
    denominator_y = 133 * y ** 3 + 81 * z ** 3
    denominator_z = 133 * z ** 3 + 81 * x ** 3
    inequality = cyclic_sum(214 * x ** 4 * denominator_y * denominator_z)
    inequality -= (x + y + z) * denominator_x * denominator_y * denominator_z

    buffalo_way = BuffaloPolynomial()
    buffalo_way.polynomial = inequality
    buffalo_way.check = CyclicCheck
    buffalo_way.substitution = NormalSubstitution
    buffalo_way.proof_strategy = StandardProof
    do_proof(buffalo_way)


# This could be another proof strategy...?
def do_proof(buffalo_way):
    unit = 1
    while True:
        start = 0
        while True:
            buffalo_way.range = Interval(start / unit, oo)
            result, proof = buffalo_way.proof()
            if result:
                for line in proof:
                    print(line)
                    print()
                return
            increment = 1
            buffalo_way.range = Interval(start / unit, (start + increment) / unit)
            result, proof = buffalo_way.proof()
            if not result:
                print(f'Unit {unit} failed. Retry with larger unit.')
                break
            while result:
                increment *= 2
                buffalo_way.range = Interval(start / unit, (start + increment) / unit)
                result, proof = buffalo_way.proof()
            low = start
            high = start + increment
            while low + 1 < high:
                middle = (low + high) // 2
                buffalo_way.range = Interval(start / unit, middle / unit)
                result, proof = buffalo_way.proof()
                if result:
                    low = middle
                else:
                    high = middle
            end = low
            buffalo_way.range = Interval(start / unit, end / unit)
            result, proof = buffalo_way.proof()
            for line in proof:
                print(line)
                print()
            start = end
        unit *= 10


if __name__ == '__main__':
    proof_3709646()
