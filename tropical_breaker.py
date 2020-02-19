from tropical_key_exchange import *


def breaker(m, h, a, max_terms=1000, cycle_max=10, m_order=30):
    mi, hi = m, h
    diffs = [[None] for i in range(cycle_max)]
    hi = h
    check_next = False
    set_break = False
    for i in range(max_terms):
        mi_previous = mi
        mi, hi = semigroup_op_1(mi, hi, m, h)
        for j in range(cycle_max - 1, 0, -1):
            # slice because otherwise diffs[j] and diffs[j-1] would become pointers to the same list
            diffs[j] = diffs[j-1][:]
        diffs[0] = [[a - b for a, b in zip(i, j)] for i, j in zip(mi, mi_previous)]
        if check_next:
            if diffs[0] == diffs[order]:
                offset = i + 2

                break
            else:
                check_next = False
        for j in range(1, cycle_max):
            if diffs[0] == diffs[j]:
                offset = i + 2
                order = j
                for row in range(m_order):
                    for column in range(m_order):
                        cycle_sum = sum([diffs[k][row][column] for k in range(order)])
                        if cycle_sum:
                            break
                    if cycle_sum:
                        break

                for k in range(order):
                    if (a[row][column] - mi[row][column] - sum([diffs[(order - 1) - l][row][column] for l in range(k)])) % cycle_sum == 0:
                        extra = k
                        set_break = True
                        break
                if set_break:
                    break
        if set_break:
            break
    if i == max_terms - 1:
        print("Unbroken/n")
        return False
    # print((((a[row][column] - mi[row][column]) // cycle_sum) * order) + offset + extra == e1, extra)
    return (((a[row][column] - mi[row][column]) // cycle_sum) * order) + offset + extra, offset - 2, order


repetitions = 1000
# number of terms to break
term_indexes = []
orders = []
errors = []

for ii in range(repetitions):
    if (ii + 1) % 100 == 0:
        print("Iteration: ", ii)
        print("max terms searched: ", max(term_indexes))
        print("max cycle length: ", max(orders))
        print("percentage broken: ", (len(term_indexes) * 100) / (ii + 1), "%")
    m, h = generate_m_h(30)
    e1, e2 = (generate_exponent() for ii in range(2))
    i1, i2 = compute_intermediaries(m, h, e1), compute_intermediaries(m, h, e2)
    bb = breaker(m, h, i1[0], 2000, 20)
    if bb:
        if e1 == bb[0]:
            term_indexes.append(bb[1])
            orders.append(bb[2])
        else:
            errors.append([m, h, e1, e2, i1, i2, bb])
            print(bb[1], e1)
    else:
        errors.append((m, h, i1[0]))

print("max terms searched: ", max(term_indexes))
print("max cycle length: ", max(orders))
print("percentage broken: ", (len(term_indexes) * 100) / repetitions, "%")
