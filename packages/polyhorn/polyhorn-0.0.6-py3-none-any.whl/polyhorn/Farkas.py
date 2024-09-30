from typing import List, Tuple

from .Constraint import CoefficientConstraint, PolynomialConstraint
from .Polynomial import Polynomial
from .Solver import Solver
from .UnknownVariable import UnknownVariable


class Farkas:
    """
    A class that performs the constraint transformation according to Farkas
    Lemma.

    Parameters
    ----------
    variables : List[UnknownVariable]
        The list of variables of the polynomials.
    LHS : List[PolynomialConstraint]
        The list of left hand side constraints in farkas algorithm
    RHS : PolynomialConstraint
        The right hand side constraint in algorithm

    Attributes
    ----------
    variables : List[UnknownVariable]
        The list of variables of the polynomials.
    LHS : List[PolynomialConstraint]
        The list of left hand side constraints in farkas algorithm
    RHS : PolynomialConstraint
        The right hand side constraint in algorithm
    """

    def __init__(self, variables: List[UnknownVariable], LHS: List[PolynomialConstraint], RHS: PolynomialConstraint):
        self.variables = variables
        self.RHS = RHS
        self.LHS = LHS

    def get_poly_sum(self, need_strict: bool = False) -> Tuple[Polynomial, CoefficientConstraint]:
        """ 
        This function returns a polynomial y_0 + y_1*f_1 + y_2*f_2 ...+ y_n*f_n
        where f_i are left hand side polynomials and y_i are newly created 
        variable in farkas theorem.

        Parameters
        ----------
        need_strict : bool, optional
            Is it generated for the 0 > 0 case or not, by default False

        Returns
        -------
        Tuple[Polynomial, CoefficientConstraint]
            polynomial of sum of all left hand side with new variables and corresponding constraints.
        """
        new_var = Solver.get_variable_polynomial(
            self.variables, 'y0', 'generated_for_Farkas')
        polynomial_of_sum = new_var

        sum_of_strict = Solver.get_constant_polynomial(
            self.variables, '0') + new_var

        constraints = [CoefficientConstraint(
            new_var.monomials[0].coefficient, '>=')]

        for i, left_constraint in enumerate(self.LHS):
            left_poly = left_constraint.polynomial
            new_var_poly = Solver.get_variable_polynomial(self.variables, f'y{i + 1}',
                                                          'generated_for_Farkas')
            if left_constraint.is_strict():
                sum_of_strict = sum_of_strict + new_var_poly

            polynomial_of_sum = polynomial_of_sum + (new_var_poly * left_poly)
            constraints.append(CoefficientConstraint(
                new_var_poly.monomials[0].coefficient, '>='))

        if need_strict or self.RHS.is_strict():
            constraints.append(CoefficientConstraint(
                sum_of_strict.monomials[0].coefficient, '>'))
        return polynomial_of_sum, constraints

    def get_SAT_constraint(self) -> List[CoefficientConstraint]:
        """ 
        A function to find the constraints when the LHS => RHS is satisfiable.

        Returns
        -------
        List[CoefficientConstraint]
            list of coefficient constraints when it is satisfiable
        """
        polynomial_of_sum, constraints = self.get_poly_sum()
        return Solver.find_equality_constraint(polynomial_of_sum, self.RHS.polynomial) + constraints

    def get_UNSAT_constraint(self, need_strict: bool = False) -> List[CoefficientConstraint]:
        """ 
        A function to find the constraints when it is not satisfiable.

        Two set of constraint can be generated:
            1. `LHS => -1 >= 0`
            2. `LHS => 0 > 0`

        Parameters
        ----------
        need_strict : bool, optional
            determine which set of constraint to generate, by default False

        Returns
        -------
        List[CoefficientConstraint]
            list of coefficient constraints when it is not satisfiable
        """
        if need_strict:
            polynomial_of_sum, constraints = self.get_poly_sum(need_strict)
            return Solver.find_equality_constraint(polynomial_of_sum,
                                                   Polynomial(polynomial_of_sum.variables, [])) + constraints
        polynomial_of_sum, constraints = self.get_poly_sum()
        return Solver.find_equality_constraint(polynomial_of_sum,
                                               Solver.get_constant_polynomial(self.RHS.polynomial.variables, '-1')) + constraints
