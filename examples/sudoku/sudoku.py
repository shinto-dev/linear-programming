from pyomo.core import ConcreteModel, Constraint, Objective, RangeSet, Var
from pyomo.repn.plugins.baron_writer import Binary

from pyomo_solver import solver_factory
from pyomo_solver.solver_factory import Solver


def solve_sudoku(board):
    model = ConcreteModel()

    model.X = RangeSet(9)
    model.Y = RangeSet(9)
    model.DIGIT = RangeSet(9)

    model.value = Var(model.X, model.Y, model.DIGIT, within=Binary)
    for (x, y, v) in board:
        model.value[x, y, v].fix(1)

    model.obj = Objective(expr=1)

    model.digit_constraint = Constraint(
        model.X, model.Y, rule=lambda m, x, y: sum(m.value[x, y, d] for d in model.DIGIT) == 1
    )
    model.row_level_constraint = Constraint(
        model.X, model.DIGIT, rule=lambda m, x, d: sum(m.value[x, y, d] for y in model.Y) == 1
    )
    model.column_level_constraint = Constraint(
        model.Y, model.DIGIT, rule=lambda m, y, d: sum(m.value[x, y, d] for x in model.X) == 1
    )
    model.subsquare_level_constraint = Constraint(
        range(1, 9, 3), range(1, 9, 3), model.DIGIT,
        rule=lambda m, i, j, d: sum(m.value[x, y, d] for x in range(i, i + 3) for y in range(j, j + 3)) == 1)

    solver = solver_factory.get_solver(Solver.BONMIN)
    solver.solve(model)

    for v in model.component_data_objects(Var):
        print(str(v), v.value)

    for i in model.X:
        row = ''
        for j in model.Y:
            row += '{} '.format(get_value(model, i, j))
        print(row)


def get_value(model, x, y):
    return sum(i * int(model.value[x, y, i].value) for i in model.DIGIT)


if __name__ == '__main__':
    board = [(1, 1, 9), (2, 2, 8)]
    solve_sudoku(board)

# Reference: https://github.com/Pyomo/pyomo/blob/master/examples/doc/pyomobook/scripts-ch/sudoku/sudoku.py
