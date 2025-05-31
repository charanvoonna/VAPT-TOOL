import socket
import socks
import argparse
from colorama import init, Fore
from threading import Thread

init(autoreset=True)

class ProxyBannerGrabber:
    def __init__(self, target_ip, target_port, proxy_ip, proxy_port, proxy_type):
        self.target_ip = target_ip
        self.target_port = target_port
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.proxy_type = proxy_type.lower()
        self.banner = None

    def grab_banner(self):
        try:
            if self.proxy_type == 'socks4':
                proxy_type = socks.SOCKS4
            elif self.proxy_type == 'socks5':
                proxy_type = socks.SOCKS5
            elif self.proxy_type == 'http':
                proxy_type = socks.HTTP
            else:
                print(Fore.RED + "[!] Invalid proxy type")
                return

            sock = socks.socksocket()
            sock.set_proxy(proxy_type, self.proxy_ip, self.proxy_port)
            sock.settimeout(5)
            sock.connect((self.target_ip, self.target_port))
            
            # Send simple HTTP GET request to try grabbing banner (adjust if needed)
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            data = sock.recv(4096)
            self.banner = data.decode(errors='ignore')
            print(Fore.GREEN + f"[+] Banner grabbed from {self.target_ip}:{self.target_port} via proxy {self.proxy_ip}:{self.proxy_port}")
            print(Fore.CYAN + self.banner)
            sock.close()

        except Exception as e:
            print(Fore.RED + f"[!] Failed to grab banner: {e}")
import argparse

def main():
    parser = argparse.ArgumentParser(description="Proxy Banner Grabber")
    parser.add_argument('-t', '--target', required=True, help='Target IP or domain')
    parser.add_argument('-p', '--port', type=int, required=True, help='Target port')
    parser.add_argument('-x', '--proxy_ip', required=True, help='Proxy IP address')
    parser.add_argument('-q', '--proxy_port', type=int, required=True, help='Proxy port')
    parser.add_argument('-y', '--proxy_type', choices=['socks4', 'socks5', 'http'], required=True, help='Proxy type')
    args = parser.parse_args()
    
    print(f"Target: {args.target}")
    print(f"Port: {args.port}")
    print(f"Proxy IP: {args.proxy_ip}")
    print(f"Proxy Port: {args.proxy_port}")
    print(f"Proxy Type: {args.proxy_type}")

    grabber = ProxyBannerGrabber(
        args.target, args.port,
        args.proxy_ip, args.proxy_port,
        args.proxy_type
    )
    grabber.grab_banner()

if __name__ == "__main__":
    main()

