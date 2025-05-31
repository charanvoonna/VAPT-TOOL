import argparse
from scapy.all import IP, TCP, send, fragment as scapy_fragment, RandShort
from colorama import Fore, Style, init

init(autoreset=True)

class FragmentedBannerGrabber:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port

    def send_fragments(self):
        ip = IP(dst=self.target_ip)
        tcp = TCP(dport=self.target_port, sport=RandShort(), flags='S', seq=1000)
        pkt = ip / tcp

        # Use scapy's fragment() function safely
        fragments = scapy_fragment(pkt, fragsize=8)

        for frag in fragments:
            send(frag, verbose=0)

        print(f"{Fore.GREEN}[+] Fragmented SYN packet sent to {self.target_ip}:{self.target_port}")
        print(f"{Fore.YELLOW}[!] Note: This is stealth, you won't receive banners directly.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fragmented Packet Banner Grabber")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target port")

    args = parser.parse_args()
    grabber = FragmentedBannerGrabber(args.target, args.port)
    grabber.send_fragments()
