
from pysat.solvers import Glucose3
from pysat.formula import CNF
import sys

def print_sudoku(solution, order):
    dimension = order * order

    print(order)

    for row in range(dimension):
        if row == 0:
            print("-------------------------")
        for col in range(dimension):
            if col == 0:
                print("| ", end=' ')
            for num in range(1, dimension + 1):
                encoded = encode(num, col, row, order)
                value = solution[encoded-1]

                if value> 0:
                    print(num, end=' ')

            if (col + 1) % order == 0 or col == dimension - 1:
                print("|", end=' ')

            if col < dimension - 1:
                print(" ", end=' ')
        print()

        if (row + 1) % order == 0 or row == dimension - 1:
            print("-------------------------")

def solve_dimacs_to_formula(constraints, order, file_name):

    formula = CNF(file_name)

    with Glucose3(bootstrap_with=formula.clauses) as solver:
        if solver.solve():
            # Print the solution
            solution = solver.get_model()
            print_sudoku(solution, order)
        else:
            print("No solution found.")



def write_dimacs_to_file(formula, order, output_filename):
    with open(output_filename, 'w') as file:
        file.write("c\n")
        file.write("c DIMACS file to solve a Sudoku game with SAT\n")
        file.write("c\n")
        num_variables = order * order * order * order * order * order
        file.write("p cnf {} {}\n".format(num_variables, len(formula)))

        for clause in formula:
            for literal in clause:
                var = literal[0]

                if not literal[1]:
                    var *= -1

                file.write("{} ".format(var))

            file.write("0\n")

def of_fields(order):
    indices = []
    dimension = order * order

    for i in range(dimension):
        for j in range(dimension):
            field_indices = []
            for n in range(1, dimension + 1):
                field_indices.append(encode(n, i, j, order))
            indices.append(field_indices)

    return indices

def of_columns(order):
    indices = []
    dimension = order * order

    for n in range(1, dimension + 1):
        for i in range(dimension):
            column_indices = []
            for j in range(dimension):
                column_indices.append(encode(n, i, j, order))
            indices.append(column_indices)

    return indices

def of_rows(order):
    indices = []
    dimension = order * order

    for n in range(1, dimension + 1):
        for j in range(dimension):
            row_indices = []
            for i in range(dimension):
                row_indices.append(encode(n, i, j, order))
            indices.append(row_indices)

    return indices

def of_blocks(order):
    indices = []
    dimension = order * order

    for n in range(1, dimension + 1):
        for a in range(order):
            for b in range(order):
                block_indices = []
                for col_i in range(order):
                    for row_j in range(order):
                        col_offset = a * order
                        row_offset = b * order
                        block_indices.append(encode(n, col_i + col_offset, row_j + row_offset, order))
                indices.append(block_indices)

    return indices

def exactly_one_of(indices):
    constraints = []

    while indices:
        elems = list(indices[-1])
        at_least_one = []

        for i in range(len(elems)):
            at_least_one.append((elems[i], True))
            for j in range(i + 1, len(elems)):
                constraints.append([(elems[i], False), (elems[j], False)])

        constraints.append(at_least_one)
        indices.pop()

    return constraints

def at_least_one_of(indices):
    constraints = []

    while indices:
        elems = list(indices[-1])
        at_least_one = []

        while elems:
            at_least_one.append((elems[-1], True))
            elems.pop()

        constraints.append(at_least_one)
        indices.pop()

    return constraints

def at_most_one_of(indices):
    constraints = []

    while indices:
        elems = list(indices[-1])

        for i in range(len(elems)):
            for j in range(i + 1, len(elems)):
                constraints.append([(elems[i], False), (elems[j], False)])

        indices.pop()

    return constraints

def encode(num, col, row, order):
    dimension = order * order
    return (col + row * dimension) * dimension + num

def generate_dimacs(file_name):
    with open(file_name, 'r') as file:
        lines = file.read().splitlines()

    if len(lines) < 2:
        print("error reading from file: expected at least 2 lines, got", len(lines))
        return 1

    order = int(lines[0])
    dimension = order * order
    lines.pop(0)

    if order < 1:
        print("error reading from file: expected sudoku order in the first line to be a positive integer, got", order)
        return 1

    if len(lines) != dimension:
        print("error reading from file: after order number line (", order, "), there are order * order (", dimension, ") lines expected, got", len(lines))
        return 1

    line_ctr = 0

    for line in lines:
        columns = line.split()

        if len(columns) != dimension:
            print("error reading from file: error in line", line_ctr + 2, ": expected", dimension, "columns separated by whitespace, got", len(columns))
            return 1

        col_ctr = 0

        for col in columns:
            elem = int(col)

            if elem < 0 or elem > dimension:
                print("error reading from file: error in line", line_ctr + 2, ", column", col_ctr, ": expected integer between 0 and", dimension, ", got", elem)
                return 1

            if elem == 0:
                col_ctr += 1
                continue

            # set the all (column, row) variables for that number to False,
            # except for the number that was read from input (is True by definition)
            for n in range(1, dimension + 1):
                input_formula.append(((encode(n, col_ctr, line_ctr, order), elem == n)))

            col_ctr += 1

        line_ctr += 1

    formula = CNF()

    constraints = exactly_one_of(of_fields(order)) + exactly_one_of(of_columns(order)) + exactly_one_of(of_rows(order)) + exactly_one_of(of_blocks(order))

    write_dimacs_to_file(constraints, order, "test.txt")

    solve_dimacs_to_formula(constraints, order, "test.txt")

        
input_formula = []
order = 0

if __name__ == "__main__":
    generate_dimacs(sys.argv[1])