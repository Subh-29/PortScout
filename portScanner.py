import socket
import ssl

from concurrent.futures import ThreadPoolExecutor as TPE

target = input("Enter target IP or Domain Name: ")
ports = 30

def grabSSLBanner(target):
    context = ssl.create_default_context()
    with socket.create_connection((target, 443)) as sock:
        with context.wrap_socket(sock=sock, server_hostname=target) as ssock:
            certificate = ssock.getpeercert()
            cert = ssock.getpeername()
            print(f"   └─>SSL/TLS Version: {ssock.version()}\n")
            print(f"   └─>Certificate Subject: {certificate['subject']}\n")
            print(f"   └─>IP: {cert[0]}\n")

def scanPort(port, target):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            print(f"[+] Port {port} is OPEN\n")
        # else:
        #     print(f"[-] Port {port} is CLOSED!")
        try:
            if port == 80:
                s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            if port == 443:
                grabSSLBanner(target=target)
            try:
                banner = s.recv(1024)
                print(f"====> Banner on Port {port} : {banner.decode(errors='ignore').strip()}\n")
            except:
                pass
        except:
            print(f"Banner Grabbing failed at Port {port}\n")
        s.close()
    except KeyboardInterrupt:
        pass

with TPE(max_workers=300) as executor:
    for port in range(1, 1024):
        executor.submit(scanPort, port, target)