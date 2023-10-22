from pysat.solvers import Glucose3
from pysat.formula import CNF

def pythagorean_triples(n):
    # Create a SAT formula for the Pythagorean triples problem
    formula = CNF()

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            for k in range(j + 1, n + 1):
                if i * i + j * j == k * k:
                    # Encode the constraint using Boolean variables
                    formula.append([-i, -j, k])
                    formula.append([-i, j, -k])
                    formula.append([i, -j, -k])
                    formula.append([i, j, k])

    # Solve the SAT formula
    with Glucose3(bootstrap_with=formula.clauses) as solver:
        if solver.solve():
            # Print the solution
            solution = solver.get_model()
            print("Solution found:")
            for i in range(1, n + 1):
                if solution[i - 1] > 0:
                    print(f"{i}: red")
                else:
                    print(f"{i}: blue")
        else:
            print("No solution found.")

# Example usage
pythagorean_triples(1000)
