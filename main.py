from web_server import run_server
from udp_socket import UDPSocketServer
from threading import Thread, Event

def main():
    event = Event()
    web_server_thread = Thread(target=run_server, args=(event,))
    socket_server_thread = Thread(target=UDPSocketServer().run, kwargs={"event": event})
    web_server_thread.start()
    socket_server_thread.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Destroy servers")
        event.set()
        

if __name__ == "__main__":
    main()
    