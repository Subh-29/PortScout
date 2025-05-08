import socket

from concurrent.futures import ThreadPoolExecutor as TPE

target = input("Enter target IP or Domain Name: ")
ports = 30

def scanPort(port, target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            print(f"[+] Port {port} is OPEN")
        # else:
        #     print(f"[-] Port {port} is CLOSED!")
        s.close()
    except KeyboardInterrupt:
        pass

with TPE(max_workers=300) as executor:
    for port in range(1, 1024):
        executor.submit(scanPort, port, target)