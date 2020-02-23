from tropical_key_exchange import *


def attack_1(m, h, a, max_terms=1000, cycle_max=10):
    mi, hi = m, h
    diffs = [[None] for i in range(cycle_max)]
    hi = h
    check_next = False
    # set_break = False
    for i in range(max_terms):
        mi_previous = mi
        mi, hi = semigroup_op_1(mi, hi, m, h)
        for j in range(cycle_max - 1, 0, -1):
            # slice because otherwise diffs[j] and diffs[j-1] would become pointers to the same list
            diffs[j] = diffs[j-1][:]
        diffs[0] = [[a - b for a, b in zip(i, j)] for i, j in zip(mi, mi_previous)]
        if check_next:
            if diffs[0] == diffs[seq_order]:
                offset = i + 2

                break
            else:
                check_next = False
        for j in range(1, cycle_max):
            if diffs[0] == diffs[j]:
                offset = i + 2
                seq_order = j
                for row in range(len(m)):
                    for column in range(len(m[0])):
                        cycle_sum = sum([diffs[k][row][column] for k in range(seq_order)])
                        if cycle_sum:
                            for k in range(seq_order):
                                if (a[row][column] - mi[row][column] - sum([diffs[(seq_order - 1) - l][row][column]
                                                                            for l in range(k)])) % cycle_sum == 0:
                                    """
                                    i + 2 is number of iterations to reach mi
                                    k is number of elements from cycle needed to find a after whole cycles
                                    have been added
                                    """
                                    return ((((a[row][column] - mi[row][column]) // cycle_sum) * seq_order) + i + 2 + k,
                                            i, seq_order)
    print("Unbroken")
    print(i)
    print(cycle_sum)
    print(j)
    print(mi)
    print(diffs[0])
    print(diffs[j])
    return False
    # print((((a[row][column] - mi[row][column]) // cycle_sum) * order) + offset + extra == e1, extra)


def test_attack(max_terms=1500, cycle_max=15, reps=10000,
                matrix_order=30, element_max=1000, include_positives=True, include_zero=True):
    term_indexes = []
    orders = []
    errors = []

    for i in range(reps):
        m, h = generate_m_h(matrix_order, element_max, include_positives, include_zero)
        e1, e2 = (generate_exponent() for i in range(2))
        i1, i2 = compute_intermediaries(m, h, e1), compute_intermediaries(m, h, e2)
        a = attack_1(m, h, i1[0], max_terms, cycle_max)
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
    print("Number broken:", (len(term_indexes) * 100) / reps, "%")
    print("Max terms searched:", max(term_indexes))
    print("Max cycle length:", max(orders))
    print("Cycle occurrences:")
    for i in set(orders):
        print(i, ":", orders.count(i))

    return errors
