import pickle
import socket
import sys

from tropical_key_exchange import *


class TropicalPeer:
    def __init__(self, partnerIP, IP=socket.gethostbyname(socket.gethostname()), port='9699', mode=1):
        self.partnerIP = partnerIP
        self.IP = IP
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exponent = generate_exponent()
        if self.IP > self.partnerIP:
            self.m, self.h = generate_m_h()
            self.server = True
            self.socket.bind((self.IP, self.port))
            self.socket.listen(0)
            self.client_socket, self.client_address = self.socket.accept()
        else:
            self.m, self.h = None, None
            self.server = False
            connected = False
            while not connected:
                try: # must fix for connection refused
                    self.socket.connect((self.partnerIP, self.port))
                    connected = True
                except ConnectionRefusedError:
                    pass
                except socket.error as message:
                    print("Couldn't connect to peer: " + str(message))
                    sys.exit(1)
            self.client_socket = None
            self.client_address = None
        self.a, self.b, self.h_exp = None, None, None

    def exchange_m_h(self):
        if self.server:
            print("Sending initial values")
            print(self.client_socket.send(pickle.dumps(self.m)))
            self.client_socket.sendall(pickle.dumps(self.h))
        else:
            self.m = pickle.loads(self.socket.recv(32768))
            self.h = pickle.loads(self.socket.recv(32768))
            print("Received initial values")

    def exchange_a_b(self):
        self.a, self.h_exp = compute_intermediaries(self.m, self.h, self.exponent)
        if self.server:
            print("Sending intermediary values")
            print(self.client_socket.send(pickle.dumps(self.a)))
            self.b = pickle.loads(self.client_socket.recv(32768))
            print("Received intermediary values")
            self.client_socket.close()
        else:
            self.b = pickle.loads(self.socket.recv(32768))
            print("Received intermediary values")
            print("Sending intermediary values")
            print(self.socket.send(pickle.dumps(self.a)))
            # self.socket.sendall(self.a)
            print("sent")
        self.socket.close()

    def derive_key(self):
        print("Computing secret key")
        return compute_secret_key(self.b, self.a, self.h_exp)
        # output file. might want to allow specifying destination. put dest in init file
        # also change random generation to use secrets module


# T = TropicalPeer("DESKTOP-K0EJFJJ", "144.32.246.48")
# T.exchange_m_h()
# T.exchange_a_b()
# T.derive_key("haha")
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("DESKTOP-K0EJFJJ", 9699))
# s.sendall(T.derive_key("haha"))
# s.close()

if __name__ == "__main__":
    T = TropicalPeer(sys.argv[1], *sys.argv[3:])  # check if argv blank None is returned
    T.exchange_m_h()
    T.exchange_a_b()
    key = T.derive_key()
    print(key[1])

    print(T.exponent)
    try:
        output = open(sys.argv[2], "w")
        output.write(" ".join([hex(j) for i in T.derive_key() for j in i]))
        output.close()
    except FileExistsError as message:
        print(message)




