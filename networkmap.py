import socket,time,sys
global addr,addaddr,spec_lan_addr,port_scan
addr = '192.168.1'
adresses = []
ip_adresses = []
ip = ""
addaddr = []
open_ports = []
closed_ports = []
spec_lan = ""
spec_lan_from = False
port_scan = False
port_scan_spec = False
def add():
    for x in range(0,1000):
        addaddr.append(x)
    run_lan()

def run_lan():
    for c in range(0,len(addaddr)):
        try:
            addr = '192.168.1.'+str(addaddr[c])
            hostname = socket.gethostbyaddr(addr)
            if hostname[0] != addr:
                print("Hostname is: {}".format(hostname[0]) + " IP is: {}".format(addr))
                if hostname[0] in adresses:
                    pass
                else:
                    adresses.append(hostname[0])
                    ip_adresses.append(addr)
            #time.sleep(1)
            if c > 19 and spec_lan_from == True:
                #spec_lan_from = False
                select_specific_lan()
            if c > 19 and port_scan == True:
                #port_scan = False
                port_scan_all()
            if c > 20 and hostname[0] == addr:
                print("=====Scan is done.=====")
                break
        except Exception:
            continue

def select_specific_lan():
    if not adresses:
        print("You must scan LAN adresses!")
        spec_lan_from = True
        add()
    for x in range(len(adresses)):
        print("Adress {}: ".format(x) + adresses[x])
    get_input = input("Select specific lan > ")
    spec_lan = adresses[(int(get_input))]
    index = adresses.index(spec_lan)
    global ip
    ip = ip_adresses[index]
    spec_lan_port()
def spec_lan_port():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        port = 0
        print(ip)
        while port < 1105:
            result = s.connect_ex((ip, int(port)))
            if result == 0:
                open_ports.append(port)
                #s.close()
            port += 1
        if open_ports:
            print("Acik portlar > " + str(open_ports))
        if not open_ports:
            print("Acik port yok.")
            s.close()
        for c in range(len(open_ports)):
            del open_ports[c]
    except Exception as msg:
        print("Hata "+ str(msg))
def lan_portcheck():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        port = 0
        while port < 1105:
            result = s.connect_ex((adresses[0], int(port)))
            # print(str(result))
            if result == 0:
                print("Port: {}".format(port))
                open_ports.append(port)
                s.close()
            port += 1
        if open_ports:
            print("Acik portlar > " + str(open_ports))
            s.close()
        if not open_ports:
            print(open_ports)
            print("Acik port yok.")
            s.close()
    except:
        pass

def port_scan_all():
    if not adresses:
        print("You must scan LAN adresses!")
        port_scan = True
        add()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    port = 0
    for c in ip_adresses:
        print(c)
        port = 0
        while port < 1105:
            result = s.connect_ex((c, int(port)))
            #print(str(result))
            if result == 0:
                print("Port: {}".format(port))
                open_ports.append(port)
                s.close()
            port += 1
        if open_ports:
            print("Acik portlar > " + str(open_ports))
        if not open_ports:
            print(open_ports)
            s.close()

def main():
    print("Welcome our scanner program.")
    print("This is not about us, about you.")
    print("What is your choice?")
    print("1 - LAN IP adresses scan")
    print("2 - LAN IP adresses port scan")
    print("3 - Port scan")
    print("3 - Port scan from specific adress")
    print("Type help for show again this information.")
    while True:
        try:
            get_input = input("What is your choice? > ")
            if get_input.lower() == 'help':
                print("Welcome our scanner program.")
                print("This is not about us, about you.")
                print("What is your choice?")
                print("1 - LAN IP adresses scan")
                print("2 - LAN IP adresses port scan")
                print("3 - Port scan")
                print("Type help for show again this information.")
            if get_input == '1':
                if not addaddr:
                    add()
                run_lan()
            if get_input == '2':
                select_specific_lan()
            if get_input == '3':
                port_scan_all()
            if get_input.lower() == 'q':
                print("Good bye.")
                sys.exit(0)
        except KeyboardInterrupt:
            print("\bGood bye.")
            sys.exit()
main()