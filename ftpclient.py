from ftplib import FTP
import sys
class FTPCLIENT():

    def __init__(self):
        self.ftp = FTP('')
    def connect(self):
        try:
            self.ftp.connect('IPADRESS',1026)
            self.ftp.login(user='xboomer',passwd='12345')
            self.ftp.dir()
            self.ftp.retrlines('LIST')
        except Exception as msg:
            print("ERROR: " + str(msg))
            return -1
    def getfile(self):
        try:
            print("FILES : ")
            print(self.ftp.dir())
            filename = input("Give filename> ")
            localfile = open(filename, 'wb')
            self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
            localfile.close()
        except Exception as msg:
            print("RETRIVE FILE FAILED: " + str(msg))
    def upfile(self):
        try:
            filename = input("Give filename or filepath if> ")
            self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
        except Exception as msg:
            print("FILE UPLOAD FAILED: " + str(msg))

def main():
    print("FTP LOGGING IN..")
    print("-----------------")
    FTPC = FTPCLIENT()
    val = FTPC.connect()
    if val == -1:
        sys.exit(1)
    print("Call help for input commands")
    while 1:
        try:
            choice = input("> ")
            if choice.lower() == 'help':
                print("cmd: send a command \ngetfile: retrieve for a file\nupfile: upload for a file\nhelp: this command\nq: exit")
            elif choice.lower() == 'q':
                print("Good bye.")
                sys.exit(0)
            elif choice.lower() == 'getfile':
                FTPC.getfile()
            elif choice.lower() == 'upfile':
                FTPC.upfile()
            elif choice.lower() == 'cmd':
                try:
                    comm = input("Get command> ")
                    listen = FTPC.ftp.sendcmd(comm)
                    print(listen)
                except Exception as msg:
                    print("Command failed: " + str(msg))
            else:
                print("Invalid command for print commands type > 'help'")
        except KeyboardInterrupt:
            sys.exit(0)
main()
