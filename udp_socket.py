import socket
from pathlib import Path
import json
from datetime import datetime
from threading import Event

class UDPSocketServer():
    UDP_IP = '127.0.0.1'
    UDP_PORT = 5000
    SAVE_TO = Path("storage", "data.json")
    data = None
    
    def run(self, event: Event=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = self.UDP_IP, self.UDP_PORT
        sock.bind(server)
        while not event.is_set():
            data, address = sock.recvfrom(1024)
            self.data = self.data_parce(data.decode())
            self.data_save()
            sock.sendto("success".encode(), address)
        sock.close()
    
    def data_parce(self, data: str):
        return {key: value for key, value in [el.split("=") for el in data.split("&")]}
    
    def data_save(self):
        try:
            with open(self.SAVE_TO, "r") as fh:
                data = json.load(fh)
        except:
            data = {}

        data[str(datetime.now())] = self.data
        with open(self.SAVE_TO, "w") as fh:
            json.dump(data, fh)
        
def send_to_udp_server(data: bytes):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = UDPSocketServer.UDP_IP, UDPSocketServer.UDP_PORT
    sock.sendto(data, server)
    sock.recvfrom(1024)
    sock.close()


if __name__ == '__main__':
    server = UDPSocketServer()
    server.run()
