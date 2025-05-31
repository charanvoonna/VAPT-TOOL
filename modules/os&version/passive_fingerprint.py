from scapy.all import sniff, IP, TCP, get_if_list  
from colorama import Fore, init
import argparse
import threading

init(autoreset=True)

class PassiveFingerprint:
    def __init__(self, interface=None, packet_count=100):
    
        if interface is None:
            self.interface = get_if_list()[0]  
        else:
            self.interface = interface
        self.packet_count = packet_count
        self.lock = threading.Lock()

    def analyze_packet(self, packet):
        
        print(Fore.YELLOW + "[TraceNet] Packet captured...")  

        if IP in packet and TCP in packet and packet[TCP].flags & 0x02:
            ip_layer = packet[IP]
            tcp_layer = packet[TCP]

            src_ip = ip_layer.src
            ttl = ip_layer.ttl
            window = tcp_layer.window

            os_guess = self.guess_os(ttl, window)

            with self.lock:
                print(f"{Fore.GREEN}[TraceNet] From {src_ip} → TTL: {ttl}, Window: {window}, OS Guess: {os_guess}")

    def guess_os(self, ttl, window_size):
        
        if ttl >= 128:
            if window_size in [8192, 65535]:
                return "Windows"
        elif ttl >= 64:
            if window_size in [5840, 14600]:
                return "Linux"
        elif ttl >= 255:
            return "Cisco/Unix"
        return "Unknown"

    def start_sniffing(self):
        print(f"{Fore.MAGENTA}[TraceNet] Passive OS Fingerprinting started on interface '{self.interface}'...\n")

        try:
            sniff(
                filter="tcp",
                iface=self.interface,
                prn=self.analyze_packet,
                store=False,
                count=self.packet_count
            )
        except Exception as e:
            print(Fore.RED + f"[TraceNet] ERROR: {e}")

        print(f"\n{Fore.MAGENTA}[TraceNet] Passive OS Fingerprinting completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TraceNet Passive OS Fingerprinting")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on (e.g., 'Wi-Fi', 'Ethernet')")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of packets to capture (default 100)")

    args = parser.parse_args()

    
    print(Fore.CYAN + "[TraceNet] Available Interfaces:")
    for i in get_if_list():
        print(Fore.CYAN + f" - {i}")

    sniffer = PassiveFingerprint(args.interface, args.count)
    sniffer.start_sniffing()
