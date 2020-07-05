import os

import pyomo.environ as pyomo_env
from enum import Enum


class Solver(Enum):
    CBC = 1
    BONMIN = 2


def get_solver(solver: Solver):
    print(os.path.dirname(os.path.abspath(__file__)))
    return pyomo_env.SolverFactory(f"{os.path.dirname(os.path.abspath(__file__))}/solvers/bonmin")
