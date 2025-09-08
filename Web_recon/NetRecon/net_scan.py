import socket
import threading
import ssl

port= input("Enter the Ports or Port you wanna scan : ")
port=port.split(",")
port= [int(p.strip()) for p in port]
host=input("Now the Host you want to scan : ")
timeout=int(input("Enter Delay before scanning port:"))

def scan(p): 
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket.gethostbyname(host)
            s.settimeout(timeout)
            s.connect((host,p))
            print(f"Port {p} is open ")
            try:
                 #banner Grabbing and port status checking for common ports 
                 if p==80:
                    req=(
                        'GET / HTTP/1.1\r\n'
                        f'Host:{host}\r\n'
                        'User-Agent: SimpleScanner/1.0\r\n'
                        'Connection: close\r\n'
                        '\r\n'
                    )
                    s.send(req.encode())
                    banner=s.recv(2048).decode(errors="ignore")
                    print(f"Banner from port {p}:\n{banner.strip()}")
                 elif p==443:
                     
                     s.close()
                     
                     context=ssl.create_default_context()
                     #making a separate socket with ssl wrapping for a possible ssl/tls handshake to get a banner 
                     ssl_sock=context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),server_hostname=host)
                     ssl_sock.connect((host,p))
                     print(f"Port {p} is open (HTTPS)")

                     req=(
                        'GET / HTTP/1.1\r\n'
                        f'Host:{host}\r\n'
                        'User-Agent: SimpleScanner/1.0\r\n'
                        'Connection: close\r\n'
                        '\r\n'
                        )
                     ssl_sock.send(req.encode())
                     banner = ssl_sock.recv(2048).decode(errors="ignore")
                     print(f"HTTPS Banner from port {p}:\n{banner.strip()}")
                     ssl_sock.close()
                    

                 elif p==21:
                     banner=s.recv(2048).decode(errors="ignore")
                     print(f" FTP Banner from port {p}:\n{banner.strip()}")
                 elif p==22:
                     banner=s.recv(2048).decode(errors="ignore")
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


        except ConnectionRefusedError:
            print(f"Port {p} is Closed")
        except socket.timeout:
            print(f"Port {p} is filtered")
        except Exception as e:
            print(f"Unknow error on Port {p} : {e}")
        finally:
            try:
                s.close()
            except:
                pass
#Added threading for Simultaneous port Scans 
threads=[]
for p in port:
    t=threading.Thread(target=scan,args=(p,))
    threads.append(t)
    t.start()

    
for t in threads:
    t.join()
        
                             

print("All ports are Scanned!")


