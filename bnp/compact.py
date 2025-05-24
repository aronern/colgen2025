from typing import List
from pyscipopt import Model, quicksum


def binpacking_compact(sizes: List[int], capacity: int) -> Model:
    model = Model("Binpacking")

    # TODO: Implement the compact bin packing formulation
    B = len(sizes)
    # Variables
    varsX = {}
    varsY = {}
    for i in range(len(sizes)):
        for b in range(B):
            varsX[i, b] = model.addVar(vtype='B', name=f"x_{i}_{b}", obj=0)

    for b in range(B):
        varsY[b] = model.addVar(vtype='B', name=f"y_{b}", obj=1)

    # Constraints
    coverConstr = {}
    for i in range(len(sizes)):
        coverConstr[i] = model.addCons(
            quicksum(varsX[i, b] for b in range(B)) == 1, name=f"cover_{i}")

    binConstr = {}
    for b in range(B):
        binConstr[b] = model.addCons(quicksum(
            varsX[i, b]*sizes[i] for i in range(len(sizes))) <= capacity*varsY[b], name=f"bin_{b}")
    return model
