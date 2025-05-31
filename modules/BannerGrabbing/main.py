import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
import sys

# Import your existing classes from their files (make sure these files are in the same folder or python path)
from banner_grabber import BannerGrabber
from proxy_banner_grabber import ProxyBannerGrabber
from fragmented_banner_grabber import FragmentedBannerGrabber
from http_banner_grabber import HTTPBannerGrabber

init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description="TraceNet Banner Grabbing Tool - Main Launcher")
    
    subparsers = parser.add_subparsers(dest='technique', help='Choose a banner grabbing technique')

    # 1. Simple TCP Banner Grabber
    parser_tcp = subparsers.add_parser('tcp', help='Simple TCP Banner Grabber')
    parser_tcp.add_argument('targets', nargs='+', help='Target IP(s) or hostname(s)')
    parser_tcp.add_argument('-p', '--ports', type=int, nargs='+', required=True, help='Port(s) to scan')
    parser_tcp.add_argument('-t', '--timeout', type=int, default=3, help='Timeout in seconds')
    parser_tcp.add_argument('-mt', '--max_threads', type=int, default=10, help='Max threads')

    # 2. Proxy Banner Grabber
    parser_proxy = subparsers.add_parser('proxy', help='Proxy Banner Grabber')
    parser_proxy.add_argument('-t', '--target', required=True, help='Target IP or domain')
    parser_proxy.add_argument('-p', '--port', type=int, required=True, help='Target port')
    parser_proxy.add_argument('-x', '--proxy_ip', required=True, help='Proxy IP address')
    parser_proxy.add_argument('-q', '--proxy_port', type=int, required=True, help='Proxy port')
    parser_proxy.add_argument('-y', '--proxy_type', choices=['socks4', 'socks5', 'http'], required=True, help='Proxy type')

    # 3. Fragmented Packet Banner Grabber
    parser_frag = subparsers.add_parser('fragmented', help='Fragmented Packet Banner Grabber')
    parser_frag.add_argument('-t', '--target', required=True, help='Target IP address')
    parser_frag.add_argument('-p', '--port', type=int, required=True, help='Target port')

    # 4. HTTP Header Banner Grabber
    parser_http = subparsers.add_parser('http', help='HTTP Header Banner Grabber')
    parser_http.add_argument('targets', nargs='+', help='Target IP(s) or domain(s)')
    parser_http.add_argument('-p', '--port', type=int, default=80, help='Port (default 80)')
    parser_http.add_argument('-t', '--threads', type=int, default=5, help='Number of threads (max 10)')

    args = parser.parse_args()

    if args.technique == 'tcp':
        scanner = BannerGrabber(args.targets, args.ports, args.timeout, args.max_threads)
        scanner.run()

    elif args.technique == 'proxy':
        grabber = ProxyBannerGrabber(args.target, args.port, args.proxy_ip, args.proxy_port, args.proxy_type)
        grabber.grab_banner()

    elif args.technique == 'fragmented':
        grabber = FragmentedBannerGrabber(args.target, args.port)
        grabber.send_fragments()

    elif args.technique == 'http':
        grabber = HTTPBannerGrabber(args.targets, args.port, args.threads)
        grabber.run()

    else:
        print(Fore.RED + "[-] No valid technique selected. Use -h for help." + Style.RESET_ALL)
        sys.exit(1)


if __name__ == "__main__":
    main()
