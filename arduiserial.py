import os,time,sys,serial
from threading import Thread
class FArdui():

    def __init__(self):
        serial
        self.ports = []
        self.gate = False
        self.device = ""
        self.usbs = ['ttyUSB0','ttyUSB1','ttyUSB2','ttyUSB3']
        self.yourusb = ""
        self.find = False
        self.serialstatus = False
        self.serialport = None
        self.mem = []
        self.started = False
        self.selecting = 0
        self.firstplug = False
        self.olddevices = []
        self.newdevices = []
        self.boot = False
    def search(self):
        print("PLEASE PLUG OUT YOUR DEVICE..")
        print("WAIT.", end="")
        for x in range(3):
            print(".",end="",flush=True)
            time.sleep(1)
        while self.boot == False:
            print("SCANNING")
            os.chdir("/dev/")
            devices = os.listdir(".")
            if not self.firstplug:
                for x in devices:
                    self.olddevices.append(x)
                    self.firstplug = True
            for y in devices:
                if y not in self.olddevices:
                    self.newdevices.append(y)
                    self.olddevices.append(y)

            if self.newdevices:
                for x in range(0,5):
                    print(self.newdevices)
                    print("ttyUSB"+str(x))
                    if "ttyUSB"+str(x) in self.newdevices:
                        self.device = "/dev/ttyUSB"+str(x)
                    if "COM"+str(x) in self.newdevices:
                        self.device = "COM"+str(x)
                    print("Your device is: " + self.device)
                    question = input("Confirm? Y/N> ")
                    if question == 'y':
                        self.boot = True
                        break
                    if question == 'n':
                        pass
            time.sleep(5)

    def connection_test(self):
        try:
            print(self.device)
            self.serialport = serial.Serial(self.device,9600)
            self.serialport.flush()
            self.serialstatus = True
            print("CONNECTED.")
        except Exception as msg:
            print("ERROR : CONNECTION DIDN'T ESTABLISHED")
            print(str(msg))
            self.serialstatus = False

    def screenclear(self):
        os.system("clear")
        if self.gate == True:
            print("WAIT PLEASE...")
            self.gate = False
        if self.gate == False:
            print("DEVICE: " + self.device)
            if self.serialstatus == True:
                print("SERIAL COMMUNICATION: " + "OPEN")
            else:
                print("SERIAL COMMUNICATION: " + "CLOSE")
            if self.started == True:
                print("LISTENER MODE: " + "ON")
            else:
                print("LISTENER MODE: " + "OFF")
            print("INPUT 1:FOR SEND TEXT")
            print("INPUT 2: SHOW MESSAGES")
            print("INPUT Q: QUIT")
    def readfromserial(self):
        self.started = True
        while True:
            try:
                inputs = self.serialport.readline()
                if len(inputs) > 0:
                    print("Message From Arduino: ",end="")
                    print(inputs)
                    self.mem.append(inputs)
                    self.gate = True
                    FArdui.screenclear(self)
                else:
                    self.gate = False
                    FArdui.screenclear(self)
            except Exception:
                pass
    def conn_main(self):
        while self.serialstatus == True:
            schoice = input("1 = Send Text\n"+"2 = Show Messages\n"+"q = quit")
            try:
                if schoice == '1':
                    text = input("Input text > ")
                    print("Sending text...")
                    self.serialport.write(b'202')
                    self.serialport.flush()
                    time.sleep(1)
                    self.serialport.write(bytes(text, "utf-8"))
                    self.serialport.flush()
                    self.serialport.write(bytes("son", "utf-8"))
                    self.serialport.flush()
                    print("Sended.")
                if schoice == '2':
                    print(self.mem)
                if schoice == 'q':
                    sys.exit(0)
            except Exception as msg:
                print("ERROR CONNECTING TO DEVICE...")
                print(str(msg))
                self.serialstatus = False
                time.sleep(3)
def main():
    try:
        fa = FArdui()
        thread2 = Thread(target=fa.search())
        thread2.start()
        if fa.boot == True:
            fa.connection_test()
            fa.screenclear()
            thread1 = Thread(target=fa.readfromserial)
            thread1.start()
            thread3 = Thread(target=fa.conn_main)
            thread3.start()
        while True:
            time.sleep(10)
            if fa.serialstatus == False:
                thread2.join()
                fa.connection_test()
                thread1 = Thread(target=fa.readfromserial)
                thread1.start()
                thread3 = Thread(target=fa.conn_main)
                thread3.start()
        loop = 0
    except KeyboardInterrupt:
        sys.exit(0)

main()