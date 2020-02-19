def add(x, y):  # Tropical Addition: Elementwise minimum.
    # total = []
    # for i in range(ORDER):
    #     total.append([])
    #     for j in range(ORDER):
    #         if x[i][j] < y[i][j]:
    #             total[i].append(x[i][j])
    #         else:
    #             total[i].append(y[i][j])
    # return total
    return [[a if a < b else b for a, b in zip(x_rows, y_rows)] for x_rows, y_rows in zip(x, y)]


def multiply(x, y):  # Tropical Multiplication
    # result = []
    # for i in range(ORDER):
    #     result.append([])
    #     for j in range(ORDER):
    #         val = 1000
    #         for k in range(ORDER):
    #             if x[i][k] + y[k][j] < val:
    #                 val = x[i][k] + y[k][j]
    #         result[i].append(val)
    # return result
    return [[min(a + b for a, b in zip(row, col)) for col in zip(*y)] for row in x]


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
    # list(zip(*m)) returns the transpose of m
    return add(add(multiply(h, list(zip(*m))), multiply(list(zip(*m)), h)), s), multiply(g, h)
