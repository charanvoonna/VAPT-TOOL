import argparse
import socket
import threading
from colorama import Fore, Style
from random import randint

class DecoyScanner:
    def __init__(self, target, ports, decoys, timeout):
        self.target = target
        self.ports = ports
        self.decoys = decoys
        self.timeout = timeout
        self.lock = threading.Semaphore(10)  
        self.open_ports = []

    def scan_port(self, port):
        with self.lock:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
                    self.open_ports.append(port)
                else:
                    print(f"{Fore.RED}[-] port {port} is CLOSED{Style.RESET_ALL}") 
                sock.close()
            except Exception as e:
                print(f"{Fore.RED}[!] Error on port {port}: {e}{Style.RESET_ALL}")

    def spoof_ip(self):
        return ".".join(str(randint(1, 254)) for _ in range(4))

    def start_scan(self):
        print(f"{Fore.CYAN}[*] Starting Decoy Scan on {self.target} with {self.decoys} decoys{Style.RESET_ALL}")
        threads = []
        for port in self.ports:
            for _ in range(self.decoys):
                fake_ip = self.spoof_ip()
                print(f"{Fore.YELLOW}[*] Sending decoy from {fake_ip} to port {port}{Style.RESET_ALL}")
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

            if not self.open_ports:
                print(f"{Fore.MAGENTA}[!] No ports are open on {self.target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Decoy Scan complete!{Style.RESET_ALL}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Decoy Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("-p", "--ports", nargs="+", type=int, required=True, help="Ports to scan")
    parser.add_argument("-d", "--decoys", type=int, default=5, help="Number of decoy IPs")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for each connection")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    scanner = DecoyScanner(args.target, args.ports, args.decoys, args.timeout)
    scanner.start_scan()
