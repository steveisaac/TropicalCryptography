from tropical_key_exchange import *


def attack(m, h, a, max_terms=30000, cycle_max=20):
    """
    The attack works by finding the point in which the elementwise differences between (M, H)^i-1 and (M, H)^i begin
    to cycle. The exponent from which A is generated can then be derived from A, the point at which the cycle began,
    and the values of the cyclic elementwise differences.

    I have not yet found an M H A combination which is not vulnerable to this attack
    """
    mi, hi = m, h
    diff_hists = [[[None]] for i in range(cycle_max)]
    hi = h
    for i in range(2, max_terms + 2):
        # (M, H)^i-1
        mi_previous = mi
        # (M, H)^i
        mi, hi = semigroup_op_1(mi, hi, m, h)

        # Elementwise difference between (M, H)^i and (M, H)^i-1
        diff = [[mi_val - mip_val for mi_val, mip_val in zip(mi_row, mip_row)]
                for mi_row, mip_row in zip(mi, mi_previous)]

        for j in range(cycle_max):
            # Check if the current elementwise difference is equal to a historic elementwise difference
            if diff == diff_hists[j]:
                seq_order = j + 1
                # Sum of the elements at position [0, 0] in the cycle of elementwise differences
                cycle_sum = sum([diff_hists[k][0][0] for k in range(seq_order)])
                for k in range(seq_order):
                    # The below if statement is a quick means of filtering out local cycles
                    if (a[0][0] - mi[0][0] - sum(
                            [diff_hists[(seq_order - 1) - l][0][0] for l in range(k)])) % cycle_sum == 0:
                        exp = (((a[0][0] - mi[0][0]) // cycle_sum) * seq_order) + i + k
                        # The below if statement filters out any local cycles that slip through the last.
                        # It is only necessary in rare cases and is costly.
                        if compute_intermediaries(m, h, exp)[0] == a:
                            return exp, i, seq_order

        # Remove oldest difference and add current difference to difference histories
        diff_hists.pop()
        diff_hists.insert(0, diff)

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



