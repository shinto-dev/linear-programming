# Problem
# V = [1,   1,  1,  10, 10, 13,  3]
# W = [2,   2,  2,  5,  5,  8,   3]
from typing import List, Union

from pyomo.core import ConcreteModel, Constraint, Objective, Var, maximize
from pyomo.repn.plugins.baron_writer import Binary

from pyomo_solver import solver_factory
from pyomo_solver.solver_factory import Solver


def knapsack(weights: List[Union[int, float]], values: List[Union[int, float]], max_weight: Union[int, float]):
    I = list(range(len(weights)))

    model = ConcreteModel()
    model.x = Var(I, within=Binary)

    model.objective = Objective(expr=sum(model.x[i] * values[i] for i in I), sense=maximize)
    model.constraint = Constraint(expr=sum(model.x[i] * weights[i] for i in I) <= max_weight)

    solver = solver_factory.get_solver(Solver.BONMIN)
    solver.solve(model)

    for v in model.component_data_objects(Var):
        print(str(v), v.value)


if __name__ == '__main__':
    V = [1, 1, 1, 10, 10, 13, 3]
    W = [2, 2, 2, 5, 5, 8, 3]

    knapsack(W, V, 10)
