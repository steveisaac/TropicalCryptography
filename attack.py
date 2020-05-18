from numpy import array, zeros
from warnings import warn

from tropical_key_exchange import *


def attack(m, h, m_a, max_terms=None, max_period=None):
    #
    # The attack works by finding the point at which the elementwise differences between (M, H)^n-1 and (M, H)^n become
    # periodic. a can then be derived from M_a, the point at which the cycle began, and the values of the periodic
    # elementwise differences.
    #
    # We have not yet found an M, H, M_a combination which is not vulnerable to this attack
    #
    if max_terms is None:
        max_terms = 100000
    if max_period is None:
        max_period = 2 * len(m)
    m_n, h_n = m, h
    hist_diffs = [[[None]] for i in range(max_period)]
    h_n = h
    for n in range(2, max_terms + 2):
        # (M, H)^n-1
        m_n_previous = m_n
        # (M, H)^n
        m_n, h_n = semigroup_op_1(m_n, h_n, m, h)

        # Matrix of elementwise differences between (M, H)^n and (M, H)^n-1
        diff = [[mi_val - mip_val for mi_val, mip_val in zip(mi_row, mip_row)]
                for mi_row, mip_row in zip(m_n, m_n_previous)]

        for hist_index in range(max_period):
            # Check if the current elementwise difference is equal to a historic elementwise difference matrix
            if diff == hist_diffs[hist_index]:
                period = hist_index + 1
                # Sum of the matrices in the cycle of elementwise differences
                period_sum = sum([array(hist_diffs[index]) for index in range(period)])
                # Checks for special case where period_sum is the zero matrix
                zero_check = period_sum == zeros(period_sum.shape)
                if zero_check.all():
                    if compute_intermediaries(m, h, n)[0] == m_a:
                        return n, n, 1
                # Locates non-zero element in period_sum
                for i in range(len(period_sum)):
                    for j in range(len(period_sum)):
                        if period_sum[i][j]:
                            row = i
                            column = j
                            break
                    if period_sum[i][j]:
                        break
                for k in range(period):
                    # Sum of a section at the start of the cycle
                    section_sum = sum([hist_diffs[period - 1 - index][row][column] for index in range(k)])

                    # The below statement derives a possible difference between the first element of A and (M, H)^n
                    #
                    # The reason multiple candidates need to be tested is that the element of the difference cycle
                    # that is equal to (M, H)^a - (M, H)^a-1 is unknown
                    candidate_difference = m_a[row][column] - m_n[row][column] - section_sum

                    # If period_sum divides candidate_difference evenly it is the true difference between M_a
                    # and (M, H)^n
                    # There may be very rare exceptions to this where a false candidate_difference can be divided evenly
                    # by the period_sum as well as the true one.
                    if candidate_difference % period_sum[row][column] == 0:

                        # Exponent is ((M_a - (M, H)^n / cycle sum) * cycle order) + n + k
                        a = (((m_a[row][column] - m_n[row][column]) // period_sum[row][column]) * period) + n + k

                        # The below if statement filters out aforementioned exceptions
                        # This is achieved by checking to see if (M, H)^a gives M_a
                        if compute_intermediaries(m, h, a)[0] == m_a:
                            return a, n, period

        # Remove oldest difference matrix from and add current matrix to historic differences
        hist_diffs.pop()
        hist_diffs.insert(0, diff)

    # If max terms are reached without finding exponent False is returned
    warning_msg = 'Attack reached max terms without finding a cycle. Try increasing max terms and cycle max.'
    warn(warning_msg, stacklevel=2)
    return False


def crack_key(m, h, m_a, m_b, max_terms=None, cycle_max=None):
    try:
        a = attack(m, h, m_a, max_terms=None, max_period=None)[0]
        m_a, h_a = compute_intermediaries(m, h, a)
        return compute_secret_key(m_b, m_a, h_a)
    except TypeError:
        pass
