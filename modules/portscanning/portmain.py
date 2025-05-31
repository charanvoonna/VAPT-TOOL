import argparse
from Tcpconnectscanner_fixed import TCPConnectScanner
from syn_scan import SynPortScanner
from slow_timing_scanner import PortScanner
from decoy_scan import DecoyScanner

def parse_ports(port_str):
    ports = set()
    parts = port_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def main():
    parser = argparse.ArgumentParser(description="Main VAPT Scanner",usage="python main.py <method> <target> -p <ports> [--threads N] [--delay N] [--decoys N] [--timeout N]")
    parser.add_argument("method", nargs="?", choices=["tcp", "syn", "slow", "decoy"], help="Scan technique")
    parser.add_argument("target", nargs="?", help="Target IP address")
    parser.add_argument("-p", "--ports", required=True, help="Ports to scan (e.g. 22,80,443 or 20-25)")
    parser.add_argument("--threads", type=int, default=10, help="Max threads (default: 10)")
    parser.add_argument("--delay", type=int, default=0, help="Delay in seconds (for slow scan)")
    parser.add_argument("--decoys", type=int, default=5, help="Number of decoy IPs")
    parser.add_argument("--timeout", type=int, default=1, help="Connection timeout (for decoy only)")

    args = parser.parse_args()
    ports = parse_ports(args.ports)

    if args.method == "tcp":
        scanner = TCPConnectScanner(args.target, ports)
        scanner.run(max_threads=args.threads)

    elif args.method == "syn":
        scanner = SynPortScanner(args.target, ports)
        scanner.scan()

    elif args.method == "slow":
        scanner = PortScanner(args.target, ports, args.delay)
        scanner.start_scan(max_threads=args.threads)

    elif args.method == "decoy":
        scanner = DecoyScanner(args.target, ports, args.decoys, args.timeout)
        scanner.start_scan()

if __name__ == "__main__":
    main()
