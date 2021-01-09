import os
from threading import Thread


class Server(Thread):

    def run(self):
        os.system('cd "C:/Program Files (x86)/torcs" & wtorcs.exe -T  -nofuel -nolaptime -t 1000000000>NUL')


class Server_gui(Thread):

    def run(self):
        os.system('cd "C:/Program Files (x86)/torcs" & wtorcs.exe -nofuel -nolaptime -t 1000000000>NUL')



if __name__ == "__main__":
    Server_gui().start()
