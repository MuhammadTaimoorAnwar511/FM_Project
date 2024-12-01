from pysat.formula import CNF
from pysat.solvers import Solver


def logic_to_cnf(expression):
    """
    Converts a single propositional logic expression into CNF format.
    This is a placeholder; you'll need to implement or use a library for this.
    """
    # Example: Convert simple logic to CNF manually (expand for complex cases)
    if expression == "(A -> B)":
        return [[-1, 2]]  # A -> B is equivalent to (~A OR B)
    elif expression == "(A | B)":
        return [[1, 2]]  # A OR B
    elif expression == "(~A | B)":
        return [[-1, 2]]  # NOT A OR B
    else:
        raise NotImplementedError(f"Conversion for {expression} not implemented")


def compute_mwps(logic_expressions):
    cnf = CNF()

    # Convert logic expressions to CNF and add to the CNF object
    for expr in logic_expressions:
        try:
            cnf_clauses = logic_to_cnf(expr)
            for clause in cnf_clauses:
                cnf.append(clause)
        except NotImplementedError as e:
            print(f"Skipping expression: {expr}. Reason: {e}")

    print("\nConverted Logic Expressions to CNF:")
    print(cnf.clauses)

    # Use a SAT solver to find minimal working products (MWPs)
    with Solver(bootstrap_with=cnf) as solver:
        mwps = []
        while solver.solve():
            model = solver.get_model()
            mwps.append(model)
            print(f"MWP Found: {model}")
            # Add a blocking clause to prevent finding the same solution again
            solver.add_clause([-lit for lit in model])

    print("\nAll MWPs Computed:")
    print(mwps)
    return mwps
