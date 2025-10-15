import socket
from concurrent.futures import ThreadPoolExecutor
import ssl
import threading
import socketserver
import select


# ------------------ PORT SCANNER ------------------
class Port_scanner:
    PROXIES = [
    {"type": "http",  "addr": "127.0.0.1", "port": 8000},   # local HTTP proxy (proxy.py example)
    {"type": "http",  "addr": "127.0.0.1", "port": 8001},
    {"type": "http",  "addr": "127.0.0.1", "port": 8002},
    {"type": "socks5", "addr": "127.0.0.1", "port": 1080},  # local SOCKS5 (ssh -D)
    {"type": "socks4", "addr": "127.0.0.1", "port": 1081},  # local SOCKS4 (microsocks/dante)
      ]
 # safe default

    def __init__(self, host, port, timeout, proxy=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.proxy = proxy  # optional, for future proxy support

    def chunk_ports(self, chunk_size):
        for i in range(0, len(self.port), chunk_size):
            yield self.port[i : i + chunk_size]

    def scan(self, p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.gethostbyname(self.host)  # Validate host
            s.settimeout(self.timeout)
            result = s.connect_ex((self.host, p))

            if result != 0:
                print(
                    f"Connect not possible for port {p}, maybe filtered or closed by firewall"
                )
                print(f"Error: {result}")
            else:
                print(f"Connection Established on Port {p}")
                # Banner grabbing
                try:
                    if p == 80:
                        req = (
                            f"GET / HTTP/1.1\r\nHost:{self.host}\r\n"
                            "User-Agent: SimpleScanner/1.0\r\nConnection: close\r\n\r\n"
                        )
                        s.send(req.encode())
                        banner = s.recv(2048).decode(errors="ignore")
                        print(f"HTTP Banner from port {p}:\n{banner.strip()}")
                    elif p == 443:
                        s.close()
                        context = ssl.create_default_context()
                        ssl_sock = context.wrap_socket(
                            socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                            server_hostname=self.host,
                        )
                        ssl_sock.settimeout(self.timeout)
                        ssl_sock.connect((self.host, p))
                        req = (
                            f"GET / HTTP/1.1\r\nHost:{self.host}\r\n"
                            "User-Agent: SimpleScanner/1.0\r\nConnection: close\r\n\r\n"
                        )
                        ssl_sock.send(req.encode())
                        banner = ssl_sock.recv(2048).decode(errors="ignore")
                        print(f"HTTPS Banner from port {p}:\n{banner.strip()}")
                        ssl_sock.close()
                    elif p == 21:
                        banner = s.recv(2048).decode(errors="ignore")
                        print(f"FTP Banner from port {p}:\n{banner.strip()}")
                    elif p == 22:
                        banner = s.recv(2048).decode(errors="ignore")
                        print(f"SSH Banner from port {p}:\n{banner.strip()}")
                    else:
                        s.send(b"\r\n")
                        banner = s.recv(1024).decode(errors="ignore").strip()
                        print(f"Banner from port {p}: {banner if banner else 'None'}")
                except Exception:
                    print(f"Port {p} open, but no banner grabbed")
        except Exception as e:
            print(f"Unknown error on Port {p}: {e}")
        finally:
            try:
                s.close()
            except:
                pass

    def scan_chunk(self, chunk):
        for p in chunk:
            self.scan(p)

    def run(self, chunk_size=5, max_workers=4):
        port_chunks = list(self.chunk_ports(chunk_size))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.scan_chunk, port_chunks)
        print("All ports are scanned!")


# ------------------ PROXY MAKER ------------------
class _ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class _SimpleProxyHandler(socketserver.BaseRequestHandler):
    BUFSIZE = 8192

    def handle(self):
        try:
            data = self._recv_headers()
            if not data:
                return
            first = data.split(b"\r\n", 1)[0].decode(errors="ignore")
            parts = first.split()
            if len(parts) < 2:
                return
            method, target = parts[0].upper(), parts[1]
            if method == "CONNECT":
                if ":" not in target:
                    return
                host, port = target.split(":")
                port = int(port)
                self._handle_connect(host, port)
            else:
                host, port = self._get_host_port(data, target)
                if not host:
                    return
                self._handle_http(host, port, data)
        except Exception:
            return

    def _recv_headers(self, timeout=1.5):
        self.request.settimeout(timeout)
        data = b""
        try:
            while b"\r\n\r\n" not in data:
                chunk = self.request.recv(self.BUFSIZE)
                if not chunk:
                    break
                data += chunk
                if len(data) > 65536:
                    break
        except Exception:
            pass
        return data

    def _get_host_port(self, raw, url):
        try:
            for line in raw.split(b"\r\n"):
                if line.lower().startswith(b"host:"):
                    host = line.split(b":", 1)[1].strip().decode(errors="ignore")
                    if ":" in host:
                        h, p = host.split(":", 1)
                        return h, int(p)
                    return host, 80
            url = url.decode() if isinstance(url, bytes) else url
            if url.startswith("http://"):
                after = url[len("http://") :]
                host = after.split("/", 1)[0]
                if ":" in host:
                    h, p = host.split(":", 1)
                    return h, int(p)
                return host, 80
        except Exception:
            pass
        return None, None

    def _handle_connect(self, host, port):
        try:
            remote = socket.create_connection((host, port), timeout=5)
        except Exception:
            try:
                self.request.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            except:
                pass
            return
        try:
            self.request.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        except:
            remote.close()
            return
        try:
            self._tunnel(self.request, remote)
        finally:
            try:
                remote.close()
            except:
                pass

    def _handle_http(self, host, port, first_data):
        try:
            remote = socket.create_connection((host, port), timeout=5)
            remote.sendall(first_data)
            self._relay_once(self.request, remote)
            while True:
                r = remote.recv(self.BUFSIZE)
                if not r:
                    break
                self.request.sendall(r)
        except Exception:
            pass
        finally:
            try:
                remote.close()
            except:
                pass

    def _relay_once(self, src, dst, timeout=0.2):
        try:
            src.settimeout(timeout)
            while True:
                chunk = src.recv(self.BUFSIZE)
                if not chunk:
                    break
                dst.sendall(chunk)
                if len(chunk) < self.BUFSIZE:
                    break
        except Exception:
            return

    def _tunnel(self, a, b):
        sockets = [a, b]
        try:
            while True:
                rlist, _, _ = select.select(sockets, [], [], 10)
                if not rlist:
                    break
                for r in rlist:
                    other = b if r is a else a
                    data = r.recv(self.BUFSIZE)
                    if not data:
                        return
                    other.sendall(data)
        except Exception:
            return


class ProxyMaker:
    """Start N local HTTP proxies (CONNECT supported) on 127.0.0.1 starting at start_port."""

    def __init__(self, start_port=8000, count=5, host="127.0.0.1"):
        self.start_port = int(start_port)
        self.count = int(count)
        self.host = host
        self._servers = []  # list of (server, thread, port)

    def start_all(self):
        for i in range(self.count):
            port = self.start_port + i
            srv = _ThreadingTCPServer((self.host, port), _SimpleProxyHandler)
            t = threading.Thread(target=srv.serve_forever, daemon=True)
            t.start()
            self._servers.append((srv, t, port))
            print(f"[proxy-maker] started proxy on {self.host}:{port}")
        return [(self.host, p) for (_, _, p) in self._servers]

    def stop_all(self):
        for srv, thr, port in self._servers:
            try:
                srv.shutdown()
                srv.server_close()
            except Exception:
                pass
        self._servers = []
        print("[proxy-maker] stopped proxies")
