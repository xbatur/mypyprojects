from __future__ import unicode_literals
import youtube_dl
import os
from ftplib import FTP
import sys
class YDown():
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.url = ''
        self.file = []
        self.ip_adress = ''
        self.ftp = FTP('')
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def download(self):
        try:
            if os.path.exists("Musics"):
                pass
            else:
                os.mkdir("Musics")
            os.chdir("Musics")
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                if len(self.url) > 15:
                    ydl.download([self.url])
                else:
                    print(self.FAIL + "=====================" + self.ENDC)
                    print(self.FAIL + "URL IS NOT ACCEPTABLE" + self.ENDC)
                    print(self.FAIL + "=====================" + self.ENDC)
                MyDirectory = os.listdir(os.getcwd())
                for file in MyDirectory:
                    if file.endswith('.mp3') or file.endswith('.m4a') or file.endswith('.mp4'):
                        print(file)
                        os.rename(file, file.encode('latin-1', 'ignore'))
                        self.file.append(file)
        except Exception as msg:
            print(self.FAIL + "ERROR IN DOWNLOAD FNC: " + self.ENDC + str(msg) )
            return -1

    def uploadphone(self):
        try:
            self.ftp.connect(host=self.ip_adress,port=2221)
            self.ftp.login(user='android',passwd='12345')
            self.ftp.cwd('Music')
            for x in range(len(self.file)):
                if self.file[x] in self.ftp.nlst():
                    print(self.WARNING + self.file[x] + self.ENDC + " exist on phone.")
                else:
                    print(self.file[x])
                    self.ftp.storbinary('STOR ' + self.file[x], open(self.file[x], 'rb'))
        except Exception as msg:
            print(self.FAIL + "ERROR IN UPLOADPHONE FNC: " + self.ENDC + str(msg))
            return -1

def main():
    try:
        Dwn = YDown()
        print(Dwn.HEADER + "Welcome MP3 download pc /upload phone over FTP program." + Dwn.ENDC)
        while 1:
            if not Dwn.ip_adress:
                Dwn.ip_adress = input(Dwn.OKGREEN + "Give IP Adress> " + Dwn.ENDC)
            Dwn.url = input(Dwn.OKBLUE + "Give Youtube URL: " + Dwn.ENDC)
            if Dwn.url == 'q':
                sys.exit(0)
            val1 = Dwn.download()
            if val1 != -1:
                print(Dwn.OKGREEN + "DOWNLOAD SUCCESSFUL" + Dwn.ENDC)
                print(Dwn.OKGREEN + "===================" + Dwn.ENDC)
            val2 = Dwn.uploadphone()
            if val2 != -1:
                print(Dwn.OKGREEN + "UPLOAD SUCCESSFUL" + Dwn.ENDC)
                print(Dwn.OKGREEN + "=================" + Dwn.ENDC)
    except KeyboardInterrupt:
        sys.exit(0)
main()