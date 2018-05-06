import urllib.request
import cv2
import numpy as np
import sys
import time
import os
import threading
import socket
class TrackWebcam():

  def __init__(self):
    self.HEADER = '\033[95m'
    self.OKBLUE = '\033[94m'
    self.OKGREEN = '\033[92m'
    self.WARNING = '\033[93m'
    self.FAIL = '\033[91m'
    self.ENDC = '\033[0m'
    self.BOLD = '\033[1m'
    self.UNDERLINE = '\033[4m'
    self.ip_adress = ""
    self.old_urls = []
    self.memory = []
    self.error = False
    self.trry = False
    self.org = ""
  def diffImg(self,t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_or(d1, d2)

  def capture(self):
    try:
      #print("BURAYA GELDIM")
      url = 'http://{}:8080/shot.jpg'.format(self.ip_adress)
      imgResp = urllib.request.urlopen(url)
      # Numpy to convert into a array
      imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
      # Finally decode the array to OpenCV usable format ;)
      img = cv2.imdecode(imgNp, -1)
      # cam = cv2.VideoCapture(0) # for webcam
      threshold = 630000 # this value changing every phone and ambient light intensity so test and replace it. (for S3)
      #2028320 sony
      winName = "Movement Indicator"
      cv2.namedWindow(winName)
      # Read three images first:
      t_minus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
      t = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
      t_plus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
      while True:
        try:
          counter = 0
          url = 'http://{}:8080/shot.jpg'.format(self.ip_adress)
          imgResp = urllib.request.urlopen(url)
          # Numpy to convert into a array
          imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
          # Finally decode the array to OpenCV usable format ;)
          img = cv2.imdecode(imgNp, -1)
          cv2.imshow(winName, TrackWebcam.diffImg(self,t_minus, t, t_plus))
          print(cv2.countNonZero(TrackWebcam.diffImg(self, t_minus, t, t_plus)))
          if cv2.countNonZero(TrackWebcam.diffImg(self,t_minus, t, t_plus)) > threshold:
            print(cv2.countNonZero(TrackWebcam.diffImg(self,t_minus, t, t_plus)))
            if counter < 3:
              cv2.imwrite("{}motion.jpg".format(str(counter)), img)
              os.system("echo -e '\a'")
            counter += 1
          if cv2.countNonZero(TrackWebcam.diffImg(self,t_minus, t, t_plus)) < threshold:
            counter = 0
          # Read next image
          t_minus = t
          t = t_plus
          t_plus = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
          key = cv2.waitKey(10)
          if key == 27:
            cv2.destroyWindow(winName)
            sys.exit(0)
        except Exception as msg:
          print(self.FAIL + str(msg) + self.ENDC)
          cv2.destroyAllWindows()
          main()
    except Exception as msg:
      #index = self.old_urls.index(self.org)
      #del self.old_urls[index]
      cv2.destroyAllWindows()
      self.memory.append(self.ip_adress)
      TrackWebcam.giveme_url(self)

  def file_work(self):
    if os.path.isfile("ip_list.txt"):
      if os.stat("ip_list.txt") != 0:
        with open("ip_list.txt") as f:
          content = f.readlines()
        self.old_urls = [x.strip() for x in content]
        set(self.old_urls)
        self.trry = True
    else:
      dosya = open("ip_list.txt",'w')
      dosya.close()

  def giveme_url(self):
    self.ip_adress = input("GIVE URL> ")
    if self.ip_adress == 'q':
      sys.exit()
    if self.ip_adress == 'rescan':
      main()
    if len(self.ip_adress) < 11:
      print(self.FAIL + "URL MUST BE LONG THAN 11 CHARS" + self.ENDC)
      TrackWebcam.giveme_url(self)
    for x in range(len(self.memory)):
      #print(self.memory)
      if self.ip_adress in self.memory[x]:
        print(self.FAIL + "THIS ADRESS IS OLD! NOT WORKING" + self.ENDC)
        TrackWebcam.giveme_url(self)
    if self.error == True:
      dosya = open('ip_list.txt', 'a')
      print(self.ip_adress,file=dosya)
      dosya.close()
      TrackWebcam.capture(self)


  def try_url(self):
    try:
      print(self.HEADER + "TRYING URLS FROM IP LIST...." + self .ENDC)
      print("============================")
      if not self.old_urls:
        self.error = True
        TrackWebcam.giveme_url(self)
      for x in range(len(self.old_urls)):
        if self.old_urls[x] in self.memory:
          del self.old_urls[x]
        else:
          url = 'http://{}:8080/shot.jpg'.format(self.old_urls[x])
          print(url)
          self.memory.append(self.old_urls[x])
          openurl = urllib.request.urlopen(url)
          self.ip_adress = self.old_urls[x]
          TrackWebcam.capture(self)
    except Exception as msg:
      print(str(msg))
      for x in range(len(self.memory)):
        if self.old_urls:
          del self.old_urls[x]
          TrackWebcam.try_url(self)
      if not self.old_urls:
        self.error = True
        TrackWebcam.giveme_url(self)
def main():
  Track = TrackWebcam()
  print(Track.OKGREEN + "WELCOME TRACK IP WEBCAM PROGRAM" + Track.ENDC)
  print("===============================")
  try:
    if os.path.isfile("ip_list.txt"):
      if os.stat("ip_list.txt") == 0:
        #print("T1")
        Thread1 = threading.Thread(target=Track.giveme_url)
        Thread1.start()
        Thread1.join()
      else:
        if Track.trry == False:
          #print("T2")
          Thread2 = threading.Thread(target=Track.file_work)
          Thread2.start()
          Thread2.join()
      if Track.trry == True:
        #print("T4")
        Thread4 = threading.Thread(target=Track.try_url)
        Thread4.start()
        Thread4.join()
    else:
      #print("T3")
      Thread3 = threading.Thread(target=Track.file_work)
      Thread3.start()
      Thread3.join()
  except KeyboardInterrupt:
    sys.exit(0)

main()
