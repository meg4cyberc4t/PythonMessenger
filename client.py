import socket
import threading

while True:
    input_host = input("Input your IP server" \
                       "(Default: 127.0.0.1): ")
    if input_host.replace(".", "").strip().isnumeric():
        HOST = input_host
        break
    elif input_host.strip() == "":
        HOST = "127.0.0.1"
        break
    else:
        print("Incorrect IP server...")

while True:
    input_port = input("Input port" \
                       "(Default: 10000): ")
    if input_port.isnumeric():
        PORT = int(input_port)
        break
    elif input_port.strip() == "":
        PORT = 10000
        break
    else:
        print("Incorrect port...")    

class Client:
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.nickname = input("Please choose a nickname: ")

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def gui_loop(self):
        print(f"Your nickname: {self.nickname}\n")
        while True:
            self.write()
        self.gui_done = True

    def write(self):
        message = input()
        self.sock.send(f"{self.nickname}: {message}".encode('utf-8'))

    def stop(self):
        self.running = False
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                message = message.decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

try:
    client = Client(HOST, PORT)
except ConnectionRefusedError:
    print("No server connection")
