# udpserver.py
import socket

class udpserver:
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__s.bind((self.__ip, self.__port))

    def start(self):
        print("server is running...")

    def recmsg(self):
        data, addr = self.__s.recvfrom(1024)
        print(f"Received {data} from {addr}")
        return data, addr

    def sendmsg(self, addr, msg):
        print("服务器端：")
        print(msg)
        print(addr)
        self.__s.sendto(msg, addr)

    def stop(self):
        self.__s.close()
