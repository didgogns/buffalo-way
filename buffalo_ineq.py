from sympy.abc import x, y, z, u, v, X
from sympy import Poly, degree, Interval, oo
from poly_extrema import is_positive_poly, binary_search_best_number

from typing import List, Tuple


class BuffaloInequality:
    def __init__(self, polynomial):
        self.polynomial: Poly = polynomial
        self.poly_variables = list(self.polynomial.free_symbols)
        self.substitution = [x, x + u, x + v]
        self.base_variable = x
        self.poly_variables_after_substitution = [u, v]
        self.is_substitution_necessary = True
        self.interval = Interval(0, oo)

    def solve(self) -> Tuple[List[str], bool]:
        proof = [f'Proving whether {self.polynomial.as_expr()} is positive']
        # Polynomial should be homogeneous
        if not self.polynomial.is_homogeneous:
            proof.append('The polynomial should be homogeneous!')
            return proof, False

        for var in self.poly_variables:
            change_map = {key: 0 for key in self.poly_variables}
            change_map[var] = 1
            if self.polynomial.subs(change_map).is_negative:
                proof.append('The polynomial should be actually positive!')
                return proof, False

        if self.is_substitution_necessary:
            if not len(self.poly_variables) == len(self.substitution):
                message = ('If is_substitution_necessary, poly_variables and substitution must be same length '
                           'for actual substitution to happen.')
                proof.append(message)
                return proof, False

            # Polynomial should be cyclic
            for idx in range(len(self.poly_variables)):
                rotated_variable = self.poly_variables[-idx:] + self.poly_variables[:-idx]
                rotated_poly = self.polynomial.subs({
                    key: val for key, val in zip(self.poly_variables, rotated_variable)
                }, simultaneous=True)
                if not (self.polynomial - rotated_poly).is_zero:
                    proof.append('If is_substitution_necessary, the polynomial should be cyclic')
                    return proof, False
            # Polynomial should be 0 when all variables are equal
            if not self.polynomial.subs({key: 1 for key in self.poly_variables}).is_zero:
                proof.append('If is_substitution_necessary, the polynomial should be 0 when all variables are equal')
                return proof, False
            for variable, sub in zip(self.poly_variables, self.substitution):
                self.polynomial = self.polynomial.subs(variable, sub)

        poly_as_expr = self.polynomial.as_expr().expand()
        max_deg = self.polynomial.homogeneous_order()
        deg_map = poly_as_expr.collect(self.base_variable, evaluate=False)
        deg_map = {degree(key, self.base_variable): val for key, val in deg_map.items()}
        if self.is_substitution_necessary:
            pretty_poly = ''
            for key, val in sorted(deg_map.items(), reverse=True):
                if val:
                    if pretty_poly:
                        pretty_poly += '\n + '
                    pretty_poly += f'{self.base_variable} ** {key} * ({val})'
            proof.append(f'Substitution gives the polynomial {pretty_poly}')

        if len(self.poly_variables) < 2:
            proof.append('The polynomial is trivially positive.')
            return proof, True
        elif len(self.poly_variables) == 2:
            univariate_poly = self.polynomial.subs(
                {
                    self.poly_variables[0]: X,
                    self.poly_variables[1]: 1
                }
            )
            if not is_positive_poly(univariate_poly, self.interval):
                proof.append('The polynomial should be actually positive!')
                return proof, False
            proof.append(f'The polynomial is positive because {univariate_poly.as_expr()} is positive for X > 0')
            return proof, True

        all_positive = True
        sub_proofs = list()
        for deg, coeff in deg_map.items():
            sub_ineq = BuffaloInequality(Poly(coeff))
            sub_ineq.is_substitution_necessary = False
            sub_ineq.poly_variables = self.poly_variables_after_substitution
            sub_proof, sub_result = sub_ineq.solve()
            sub_proofs.append(sub_proof)
            if not sub_result:
                all_positive = False
                break
        if all_positive:
            # TODO add sub_proofs into proof
            proof.append('Proved because all terms are positive!')
            #proof.append(sub_proofs)
            return proof, True

        # variable >= 4 not supported yet
        if len(self.poly_variables) > 3:
            proof.append('The solver could not solve the inequality.')
            return proof, False

        t_poly = Poly(0, X)
        for deg, coeff in deg_map.items():
            best_number = binary_search_best_number(coeff.subs(
                {
                    self.poly_variables_after_substitution[0]: X,
                    self.poly_variables_after_substitution[1]: 1
                }
            ), max_deg - deg)
            t_poly += X ** deg * best_number
        proof.append(f'The polynomoial is larger than {t_poly.as_expr()}')
        if is_positive_poly(t_poly):
            proof.append(f'{t_poly.as_expr()} is positive for X > {0}')
            return proof, True
        else:
            proof.append(f'{t_poly.as_expr()} is not always positive for X > {0}')
            return proof, False


def cyclic_sum_xyz(f):
    return f + f.subs({x: y, y: z, z: x}, simultaneous=True) + f.subs({x: z, z: y, y: x}, simultaneous=True)


def cyclic_prod_xyz(f):
    return f * f.subs({x: y, y: z, z: x}, simultaneous=True) * f.subs({x: z, z: y, y: x}, simultaneous=True)


if __name__ == '__main__':
    p = cyclic_prod_xyz(x + y)
    rhs = cyclic_sum_xyz(5 * x ** 4 * y ** 2 + x ** 4 * z ** 2 + 6 * x ** 3 * y ** 3 + 2 * x ** 4 * y * z + 4 * x ** 3 * y ** 2 * z + 2 * x ** 3 * y * z ** 2 - 4 * x ** 2 * y ** 2 * z ** 2)
    rhs = rhs * rhs * p
    lhs = 256 * cyclic_sum_xyz(x ** 3 * y ** 3 * (x + z))
    lhs *= cyclic_sum_xyz(x ** 3 * y ** 3 * (x + z) * (y + z))
    b = BuffaloInequality(Poly(rhs - lhs))
    b.minimum = 0
    b.poly_variables = [x, y, z]
    b.base_variable = x
    b.poly_variables_after_substitution = [u, v]
    pf, result = b.solve()
    for line in pf:
        print(line)
    print(result)
    '''
        P = 0
        Q = 1
        POW_1 = 5
        POW_2 = 3
        A = P * x ** POW_1 + Q * y ** POW_1
        B = P * y ** POW_1 + Q * z ** POW_1
        C = P * z ** POW_1 + Q * x ** POW_1
        king_poly = (P + Q) * x ** (POW_1 + POW_2) * B * C + (P + Q) * y ** (POW_1 + POW_2) * A * C +\
                    (P + Q) * z ** (POW_1 + POW_2) * A * B - (x ** POW_2 + y ** POW_2 + z ** POW_2) * A * B * C
    
        b = BuffaloInequality(Poly(king_poly))
        b.minimum = 0
        b.poly_variables = [x, y, z]
        b.base_variable = x
        b.poly_variables_after_substitution = [u, v]
        pf, result = b.solve()
        for line in pf:
            print(line)
        print(result)
    
        b = BuffaloInequality(Poly(king_poly))
        b.minimum = 0.4651
        b.poly_variables = [x, y, z]
        b.base_variable = x
        b.poly_variables_after_substitution = [u, v]
        pf, result = b.solve()
        for line in pf:
            print(line)
        print(result)
    
        print()
        print()
    
        b = BuffaloInequality(Poly(king_poly))
        b.poly_variables = [x, y, z]
        b.minimum = 2.15
        b.poly_variables_after_substitution = [v, u]
        pf, result = b.solve()
        for line in pf:
            print(line)
        print(result)
    '''