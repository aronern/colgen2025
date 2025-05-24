from typing import List

from pyscipopt import Model, quicksum


def pricing_solver(sizes: List[int], capacity: int, dual_solution: dict[float], together: set[tuple[int, int]],
                   apart: set[tuple[int, int]]) -> tuple[float, List[int]]:
    """
    Solve the pricing problem for the knapsack problem (with branching constraints)

    Parameters:
    sizes: List[int] - the sizes of the items
    capacity: int - the capacity of the knapsack
    dual_solution: dict[float] - the dual solution of the linear relaxation
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the minimum reduced cost and the packing of the items
    """

    profits = [dual_solution[i] for i in range(len(sizes))]
    if len(together) > 0 or len(apart) > 0:
        result = solve_knapsack_with_constraints(
            sizes, profits, capacity, together, apart)
    else:
        result = solve_knapsack(sizes, profits, capacity)

    min_red_cost = 1 - result[0]

    return min_red_cost, result[1]


def solve_knapsack(sizes: List[int], values: List[float], capacity: int) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """
    model = Model()

    varsA = {}
    for i in range(len(values)):
        # Create a variable for each item
        varsA[i] = model.addVar(vtype="B", name=f"a_{i}")

    model.addCons(quicksum(
        sizes[i]*varsA[i] for i in range(len(sizes))) <= capacity, name="capacity")

    model.setObjective(quicksum(values[i]*varsA[i]
                       for i in range(len(values))), sense="maximize")

    model.optimize()
    returnList = []
    for i in range(len(values)):
        if model.getVal(varsA[i]) > 0.5:
            returnList.append(i)
    return (model.getObjVal(), returnList)


def solve_knapsack_with_constraints(
        sizes: List[int], values: List[float], capacity: int, together: set[tuple[int, int]],
        apart: set[tuple[int, int]]
) -> tuple[float, List[int]]:
    """
    Solve the knapsack problem with branching constraints

    Parameters:
    sizes: List[int] - the sizes of the items
    values: List[float] - the values of the items
    capacity: int - the capacity of the knapsack
    together: set[tuple[int]] - the pairs of items that must be together
    apart: set[tuple[int]] - the pairs of items that must be apart

    Returns:
    tuple[float, List[int]] - the optimal value and the packing of the items
    """
    model = Model()

    varsA = {}
    for i in range(len(values)):
        # Create a variable for each item
        varsA[i] = model.addVar(vtype="B", name=f"a_{i}")

    model.addCons(quicksum(
        sizes[i]*varsA[i] for i in range(len(sizes))) <= capacity, name="capacity")

    for i, j in together:
        model.addCons(varsA[i] == varsA[j], name=f"together_{i}_{j}")

    for i, j in apart:
        model.addCons(varsA[i] + varsA[j] <= 1, name=f"apart_{i}_{j}")

    model.setObjective(quicksum(values[i]*varsA[i]
                       for i in range(len(values))), sense="maximize")

    model.optimize()
    returnList = []
    for i in range(len(values)):
        if model.getVal(varsA[i]) > 0.5:
            returnList.append(i)
    return (model.getObjVal(), returnList)
