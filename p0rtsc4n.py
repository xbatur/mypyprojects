import socket,time,sys,subprocess

try:
    #subprocess.call('clear',shell=True)
    global host,s_port,open_ports
    if len(sys.argv) == 1:
        print("IP adressi girin")
        sys.exit()
    if len(sys.argv) == 2:
        host = sys.argv[1]
    if len(sys.argv) == 3:
        host = sys.argv[1]
        s_port = sys.argv[2]
    host_ip = socket.gethostbyname(host)
    if type(host) == str:
        print("BEFORE HOST: " + str(host))
        host = host_ip
        print("HOST IP: " + str(host_ip))
        print("NOW HOST: " + str(host))
    open_ports = []
except:
    if len(sys.argv) > 1:
        pass
    if len(sys.argv) < 1:
        print("Fill IP adress; ./p0rtsc4n.py IP")
        sys.exit()

def special_scan():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex((host,int(s_port)))
        if result == 0:
            print("Port open.")
        else:
            print("Port close.")
            sys.exit(0)
        sys.exit()
    except Exception as msg:
        print("Hata " + str(msg))
        sys.exit()


def scan():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if len(sys.argv) > 2:
            special_scan()
        if len(sys.argv) == 1:
            sys.exit()
        port = 0
        while port < 1105:
            result = s.connect_ex((host,int(port)))
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
            print("Acik port yok.")
            s.close()


    except KeyboardInterrupt:
        print("Exitting.")
        sys.exit(0)
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
    except socket.timeout:
        print("Connection timeout.")
        sys.exit()

scan()