from tropical_key_exchange import *


def mp(m):
    for i in m:
        s = ""
        for j in i:
            s += str(j) + " "
        print(s)
    print()


m, h = generate_m_h()

mp(m)
mp(h)

mp(multiply(m, m))
mp(multiply2(m, m))
mp(multiply(m, h))
mp(multiply2(m, h))
mp(add(m, h))

