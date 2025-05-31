
import argparse
from scapy.all import IP, TCP, sr1, send
from colorama import init, Fore

init(autoreset=True)

class SynPortScanner:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports

    def scan(self):
        print(Fore.CYAN + f"\n[*] Starting SYN Scan on {self.target}\n")
        try:
            for port in self.ports:
                pkt = IP(dst=self.target)/TCP(dport=port, flags="S")
                response = sr1(pkt, timeout=1, verbose=0)

                if response and response.haslayer(TCP):
                    tcp_layer = response.getlayer(TCP)
                    if tcp_layer.flags == 0x12:
                        print(Fore.GREEN + f"[+] Port {port} is OPEN")
                        send(IP(dst=self.target)/TCP(dport=port, flags="R"), verbose=0)
                    elif tcp_layer.flags == 0x14:
                        print(Fore.RED + f"[-] Port {port} is CLOSED")
                else:
                    print(Fore.YELLOW + f"[!] Port {port} is FILTERED or DROPPED")
        except KeyboardInterrupt:
            print(Fore.MAGENTA + "\n[!] Scan interrupted by user. Exiting...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SYN Port Scanner using Scapy")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("ports", help="Comma-separated ports (e.g., 22,80,443)")
    args = parser.parse_args()

    target = args.target
    ports = [int(p.strip()) for p in args.ports.split(",")]

    scanner = SynPortScanner(target, ports)
    scanner.scan()
