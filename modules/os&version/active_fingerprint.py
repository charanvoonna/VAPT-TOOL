import socket
import argparse
import threading
from queue import Queue
from colorama import Fore, init

init(autoreset=True)

class ActiveFingerprint:
    def __init__(self, target, ports, max_threads=10):
        self.target = target
        self.ports = ports
        self.max_threads = min(max_threads, 10)
        self.queue = Queue()
        self.lock = threading.Lock()

    def send_tcp_probe(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((self.target, port))

            ttl = s.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
            window_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

            os_guess = self.analyze_response(ttl, window_size)

            with self.lock:
                print(f"{Fore.GREEN}[TraceNet] Port {port} → TTL: {ttl}, Window: {window_size}, OS: {os_guess}")

            s.close()

        except socket.timeout:
            with self.lock:
                print(f"{Fore.YELLOW}[TraceNet] Port {port} → Timeout")

        except Exception as e:
            with self.lock:
                print(f"{Fore.RED}[TraceNet] Port {port} → Error: {e}")

    def analyze_response(self, ttl, window_size):
        if ttl >= 128:
            if window_size in [8192, 65535]:
                return "Windows"
        elif ttl >= 64:
            if window_size in [5840, 14600]:
                return "Linux"
        elif ttl >= 255:
            return "Cisco/Unix"
        return "Unknown"

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            self.send_tcp_probe(port)
            self.queue.task_done()

    def run(self):
        print(f"{Fore.MAGENTA}[TraceNet] Starting Active OS Fingerprinting on {self.target}...\n")

        for port in self.ports:
            self.queue.put(port)

        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        self.queue.join()

        for t in threads:
            t.join()

        print(f"\n{Fore.MAGENTA}[TraceNet] Fingerprinting Completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TraceNet Active OS Fingerprinting")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--ports", required=False, default="80,443", help="Comma-separated list of ports")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (max 10)")

    args = parser.parse_args()
    ports = [int(p.strip()) for p in args.ports.split(",")]

    tracer = ActiveFingerprint(args.target, ports, args.threads)
    tracer.run()
