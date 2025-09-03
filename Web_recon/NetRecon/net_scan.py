import socket
import threading

port= input("Enter the Ports or Port you wanna scan : ")
port=port.split(",")
port= [int(p.strip()) for p in port]
host=input("Now the Host you want to scan : ")



def scan(p): 
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket.gethostbyname(host)
            s.settimeout(10)
            s.connect((host,p))
            print(f"Port {p} is open")
        except:
            print(f"Port {p} is closed")
            s.close()

threads=[]
for p in port:
    t=threading.Thread(target=scan,args=(p,))
    threads.append(t)
    t.start()

    
for t in threads:
    t.join()
        
                             
       

print("All ports are Scanned!")