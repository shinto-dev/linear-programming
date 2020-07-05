from pyomo.core import ConcreteModel, Constraint, Objective, Var, maximize

# Problem
# V = [1,   1,  1,  10, 10, 13,  3]
# W = [2,   2,  2,  5,  5,  8,   3]
from pyomo.repn.plugins.baron_writer import Binary

from pyomo_solver.solver_factory import Solver, get_solver

model = ConcreteModel()
model.x_1 = Var(within=Binary)
model.x_2 = Var(within=Binary)
model.x_3 = Var(within=Binary)
model.x_4 = Var(within=Binary)
model.x_5 = Var(within=Binary)
model.x_6 = Var(within=Binary)
model.x_7 = Var(within=Binary)

model.obj = Objective(
    expr=model.x_1 + model.x_2 + model.x_3 + 10 * model.x_4 + 10 * model.x_5 + 13 * model.x_6 + 3 * model.x_7,
    sense=maximize
)

model.con_0 = Constraint(
    expr=2 * model.x_1 + 2 * model.x_2 + 2 * model.x_3 + 5 * model.x_4 +
         5 * model.x_5 + 8 * model.x_6 + 3 * model.x_7 <= 10
)

solver = get_solver(Solver.BONMIN)
results = solver.solve(model)

for v in model.component_data_objects(Var):
    print(str(v), v.value)
