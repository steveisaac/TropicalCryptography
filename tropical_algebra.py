# Tropical Matrix Addition
def add(x, y):
    return [[a if a < b else b for a, b in zip(x_rows, y_rows)] for x_rows, y_rows in zip(x, y)]


# Tropical Matrix Multiplication
def multiply(x, y):
    return [[min(a + b for a, b in zip(row, col)) for col in zip(*y)] for row in x]


# Tropical Adjoint Multiplication
def adj_multiply(x, y):
    return add(add(x, y), multiply(x, y))


# First semigroup operation from: Tropical cryptography II: Extensions by homomorphisms
def semigroup_op_1(x, g, y, h):
    return add(adj_multiply(x, h), y), adj_multiply(g, h)


# Second semigroup operation from: Tropical cryptography II: Extensions by homomorphisms
def semigroup_op_2(m, g, s, h):
    # list(zip(*m)) returns the transpose of m
    return add(add(multiply(h, list(zip(*m))), multiply(list(zip(*m)), h)), s), multiply(g, h)
