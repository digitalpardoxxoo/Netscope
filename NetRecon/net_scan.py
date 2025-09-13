import socket
from concurrent.futures import ThreadPoolExecutor
import ssl

class Port_scanner:
    
    def __init__(self, host, port, timeout):
        self.host=host
        self.port=port
        self.timeout=timeout

    def chunk_ports(self,chunk_size):
        for i in range(0, len(self.port), chunk_size):
            yield self.port[i: i + chunk_size]

    def scan(self,p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.gethostbyname(self.host)
            s.settimeout(self.timeout)
            a = s.connect_ex((self.host, p))

            if a != 0:
                print(f"Connect is not possible for port {p}, maybe filtered or closed by firewall")
                print(f"Error : {a}")

            elif a == 0:
                print("Connection Established")
                print(f"Port {p} is open")
                try:
                    # banner Grabbing and port status checking for common ports
                    if p == 80:
                        req = (
                            'GET / HTTP/1.1\r\n'
                            f'Host:{self.host}\r\n'
                            'User-Agent: SimpleScanner/1.0\r\n'
                            'Connection: close\r\n'
                            '\r\n'
                        )
                        s.send(req.encode())
                        banner = s.recv(2048).decode(errors="ignore")
                        print(f"Banner from port {p}:\n{banner.strip()}")

                    elif p == 443:
                        s.close()
                        context = ssl.create_default_context()
                        # making a separate socket with ssl wrapping for a possible ssl/tls handshake to get a banner
                        ssl_sock = context.wrap_socket(
                            socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                            server_hostname=self.host
                        )
                        ssl_sock.connect((self.host, p))
                        print(f"Port {p} is open (HTTPS)")

                        req = (
                            'GET / HTTP/1.1\r\n'
                            f'Host:{self.host}\r\n'
                            'User-Agent: SimpleScanner/1.0\r\n'
                            'Connection: close\r\n'
                            '\r\n'
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
                        banner = s.recv(1024).decode(errors="ignore")
                        if banner.strip():
                            print(f"Banner from {p} is:{banner.strip()}")
                        else:
                            print(f"No banner received from port {p}")

                except:
                    print(f"Port {p} open, but no banner grabbed")

        except Exception as e:
            print(f"Unknow error on Port {p} : {e}")
        finally:
            try:
                s.close()
            except:
                pass

    # Added threadpool for using segmented ports to save memory for bigger checks
    def scan_chunk(self,chunk):
        for p in chunk:
            self.scan(p)

    def run(self,chunk_size=5,max_workers=4):
        port_chunks = list(self.chunk_ports(chunk_size=chunk_size))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
           executor.map(self.scan_chunk, port_chunks)

        print("All ports are Scanned!")
