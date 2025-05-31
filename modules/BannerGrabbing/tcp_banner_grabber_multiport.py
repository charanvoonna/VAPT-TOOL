import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
import argparse

class BannerGrabber:
    def __init__(self, targets, ports, timeout=3, max_threads=10):
        self.targets = targets
        self.ports = ports
        self.timeout = timeout
        self.max_threads = max_threads

    def banner_grab(self, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((host, port))
                banner = s.recv(1024).decode('utf-8', errors='ignore')
                print(f"{Fore.GREEN}[+] {host}:{port} - {banner.strip()}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] {host}:{port} - {e}{Style.RESET_ALL}")

    def run(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for host in self.targets:
                for port in self.ports:
                    executor.submit(self.banner_grab, host, port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Banner Grabbing Tool")
    parser.add_argument("targets", nargs='+', help="List of IP addresses or hostnames to scan")
    parser.add_argument("-p", "--port", type=int, nargs='+', required=True, help="One or more ports to scan")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Timeout in seconds (default: 3)")
    parser.add_argument("-mt", "--max_threads", type=int, default=10, help="Maximum number of threads (default: 10)")
    args = parser.parse_args()

    scanner = BannerGrabber(args.targets, args.port, args.timeout, args.max_threads)
    scanner.run()
