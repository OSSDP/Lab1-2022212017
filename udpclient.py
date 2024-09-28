import socket

class udpclient:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        """设置超时时间，以便在没有消息时不会阻塞"""
        self.sock.settimeout(1)

    def sendmsg(self, msg):
        try:
            self.sock.sendto(msg, self.server_address)
        except socket.error as e:
            print(f"Send error: {e}")
            self.stop()

    def recmsg(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            return data, addr
        except socket.timeout:
            return None, None
        except socket.error as e:
            print(f"Receive error: {e}")
            self.stop()
            return None, None

    def stop(self):
        self.sock.close()

