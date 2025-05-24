def print_version():
    from pyscipopt import Model

    # Create a new model
    model = Model()
    model.redirectOutput()

    # TODO: Print the version of SCIP, which SCIP version is used?
    
    print("SCIP version:", model.version())

if __name__ == "__main__":
    print_version()