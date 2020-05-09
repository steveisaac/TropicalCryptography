from tropical_key_exchange import *


def attack(m, h, a, max_terms=30000, cycle_max=20):
    #
    # The attack works by finding the point at which the elementwise differences between (M, H)^i-1 and (M, H)^i begin
    # to cycle. The exponent from which A is generated can then be derived from A, the point at which the cycle began,
    # and the values of the cyclic elementwise differences.
    #
    # We have not yet found an M, H, A combination which is not vulnerable to this attack
    #
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
                # Sum of the elements at position [0, 0] in the cycle of elementwise differences
                cycle_sum = sum([hist_diffs[index][0][0] for index in range(cycle_order)])
                for j in range(cycle_order):
                    # Sum of a section at the start of the cycle
                    section_sum = sum([hist_diffs[cycle_order - 1 - index][0][0] for index in range(j)])

                    # The below statement derives a possible difference between the first element of A and (M, H)^i
                    #
                    # The reason multiple candidates need to be tested is that the element of the difference cycle
                    # that is equal to (M, H)^exp - (M, H)^exp-1 is unknown
                    candidate_difference = a[0][0] - mi[0][0] - section_sum

                    # If cycle_sum divides candidate_difference evenly it is the true difference between A and (M, H)^i
                    # There are very rare exceptions to this where candidate_difference can be divided by the true
                    # value as well as a false value
                    if candidate_difference % cycle_sum == 0:

                        # Exponent is (floor(A - (M, H)^i / cycle sum) * cycle order) + i + j
                        exp = (((a[0][0] - mi[0][0]) // cycle_sum) * cycle_order) + i + j

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


def test_attack(reps=10000, max_terms=100000, cycle_max=30,
                matrix_order=30, m_min=-1000, m_max=1000, h_min=-1000, h_max=1000):
    term_indexes = []
    orders = []
    errors = []

    for i in range(reps):
        m, h = generate_m_h(matrix_order, m_min, m_max, h_min, h_max)
        e1, e2 = (generate_exponent() for i in range(2))
        i1, i2 = compute_intermediaries(m, h, e1), compute_intermediaries(m, h, e2)
        a = attack(m, h, i1[0], max_terms, cycle_max)
        if a:
            if e1 == a[0]:
                term_indexes.append(a[1])
                orders.append(a[2])
            else:
                errors.append((m, h, i1[0]))
                print("Incorrect attack return", a[1], e1)
        else:
            errors.append((m, h, i1[0]))
            print("Attack could not find exponent")
        if (i + 1) % 100 == 0:
            print("Iteration: ", i + 1)
            print("Percentage broken: ", (len(term_indexes) * 100) / (i + 1), "%")
            print("Max terms searched: ", max(term_indexes))
            print("Max cycle length: ", max(orders))

    print("Matrix order:", matrix_order)
    print("Repetitions:", reps)
    print("Number broken:", len(term_indexes))
    print("Max terms searched:", max(term_indexes))
    print("Max cycle length:", max(orders))
    print("Cycle occurrences:")
    for i in set(orders):
        print(i, ":", orders.count(i))

    return errors
