#
#   -   Q   -   -
#   -   -   -   Q
#   Q   -   -   -
#   -   -   Q   -
#
# Refer : http://thejavamathematician.blogspot.com/2015/02/the-n-queens-puzzle-and-0-1-integer.html

from pyomo.core import ConcreteModel, Constraint, Objective, RangeSet, Var, maximize
from pyomo.repn.plugins.baron_writer import Binary

from pyomo_solver import solver_factory
from pyomo_solver.solver_factory import Solver


def n_queens(board_size=4):
    model = ConcreteModel()
    model.ROWS = RangeSet(board_size)
    model.COLS = RangeSet(board_size)

    model.x = Var(model.ROWS, model.COLS, within=Binary)

    model.obj = Objective(expr=sum(model.x[i, j] for i in model.ROWS for j in model.COLS), sense=maximize)

    model.constraint_row_level = Constraint(model.ROWS, rule=lambda m, i: sum(m.x[i, j] for j in m.COLS) <= 1)
    model.constraint_column_level = Constraint(model.COLS, rule=lambda m, j: sum(m.x[i, j] for i in m.ROWS) <= 1)

    # remove cases like (4,4)
    model.constraint_diagonal_first_column = Constraint(
        model.ROWS, rule=lambda m, i: sum(m.x[i + j, 1 + j] for j in range(board_size - i + 1)) <= 1
    )
    model.constraint_diagonal_first_row = Constraint(
        model.COLS, rule=lambda m, j: sum(m.x[i + 1, j + i] for i in range(board_size - j + 1)) <= 1
    )

    model.constraint_back_diagonal = Constraint(
        model.COLS, rule=lambda m, j: sum(m.x[1 + i, j - i] for i in range(j)) <= 1)

    model.constraint_back_diagonal_last_row = Constraint(
        model.ROWS, rule=lambda m, i: sum(m.x[i + j, board_size - j] for j in range(board_size - i + 1)) <= 1)

    solver = solver_factory.get_solver(Solver.BONMIN)
    solver.solve(model)

    return [(i, j)
            for i in range(1, board_size + 1)
            for j in range(1, board_size + 1) if model.x[i, j] == 1]


def _display_solution(board_size, solution):
    solution_as_set = set(solution)
    for i in range(1, board_size + 1):
        res = ""
        for j in range(1, board_size + 1):
            res += "Q " if (i, j) in solution_as_set else "- "
        print(res)


if __name__ == '__main__':
    _display_solution(8, n_queens(8))
