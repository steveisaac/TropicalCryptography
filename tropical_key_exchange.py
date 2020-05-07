import secrets

from tropical_algebra import *


def generate_m_h(order=30, m_min=-1000, m_max=1000, h_min=-1000, h_max=1000):
    """
    Returns two order x order matrices filled with random integers.
    These are the public matrices M and H.
    """
    m = [[secrets.randbelow((m_max - m_min) + 1) + m_min for i in range(order)] for j in range(order)]
    h = [[secrets.randbelow((h_max - h_min) + 1) + h_min for i in range(order)] for j in range(order)]
    return m, h


def generate_exponent(order=200):
    """
    Returns the random exponent m on the order of 2^200.
    """
    return secrets.randbits(order) + 2**order


# Computes intermediaries with square-and-multiply method utilising associative property of semigroup operation
def compute_intermediaries(matrix_m, matrix_h, exponent_m, mode=1):
    if mode == 1:
        semigroup_op = semigroup_op_1
    else:
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
        elif bin(exponent_m)[:1:-1][i] == "1":
            intermediaries = semigroup_op(*intermediaries, *sq_and_mul[i])
    return intermediaries


# Use to check intermediaries without square-and-multiply method
# Only viable for small exponents
def verify_intermediaries(m, h, exponent, mode=1):
    if mode == 1:
        semigroup_op = semigroup_op_1
    else:
        semigroup_op = semigroup_op_2
    intermediaries = m, h
    for i in range(exponent - 1):
        intermediaries = semigroup_op(*intermediaries, m, h)
    return intermediaries


def compute_secret_key(received_matrix, sent_matrix, h_exp, mode=1):
    if mode == 1:
        return add(adj_multiply(received_matrix, h_exp), sent_matrix)
    elif mode == 2:
        return add(multiply(received_matrix, h_exp), sent_matrix)

