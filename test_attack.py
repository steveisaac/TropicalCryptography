from time import process_time

from attack import attack
from tropical_key_exchange import *


def test_attack(reps=10000, max_terms=100000, max_period=30,
                matrix_order=30, m_min=-1000, m_max=1000, h_min=-1000, h_max=1000):
    term_indexes = []
    orders = []
    times = []
    errors = []

    for i in range(reps):
        m, h = generate_m_h(matrix_order, m_min, m_max, h_min, h_max)
        a = generate_exponent()
        m_a, _ = compute_intermediaries(m, h, a)
        start_time = process_time()
        derived_a = attack(m, h, m_a, max_terms, max_period)
        end_time = process_time()
        times.append(end_time-start_time)
        if derived_a:
            if derived_a[0] is True:
                term_indexes.append(derived_a[1])
                orders.append(derived_a[2])
            else:
                if a == derived_a[0]:
                    term_indexes.append(derived_a[1])
                    orders.append(derived_a[2])
                else:
                    errors.append((m, h, m_a))
                    print("Incorrect attack return", derived_a[1], a)
        else:
            errors.append((m, h, m_a))
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

    return term_indexes, orders, times, errors
