# Import required modules
import socket                          # For creating network connections
import ssl                             # For SSL/TLS certificate grabbing
from colorama import Fore              # For colored terminal output
import json                            # For exporting scan results to JSON
from datetime import datetime          # For generating timestamped filenames
from concurrent.futures import ThreadPoolExecutor as TPE  # For multithreading

results = []  # To store scan results (open ports, banners, cert info)

# Take target input (IP address or domain)
target = input("Enter target IP or Domain Name: ")

# Maximum port number to scan (1 to 1024 in this case)
ports = 30  # (NOTE: This variable isn’t used, but can be expanded later)

# Function to grab SSL/TLS certificate details on port 443
def grabSSLBanner(target):
    context = ssl.create_default_context()
    with socket.create_connection((target, 443)) as sock:
        with context.wrap_socket(sock=sock, server_hostname=target) as ssock:
            certificate = ssock.getpeercert()
            cert = ssock.getpeername()

            # Print certificate and SSL info
            print(f"{Fore.LIGHTCYAN_EX}   └─>SSL/TLS Version: {ssock.version()}\n")
            print(f"{Fore.CYAN}   └─>Certificate Subject: {certificate['subject']}\n")
            print(f"{Fore.LIGHTCYAN_EX}   └─>IP: {cert[0]}\n")

            # Append this info to results for export
            results.append({
                "port": 443,
                "status": "open",
                "banner": [certificate['subject'], cert] if certificate['subject'] else "",
            })

# Function to scan a single port
def scanPort(port, target):
    try:
        # Create socket and set timeout
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        # Try connecting to the port
        result = s.connect_ex((target, port))

        # If port is open
        if result == 0:
            print(f"{Fore.BLUE} [+] Port {port} is OPEN\n")

            # Attempt to grab banner
            try:
                if port == 80:
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")  # Send simple HTTP request

                if port == 443:
                    grabSSLBanner(target=target)  # Use SSL banner grabbing on 443

                try:
                    banner = s.recv(1024)
                    print(f"{Fore.LIGHTGREEN_EX} ====> Banner on Port {port} : {banner.decode(errors='ignore').strip()}\n")
                except:
                    pass  # Failed to receive banner

            except:
                print(f"{Fore.RED} [-] Banner Grabbing failed at Port {port}\n")

            # Save successful result
            results.append({
                "port": port,
                "status": "open",
                "banner": banner.decode(errors='ignore').strip() if banner else "",
            })

        s.close()

    # Handle various exceptions
    except KeyboardInterrupt:
        return -1
    except socket.timeout:
        print(f"{Fore.YELLOW}[!] Connection Timeout")
        return -1
    except socket.gaierror:
        print(f"{Fore.RED}[-] Hostname could not be resolved")
        return -1
    except socket.error:
        print(f"{Fore.RED}[!] Couldn't connect to server")
        return -1

    return 1  # Scan successful

# Use ThreadPoolExecutor for multithreaded scanning (300 threads)
with TPE(max_workers=300) as executor:
    for port in range(1, 1024):  # Scan ports 1–1023
        flag = executor.submit(scanPort, port, target)
        if flag == -1:
            break  # Exit on user interrupt or error

# Ask user how to save results
out_format = input("Save results as (json/txt)? ").lower()
filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Save to JSON
if out_format == "json":
    with open(f"{filename}.json", "w") as f:
        json.dump(results, f, indent=4)
    print(f"{Fore.MAGENTA}[✔] Results saved to {filename}.json")

# Save to TXT
elif out_format == "txt":
    with open(f"{filename}.txt", "w") as f:
        for entry in results:
            f.write(f"Port {entry['port']} is OPEN\n")
            if entry['banner']:
                f.write(f"    Banner: {entry['banner']}\n")
    print(f"{Fore.MAGENTA}[✔] Results saved to {filename}.txt")

# Handle invalid option
else:
    print(f"{Fore.RED}[x] Invalid format. Nothing saved.")
