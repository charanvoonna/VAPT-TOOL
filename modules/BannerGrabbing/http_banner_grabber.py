import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

class HTTPBannerGrabber:
    def __init__(self, targets, port, threads):
        self.targets = targets
        self.port = port
        self.threads = min(threads, 10)

    def grab_banner(self, target):
        try:
            url = f"http://{target}:{self.port}"
            response = requests.get(url, timeout=5)
            print(f"{Fore.GREEN}[+] Banner for {target}:{self.port}{Style.RESET_ALL}")
            for header, value in response.headers.items():
                print(f"{Fore.CYAN}{header}: {value}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to grab banner from {target}:{self.port} - {e}{Style.RESET_ALL}")

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.grab_banner, self.targets)

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP Header Banner Grabbing using TraceNet")
    parser.add_argument("targets", nargs="+", help="List of target IPs or domains")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port to connect to (default: 80)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (default: 5, max: 10)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    grabber = HTTPBannerGrabber(args.targets, args.port, args.threads)
    grabber.run()
