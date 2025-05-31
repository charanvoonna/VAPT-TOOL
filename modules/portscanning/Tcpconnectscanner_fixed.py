
import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import argparse

init(autoreset=True)

class TCPConnectScanner:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports

    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
            if result == 0:
                print(f"{Fore.GREEN}[+] Port {port} is open")
            else:
                print(f"{Fore.RED}[-] Port {port} is closed")
            s.close()
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error scanning port {port}: {e}")

    def run(self, max_threads=10):
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(self.scan_port, self.ports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Connect Port Scanner")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Start port number")
    parser.add_argument("end_port", type=int, help="End port number")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    port_range = range(args.start_port, args.end_port + 1)
    scanner = TCPConnectScanner(args.target, port_range)
    scanner.run(max_threads=args.threads)
