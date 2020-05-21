from time import process_time

from tropical_key_exchange import generate_m_h, generate_exponent, compute_intermediaries
from attack import attack


def example(dimensions=30):
    m, h = generate_m_h(dimensions)
    # m, h = generate_m_h(dimensions, h_min=0, m_min=0)
    print(f'Generated M and H with order {dimensions}x{dimensions}')
    a = generate_exponent()
    print(f'Generated a: {a}')
    m_a, _ = compute_intermediaries(m, h, a)
    print('Calculated M_a')
    print('Attack provided with public values M, H, and M_a')
    start_time = process_time()
    derived_exponent = attack(m, h, m_a)
    end_time = process_time()
    if derived_exponent:
        if derived_exponent[0] == a:
            print('Attack successful.')
            print(f'a={derived_exponent[0]} found in {derived_exponent[1]} steps.')
            print(f'Cycle length: {derived_exponent[2]}')
            print(f'Time taken: {end_time - start_time}')
        else:
            print('Attack successful.')
            print(f'a={derived_exponent[0]} found in {derived_exponent[1]} steps')
            print(f'Cycle length: {derived_exponent[2]}')
            print(f'Time taken: {end_time - start_time}')
            print('Derived a differs from a when M_n = M_(n+1). The attack is still successful.')
    else:
        print('Attack failed.')

    return m, h, a


if __name__ == '__main__':
    parameters = example()
