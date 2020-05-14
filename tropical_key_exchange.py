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
    Returns the random exponent a on the order of 2^200.
    """
    return secrets.randbits(order) + 2**order


# Computes intermediaries with square-and-multiply method utilising associative property of semigroup operation
def compute_intermediaries(matrix_m, matrix_h, a, mode=1):
    if mode == 1:
        semigroup_op = semigroup_op_1
    # mode == 2 does not work due to semigroup_op_2 not being associative
    else:
        semigroup_op = semigroup_op_2
    sq_and_mul = [(matrix_m, matrix_h)]
    for i in range(len(bin(a)[2:]) - 1):
        sq_and_mul.append(semigroup_op(*sq_and_mul[i], *sq_and_mul[i]))
    first_one = True
    intermediaries = None
    for i in range(len(bin(a)[2:])):
        if bin(a)[:1:-1][i] == "1" and first_one:
            intermediaries = sq_and_mul[i]
            first_one = False
        elif bin(a)[:1:-1][i] == "1":
            intermediaries = semigroup_op(*intermediaries, *sq_and_mul[i])
    return intermediaries


# Use to check intermediaries without square-and-multiply method
# Only practical for small exponents (<100000)
def verify_intermediaries(m, h, a, mode=1):
    if mode == 1:
        semigroup_op = semigroup_op_1
    else:
        semigroup_op = semigroup_op_2
    intermediaries = m, h
    for i in range(a - 1):
        intermediaries = semigroup_op(*intermediaries, m, h)
    return intermediaries


def compute_secret_key(m_b, m_a, h_a, mode=1):
    if mode == 1:
        return add(adj_multiply(m_b, h_a), m_a)
    elif mode == 2:
        return add(multiply(m_b, h_a), m_a)

