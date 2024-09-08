#!/usr/bin/env python3    

"""
A Python script to convert symmetric TSP problems into an Ising Hamiltonian.

Input
---------------
- coef_matrix: Symmetric matrix of coefficients representing distances between cities.

Output
---------------
- Ising Hamiltonian and offset for the given TSP problem.
"""

import argparse
import numpy as np
import itertools
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.translators import to_ising
from qiskit_optimization.converters import QuadraticProgramToQubo

class QUBO_to_Ising:

    def __init__(self, coef_matrix: np.ndarray) -> None:
        self.coef = coef_matrix
        self.n = len(coef_matrix)
        self.qp = QuadraticProgram()

        if self.n in [4, 6, 8]:
            self.setup()
        else:
            raise ValueError("This script only handles simetric TSP with 4, 6, or 8 cities.")

    def setup(self):
        if self.n == 4:
            self.simetric_four_edges()
        elif self.n == 6:
            self.simetric_six_edges()
        elif self.n == 8:
            self.simetric_eight_edges()

    def simetric_four_edges(self):
        # Create binary variables for 4-city TSP problem
        self.create_variables(6)  # 4 cities, 6 possible connections
        self.add_constraints(4)
        self.create_objective_function()

    def simetric_six_edges(self):
        # Create binary variables for 6-city TSP problem
        self.create_variables(15)  # 6 cities, 15 possible connections
        self.add_constraints(6)
        self.create_objective_function()

    def simetric_eight_edges(self):
        # Create binary variables for 8-city TSP problem
        self.create_variables(28)  # 8 cities, 28 possible connections
        self.add_constraints(8)
        self.create_objective_function()

    def create_variables(self, num_vars):
        for i in range(num_vars):
            self.qp.binary_var(f'x{i+1}')

    def add_constraints(self, cities):
        # Add the necessary constraints for each city
        for i in range(cities):
            self.qp.linear_constraint(linear={f'x{i+1}': 1}, sense='==', rhs=1)

    def create_objective_function(self):
        # Create the objective function from the coefficient matrix
        num_vars = len(self.coef)
        objective = {f'x{i+1}': self.coef[i // self.num_cities, i % self.num_cities] for i in range(num_vars)}
        self.qp.minimize(linear=objective)

    def converter(self):
        # Convert the QuadraticProgram with constraints to a QUBO problem
        qubo_problem = QuadraticProgramToQubo().convert(self.qp)

        # Convert the QUBO problem to an Ising model
        ising_h, offset = to_ising(qubo_problem)

        print("Ising Hamiltonian:", ising_h)
        print("Offset:", offset)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A Python script to convert symmetric TSP problems into an Ising Hamiltonian.')
    parser.add_argument('coef_matrix', type=str, help='Symmetric coefficient matrix representing distances between cities.')

    args = parser.parse_args()

    # Assume input is a stringified numpy array; we parse it into an actual numpy array.
    coef_matrix = np.array(eval(args.coef_matrix))

    # Create the QUBO_to_Ising instance
    tsp_instance = QUBO_to_Ising(coef_matrix)
    tsp_instance.converter()
 


