from random import randrange

from tropical_algebra import *


def generate_m_h():
    """
    Returns two 30 x 30 matrices filled with random integers from -1000 to 1000 inclusive.
    These are the public matrices M and H.
    """
    # return (array([[-1 for i in range(30)] for j in range(30)]) for k in range(2))
    return (
        array([[randrange(-1000, 1001) for i in range(30)] for j in range(30)], dtype=int) for k in range(2))


def generate_exponent():
    """
    Returns the random exponent m on the order of 2^200.
    """
    return 5
    # return randrange(2**200, 2**201)


"""
//Use with small exponents to check algorithms
def check_intermediaries(matrix_m, matrix_h, exponent_m):
    matrix_a, h_to_power_m = (matrix_m, matrix_h)
    for i in range(exponent_m-1):
        matrix_a, h_to_power_m = semigroup_op_1(matrix_a, h_to_power_m, matrix_m, matrix_h)
    return matrix_a, h_to_power_m
"""


def compute_intermediaries(matrix_m, matrix_h, exponent_m, mode=1):
    if mode == 1:
        semigroup_op = semigroup_op_1
    elif mode == 2:
        semigroup_op = semigroup_op_2
    sq_and_mul = [(matrix_m, matrix_h)]
    for i in range(len(bin(exponent_m)[2:])-1):
        sq_and_mul.append(semigroup_op(*sq_and_mul[i], *sq_and_mul[i]))
    first_one = True
    intermediaries = None
    for i in range(len(bin(exponent_m)[2:])):
        if bin(exponent_m)[:1:-1][i] == "1" and first_one:
            intermediaries = sq_and_mul[i]
            first_one = False
            print(i)
        elif bin(exponent_m)[:1:-1][i] == "1":
            intermediaries = semigroup_op(*intermediaries, *sq_and_mul[i])
    return intermediaries


def compute_secret_key(received_matrix, sent_matrix, h_exp, mode=1):
    if mode == 1:
        return add(adj_multiply(received_matrix, h_exp), sent_matrix)
    elif mode == 2:
        return add(multiply(received_matrix, h_exp), sent_matrix)

