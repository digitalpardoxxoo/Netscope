import socket
port= input("Enter the Ports or Port you wanna scan : ")
port=port.split(",")
port= [int(p.strip()) for p in port]
host=input("Now the Host you want to scan : ")


for i in port:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        socket.gethostbyname(host)
        s.settimeout(10)
        s.connect((host,i))
        print(f"Port {i} is open")
    except:
        print(f"Port {i} is closed")
        s.close()

