import os,getpass,sys,time
from random import randint
from threading import Thread
class MemoryScanner():
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.PURPLE = '\033[35m'
        self.file_name = []
        self.killit = None
        self.file_size = []
        self.max_file_name = None
        self.getmaxbyte = None
        self.secondmaxbyte = None
        self.integer_list = []
        self.memory = None
        self.memory_free = None
        self.memory_space_check = False
    def ram_check(self):
        os.chdir("/proc/")
        file = open("meminfo","r")
        read = file.read()
        if(read.find("MemTotal") != -1):
            firstmem_val = read.find("MemTotal")
            secondmem_val = read.find("MemFree")
            rsize= read[firstmem_val:secondmem_val]
            rsize = rsize.split(" ")
            for x in range(len(rsize)):
                if rsize[x].isdigit():
                    self.memory = rsize[x]
            print(self.WARNING+"TOTAL MEMORY > "+self.ENDC+"{} BYTES".format(self.memory))
        if(read.find("MemAvailable") != -1):
            firstmemfree_val = read.find("MemFree")
            secondmemfree_val = read.find("MemAvailable")
            rsize = read[firstmemfree_val:secondmemfree_val]
            rsize = rsize.split(" ")
            for x in range(len(rsize)):
                if rsize[x].isdigit():
                    self.memory_free = rsize[x]
            print(self.WARNING+"FREE MEMORY > "+self.ENDC+"{} BYTES".format(self.memory_free))
    def critical_escape(self):
        MemoryScanner.scan_files(self)
        MemoryScanner.print_files(self)
        MemoryScanner.find_max(self)
        uname = getpass.getuser()
        os.chdir("/home/"+uname+"/Desktop/")
        self.killit = os.popen("pidof "+self.max_file_name).read()
        self.killit = self.killit[:-1]
        print(self.WARNING+"APPLICATION KILLING.."+self.ENDC)
        try:
            os.popen("kill "+self.killit)
            print(self.OKGREEN+self.BOLD+"[KILLED!]"+self.ENDC)
            file = open("log.txt", "w")
            file.write("KILLED APLLICATION LOG DETAILS: \n")
            file.write("APPLICATION NAME: " + self.max_file_name + "\n")
            file.write("BYTE " + self.getmaxbyte)
            file.close()
        except:
            print("GG! TOO HIGH FOR US..")
            print("SHUTDOWN!")
            file = open("log.txt","w")
            file.write("APPLICATION NAME: " + self.max_file_name + "\n")
            file.write("BYTE "+self.getmaxbyte)
            file.close()
            #os.popen("pkill -KILL -u root")
    def faultrandomizer(self):
        for x in randint(len(self.integer_list)):
            self.killit = os.popen("pidof " + str(x)).read()
            self.killit = self.killit[:-1]
            print(self.WARNING + self.killit + "APPLICATION KILLING.." + self.ENDC)
    def dangerous_check(self):
        print(self.WARNING+"STATUS> "+self.ENDC, end="")
        for x in range(0, 3):
            print(".",end="",flush=True)
            time.sleep(0.3)
        if (int(self.memory))/2 > int(self.memory_free):
            os.system("echo 'echo 3 > /proc/sys/vm/drop_caches' > /dev/null")
            print(self.OKBLUE+"NORMAL"+self.ENDC)
        if (int(self.memory))/4 > int(self.memory_free):
            print(self.FAIL+"CRITICAL!"+self.ENDC)
            try:
                MemoryScanner.critical_escape(self)
            except Exception:
                print(self.FAIL + "[FAILED] " + self.BOLD + "MEMORY FREE SPACE CHECK!" + self.ENDC)
            MemoryScanner.ram_check(self)
            if (int(self.memory)) / 6 > int(self.memory_free):
                MemoryScanner.faultrandomizer(self)
        if (int(self.memory) - int(self.memory_free) > 100000):
            print(self.BOLD+"BUT "+self.WARNING+"NOW "+self.ENDC+self.BOLD+"NOT IN FATAL LEVEL!"+self.ENDC)
        print(self.OKGREEN+"[PASSED] "+self.ENDC+self.PURPLE+"MEMORY FREE SPACE CHECK!"+self.ENDC)
        self.memory_space_check = True

    def scan_files(self):
        os.chdir("/proc/")
        file_list = os.listdir('.')
        for c in range(len(file_list)):
            if (file_list[c].isdigit()):
                os.chdir("/proc/"+file_list[c])
                file = open("status","r")
                read = file.read()
                #print(read.find("VmSize"))
                if (read.find("Umask")):
                    firstname_val = 6
                    secondname_val = read.find("Umask")
                    name = read[firstname_val:secondname_val]
                    self.file_name.append(name)
                if (read.find("VmSize") == -1):
                    self.file_size.append("-1")
                if (read.find("VmSize") != -1):
                    firstsize_val = read.find("VmSize")
                    secondsize_val = read.find("VmLck")
                    rsize = read[firstsize_val:secondsize_val]
                    rsize = rsize.split(" ")
                    for x in range(len(rsize)):
                        if rsize[x].isdigit():
                            vmsize = rsize[x]
                            self.file_size.append(vmsize)
    def find_max(self):
        os.chdir("/proc/")
        file_list = os.listdir('.')
        for c in range(len(file_list)):
            if (file_list[c].isdigit()):
                os.chdir("/proc/" + file_list[c])
                file = open("status", "r")
                read = file.read()
                if (read.find(self.getmaxbyte) != -1):
                    if (read.find("Umask")):
                        firstname_val = 6
                        secondname_val = read.find("Umask")
                        self.max_file_name = read[firstname_val:secondname_val]
                        if (self.max_file_name == "python"):
                            #randomizer guardian blocking
                            for x in randint(len(self.integer_list)):
                                self.getmaxbyte = x
                                MemoryScanner.find_max(self)
        print(self.WARNING+"DETECTED USING OF MAXIMUM MEMORY PROGRAM FILE NAME : "+self.ENDC+self.BOLD+self.PURPLE+"{} ".format(self.max_file_name),end="")
        print(self.WARNING+"USING SIZE: "+self.ENDC+"{}".format(self.getmaxbyte))
    def print_files(self):
        for c in range(len(self.file_name)):
            pass
            # print("NAME OF FILE {1}: {0}".format(self.file_name[c],c))
        for v in range(len(self.file_size)):
            if (self.file_size[v] != "-1"):
                #print("BYTES OF FILE {1}: {0} KB".format(self.file_size[v],v))
                self.integer_list.append(int(self.file_size[v]))
        self.getmaxbyte = str(max(self.integer_list))
        print("MAX VALUE OF BYTES: {}".format(self.getmaxbyte))


def main():
    scan = MemoryScanner()
    maindir = os.getcwd()
    file = open("exitlog.txt", 'w')
    file.close()
    file = open("log.txt", 'w')
    file.close()
    while (True):
        try:
            time.sleep(1)
            T1 = Thread(target=scan.scan_files())
            T2 = Thread(target=scan.print_files())
            T3 = Thread(target=scan.find_max)
            T4 = Thread(target=scan.ram_check())
            T5 = Thread(target=scan.dangerous_check())
            T1.start()
            T1.join()
            T2.start()
            T2.join()
            T3.start()
            T3.join()
            T4.start()
            T4.join()
            T5.start()
            T5.join()
        except KeyboardInterrupt:
            print(scan.OKGREEN+"WRITING LOGS",end="",flush=True)
            os.chdir(maindir)
            file = open("exitlog.txt",'w')
            file.write("DATE: "+str(time.ctime())+"\n")
            if scan.max_file_name != None:
                file.write("APPLICATION NAME: "+scan.max_file_name+"\n")
                killit = os.popen("pidof " + scan.max_file_name).read()
                killit = killit[:-1]
                file.write("PROCESS ID: " + killit + "\n")
            else:
                file.write("APPLICATION NAME: NULL \n")
            if scan.getmaxbyte != None:
                file.write("BYTE: "+scan.getmaxbyte+"\n")
            else:
                file.write("BYTE: NULL \n")
            file.close()
            for x in range(0,4):
                time.sleep(0.1)
                print(".",end="")
            print(scan.ENDC+scan.OKGREEN+scan.BOLD+"[COMPLETED!]"+scan.ENDC)
            sys.exit(0)
main()
