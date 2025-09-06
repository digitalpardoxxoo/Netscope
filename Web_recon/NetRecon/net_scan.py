import socket
import threading

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
                 s.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                 banner=s.recv(2048).decode(errors="ignore")
                 if banner.strip():
                    print(f"Banner from port {p}:\n{banner}")
                 else:
                    print(f"No banner received from port {p}")
            except:
                 print(f"Port {p} open, but no banner grabbed")

        except :
             print(f"Port {p} is closed")
             s.close()
#Added threading for Simultaneous port Scans 
threads=[]
for p in port:
    t=threading.Thread(target=scan,args=(p,))
    threads.append(t)
    t.start()

    
for t in threads:
    t.join()
        
                             

print("All ports are Scanned!")


