from tropical_key_exchange import *
from numpy import array


def breaker(m, h, a):
    mi, hi = m, h
    m_previous = m
    diffs_previous = []
    break_count = 0
    for i in range(1000):
        mi, hi = semigroup_op_1(mi, hi, m, h)
        diffs = [[a - b for a, b in zip(i, j)] for i, j in zip(mi, m_previous)]
        if diffs == diffs_previous:
            offset = i + 2
            print(i, diffs_previous[0][0])
            break
            break_count += 1
        m_previous = mi
        diffs_previous = diffs
    if i == 999:
        return False
    for j in range(30):
        for k in range(30):
            if diffs[j][k]:
                break
        if diffs[j][k]:
            break
    return i, ((a[j][k] - mi[j][k]) // diffs[j][k]) + offset


repeat_index = []
for i in range(10):
    m, h = generate_m_h(30)
    e1, e2 = (generate_exponent() for i in range(2))
    i1, i2 = compute_intermediaries(m, h, e1), compute_intermediaries(m, h, e2)
    b = breaker(m, h, i1[0])
    if b:
        if e1 == b[1]:
            repeat_index.append(b[0])
        else:
            print(b[1], e1)

print("max", max(repeat_index), "length: ", len(repeat_index))
