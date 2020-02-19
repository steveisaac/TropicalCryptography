from tropical_key_exchange import *


def breaker(m, h, a, mode=1, max_terms=1000):
    if mode == 1:
        semigroup_op = semigroup_op_1
    elif mode == 2:
        semigroup_op = semigroup_op_2
    mi, hi = m, h
    diffs = [[None] for i in range(10)]
    hi = h
    check_next = False
    set_break = False
    for i in range(max_terms):
        mi_previous = mi
        mi, hi = semigroup_op(mi, hi, m, h)
        for j in range(9, 0, -1):
            # slice because otherwise diffs[j] and diffs[j-1] would become pointers to the same list
            diffs[j] = diffs[j-1][:]
        diffs[0] = [[a - b for a, b in zip(i, j)] for i, j in zip(mi, mi_previous)]
        if check_next:
            if diffs[0] == diffs[order]:
                offset = i + 2

                break
            else:
                check_next = False
        for j in range(1, 10):
            if diffs[0] == diffs[j]:
                offset = i + 2
                order = j
                for row in range(30):
                    for column in range(30):
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
        print(mi)
        print(mi_previous)
        for i in range(10):
            print()
            print(diffs[i])
        return False
    print((((a[row][column] - mi[row][column]) // cycle_sum) * order) + offset + extra == e1, extra)
    return (((a[row][column] - mi[row][column]) // cycle_sum) * order) + offset + extra, offset - 2


repetitions = 10000
# number of terms to break
terms_index = []
errors = []
mode = 2
for ii in range(repetitions):
    if ii % 1000 == 0 and ii > 0:
        print("/nIteration: ", ii, "max: ", max(terms_index),
              "percentage broken: ", (len(terms_index) * 100) / (ii + 1), "%")
    m, h = generate_m_h(10)
    e1, e2 = (generate_exponent() for ii in range(2))
    i1, i2 = compute_intermediaries(m, h, e1, mode), compute_intermediaries(m, h, e2, mode)
    bb = breaker(m, h, i1[0], mode)
    if bb:
        if e1 == bb[0]:
            terms_index.append(bb[1])
        else:
            errors.append([m, h, e1, e2, i1, i2, bb])
            print(bb[1], e1)
    else:
        errors.append((m, h, i1[0]))

print("max: ", max(terms_index), "percentage broken: ", (len(terms_index) * 100) / repetitions, "%")
