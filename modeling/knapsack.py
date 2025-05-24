from pyscipopt import quicksum


def linear_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    varsA = {}
    for i in range(len(weights)):
        # Create a variable for each item
        varsA[i] = model.addVar(vtype="C", name=f"a_{i}")

    model.addCons(quicksum(
        weights[i]*varsA[i] for i in range(len(weights))) <= capacity, name="capacity")

    model.setObjective(quicksum(values[i]*varsA[i]
                       for i in range(len(values))), sense="maximize")
    return model


def binary_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a 0-1 knapsack, as described in exercise 2
    varsA = {}
    for i in range(len(weights)):
        # Create a variable for each item
        varsA[i] = model.addVar(vtype="B", name=f"a_{i}")

    model.addCons(quicksum(
        weights[i]*varsA[i] for i in range(len(weights))) <= capacity, name="capacity")

    model.setObjective(quicksum(values[i]*varsA[i]
                       for i in range(len(values))), sense="maximize")
    return model


def integer_knapsack(capacity, weights, values):
    from pyscipopt import Model
    model = Model()

    # TODO Implement an integer knapsack, as described in exercise 3
    varsA = {}
    for i in range(len(weights)):
        # Create a variable for each item
        varsA[i] = model.addVar(vtype="I", name=f"a_{i}")

    model.addCons(quicksum(
        weights[i]*varsA[i] for i in range(len(weights))) <= capacity, name="capacity")

    model.setObjective(quicksum(values[i]*varsA[i]
                       for i in range(len(values))), sense="maximize")

    return model


def limited_knapsack(capacity, weights, values, max_items):
    from pyscipopt import Model
    model = Model()

    # TODO Implement a knapsack limited to 4 items, as described in exercise 4

    return model
