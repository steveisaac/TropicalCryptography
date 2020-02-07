import numpy


def add(x, y):  # Tropical Addition: Elementwise minimum.
    return numpy.minimum(x, y)


def multiply(x, y):  # Tropical Multiplication
    return numpy.array([[min(i + j) for j in y.T] for i in x])


def adj_multiply(x, y):  # Tropical Adjoint multiplication
    return add(add(x, y), multiply(x, y))


def semidirect_product(x, g, y, h):  # Tropical Semidirect Product
    return add(adj_multiply(x, y), y), adj_multiply(g, h)
