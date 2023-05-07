from sympy import Poly, Interval
from check import BaseCheckStrategy
from substitution import BaseSubstitutionStrategy
from proof import BaseProofStrategy
from typing import Tuple, List
from poly_util import print_latex


class BuffaloPolynomial:
    polynomial: Poly
    check: BaseCheckStrategy
    substitution: BaseSubstitutionStrategy
    proof_strategy: BaseProofStrategy
    range: Interval

    def __init__(self):
        pass

    def proof(self) -> Tuple[bool, List[str]]:
        is_true: bool = False
        proof: List[str] = list()
        proof.append(f'We want to prove $${print_latex(self.polynomial)}$$ is positive.')
        proof.append('The Buffalo Way method helps.')

        if not self.polynomial.is_homogeneous:
            proof.append('This polynomial is not homogeneous.')

        elif not self.check.check(self.polynomial, proof):
            proof.append('Thus we cannot check this polynomial is positive.')

        else:
            substitution_map, base_symbol, substitution_str = self.substitution.get_map(self.polynomial)

            substituted_polynomial = self.polynomial.subs(substitution_map, simultaneous=True)
            substituted_polynomial = Poly(substituted_polynomial.as_expr())
            if substitution_str:
                proof.append(substitution_str)
            latex_polynomial = Poly(substituted_polynomial, base_symbol)
            proof.append(f'Substitution gives $${print_latex(latex_polynomial)}$$')

            result = self.proof_strategy.prove(substituted_polynomial, base_symbol, proof, self.range)
            if result:
                is_true = True

        return is_true, proof
