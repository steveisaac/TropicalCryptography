def add(x, y):  # Tropical Addition: Elementwise minimum.
    sum = []
    for i in range(30):
        sum.append([])
        for j in range(30):
            if x[i][j] < y[i][j]:
                sum[i].append(x[i][j])
            else:
                sum[i].append(y[i][j])
    return sum
    # return [[a if a < b else b for a, b in zip(i, j)] for i, j in zip(x, y)]


def multiply(x, y):  # Tropical Multiplication
    result = []
    for i in range(30):
        result.append([])
        for j in range(30):
            val = 1001
            for k in range(30):
                if x[i][k] + y[k][j] < val:
                    val = x[i][k] + y[k][j]
            result[i].append(val)
    return result


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

