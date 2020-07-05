import pyomo.environ as pyomo_env
from enum import Enum


class Solver(Enum):
    CBC = 1
    BONMIN = 2


def get_solver(solver: Solver):
    return pyomo_env.SolverFactory('./bonmin')
