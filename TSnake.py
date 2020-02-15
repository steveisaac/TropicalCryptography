from numpy import frombuffer, reshape
from sys import argv
import socket

from tropical_key_exchange import *


class TropicalPeer:
    def __init__(self, partnerIP, port=9699, mode=1):
        self.partnerIP = partnerIP
        self.IP = socket.gethostbyname(socket.gethostname())
        self.port = port
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
                connected = self.socket.connect((self.partnerIP, self.port))
                print(connected)
            self.client_socket = None
            self.client_address = None
        self.a, self.b, self.h_exp = None, None, None

    def exchange_m_h(self):
        if self.server:
            print("Sending initial values")
            self.client_socket.sendall(self.m)
            self.client_socket.sendall(self.h)
        else:
            self.m = reshape(frombuffer(self.socket.recv(4096), int), [30, 30])
            self.h = reshape(frombuffer(self.socket.recv(4096), int), [30, 30])
            print("Received initial values")

    def exchange_a_b(self):
        self.a, self.h_exp = compute_intermediaries(self.m, self.h, self.exponent)
        if self.server:
            print("Sending intermediary values")
            self.client_socket.sendall(self.a)
            self.b = reshape(frombuffer(self.client_socket.recv(4096), int), [30, 30])
            print("Received intermediary values")
            self.client_socket.close()
        else:
            self.b = reshape(frombuffer(self.socket.recv(4096), int), [30, 30])
            print("Received intermediary values")
            print("Sending intermediary values")
            self.socket.sendall(self.a)
        self.socket.close()

    def derive_key(self, dest):
        print("Computing and storing secret key")
        print(compute_secret_key(self.b, self.a, self.h_exp).tobytes())
        print("Storing key in dest")
        # output file. might want to allow specifying destination. put dest in init file
        # also change random generation to use secrets module


if __name__ == "__main__":
    print(argv[1])
    # T = TropicalPeer(argv[1], argv[3], argv[4]) # check if argv blank None is returned
    # T.exchange_m_h()
    # T.exchange_a_b()
    # T.derive_key(argv[2])




