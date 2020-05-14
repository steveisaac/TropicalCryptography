from tropical_key_exchange import generate_m_h, generate_exponent, compute_intermediaries
from attack import attack


def example(dimensions=30):
    m, h = generate_m_h(dimensions)
    print(f'Generated M and H with order {dimensions}x{dimensions}')
    a = generate_exponent()
    print(f'Generated exponent: {a}')
    m_a, _ = compute_intermediaries(m, h, a)
    print('Calculated M_a')
    print('Attack provided with public values M, H, and M_a')
    derived_exponent = attack(m, h, m_a, 100000, 100)
    if derived_exponent[0] is True:
        print(f'Attack found M_n reaches equilibria in {derived_exponent[1]} steps')
    elif derived_exponent:
        if derived_exponent[0] == a:
            print('Attack successful')
            print(f'a found in {derived_exponent[1]} steps')
            print(f'Cycle length: {derived_exponent[2]}')
        else:
            print('Attack failed')
    else:
        print('Attack failed')

    return m, h, a


if __name__ == '__main__':
    parameters = example()
