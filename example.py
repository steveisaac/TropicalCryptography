from time import process_time

from tropical_key_exchange import generate_m_h, generate_exponent, compute_intermediaries
from attack import attack


def example(dimensions=30):
    m, h = generate_m_h(dimensions)
    print(f'Generated M and H with order {dimensions}x{dimensions}')
    exponent = generate_exponent()
    print(f'Generated exponent: {exponent}')
    a, _ = compute_intermediaries(m, h, exponent)
    print('Calculated A')
    print('Attack provided with public values M, H, and A')
    derived_exponent = attack(m, h, a)
    if derived_exponent:
        print(f'Attack derived exponent: {derived_exponent[0]}')
        if derived_exponent[0] == exponent:
            print('Attack successful')
        else:
            print('Attack failed')
    else:
        print('Attack failed')

    return m, h, exponent


if __name__ == '__main__':
    parameters = example()
