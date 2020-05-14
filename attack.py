from numpy import array, zeros

from tropical_key_exchange import *


def attack(m, h, a, max_terms=None, cycle_max=None):
    #
    # The attack works by finding the point at which the elementwise differences between (M, H)^i-1 and (M, H)^i begin
    # to cycle. The exponent from which A is generated can then be derived from A, the point at which the cycle began,
    # and the values of the cyclic elementwise differences.
    #
    # We have not yet found an M, H, A combination which is not vulnerable to this attack
    #
    if max_terms is None:
        max_terms = 100000
    if cycle_max is None:
        cycle_max = 2 * len(m)
    mi, hi = m, h
    hist_diffs = [[[None]] for i in range(cycle_max)]
    hi = h
    for i in range(2, max_terms + 2):
        # (M, H)^i-1
        mi_previous = mi
        # (M, H)^i
        mi, hi = semigroup_op_1(mi, hi, m, h)

        # Matrix of elementwise differences between (M, H)^i and (M, H)^i-1
        diff = [[mi_val - mip_val for mi_val, mip_val in zip(mi_row, mip_row)]
                for mi_row, mip_row in zip(mi, mi_previous)]

        for hist_index in range(cycle_max):
            # Check if the current elementwise difference is equal to a historic elementwise difference matrix
            if diff == hist_diffs[hist_index]:
                cycle_order = hist_index + 1
                # Sum of the matrices in the cycle of elementwise differences
                cycle_sum = sum([array(hist_diffs[index]) for index in range(cycle_order)])
                # Checks for special case where the cycle sum is the zero matrix
                zero_check = cycle_sum == zeros(cycle_sum.shape)
                if zero_check.all():
                    return True, i, 1
                # Locates non-zero element in cycle sum
                for row in range(len(cycle_sum)):
                    for column in range(len(cycle_sum)):
                        if cycle_sum[row][column]:
                            break
                    if cycle_sum[row][column]:
                        break
                for j in range(cycle_order):
                    # Sum of a section at the start of the cycle
                    section_sum = sum([hist_diffs[cycle_order - 1 - index][row][column] for index in range(j)])

                    # The below statement derives a possible difference between the first element of A and (M, H)^i
                    #
                    # The reason multiple candidates need to be tested is that the element of the difference cycle
                    # that is equal to (M, H)^exp - (M, H)^exp-1 is unknown
                    candidate_difference = a[row][column] - mi[row][column] - section_sum

                    # If cycle_sum divides candidate_difference evenly it is the true difference between A and (M, H)^i
                    # There are very rare exceptions to this where candidate_difference can be divided by the true
                    # value as well as a false value
                    if candidate_difference % cycle_sum[row][column] == 0:

                        # Exponent is (floor(A - (M, H)^i / cycle sum) * cycle order) + i + j
                        exp = (((a[row][column] - mi[row][column]) // cycle_sum[row][column]) * cycle_order) + i + j

                        # The below if statement filters out aforementioned exceptions
                        # This is achieved by checking to see if (M, H)^exp gives A
                        if compute_intermediaries(m, h, exp)[0] == a:
                            return exp, i, cycle_order

        # Remove oldest difference matrix from and add current matrix to historic differences
        hist_diffs.pop()
        hist_diffs.insert(0, diff)

    # If max terms are reached without finding exponent False is returned
    # Try attacking again with increased max terms and cycle max
    print("Unbroken")
    return False


def crack_key(m, h, a, max_terms=None, cycle_max=None):
    vals = attack(m, h, a, max_terms=None, cycle_max=None)
    if vals:
        if vals is True:
            return compute_secret_key(m, h, len(m)**2)
        else:
            return compute_secret_key(m, h, vals[0])
