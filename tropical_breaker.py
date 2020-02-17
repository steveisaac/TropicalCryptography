from tropical_key_exchange import *


def breaker(m, h, a):
    mi, hi = m, h
    m_previous = m
    diffs_previous = []
    break_count = 0
    for i in range(2**60):
        mi, hi = semigroup_op_1(mi, hi, m, h)
        diffs = [[a - b for a, b in zip(i, j)] for i, j in zip(mi, m_previous)]
        if diffs == diffs_previous:
            offset = i
            print(i, diffs_previous[0][0])
            break
            # break_count += 1
            # if break_count == 20:
            #     break
        m_previous = mi
        diffs_previous = diffs

    # Find nonzero element of diffs
    for i in range(len(diffs)):
        for j in range(len(diffs[i])):
            if diffs[i][j]:
                break
    if diffs[i][j]:
        return (a[i][j] - m[i][j]) // diffs[i][j], offset, a[i][j], m[i][j], (a[i][j] - m[i][j]) % diffs[i][j], (a[i][j] - m_previous[i][j]) // diffs[i][j]
    return False


m, h = generate_m_h(30)
e1, e2 = (generate_exponent() for i in range(2))
i1, i2 = compute_intermediaries(m, h, e1), compute_intermediaries(m, h, e2)
v1, v2 = verify_intermediaries(m, h, e1), verify_intermediaries(m, h, e2)
k = compute_secret_key(i2[0], *i1)
print("Key exchange successful: ", k == compute_secret_key(i1[0], *i2))
print(breaker(m, h, i1[0]))
print(e1)
