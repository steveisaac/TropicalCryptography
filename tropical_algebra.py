from numpy import minimum, array, dtype


def add(x, y):  # Tropical Addition: Elementwise minimum.
    return minimum(x, y)


def multiply(x, y):  # Tropical Multiplication
    return array([[min(i + j) for j in y.T] for i in x], dtype=int)


def adj_multiply(x, y):  # Tropical Adjoint multiplication
    return add(add(x, y), multiply(x, y))


def semigroup_op_1(x, g, y, h):
    """
    First semigroup operation from: Tropical cryptography II: Extensions by homomorphisms
    """
    return add(adj_multiply(x, h), y), adj_multiply(g, h)


def semigroup_op_2(m, g, s, h):
    """
    Second semigroup operation from: Tropical cryptography II: Extensions by homomorphisms
    """
    return add(add(multiply(h, m.T), multiply(m.T, h)), s), multiply(g, h)

