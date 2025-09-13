from NetRecon.net_scan import Port_scanner
def take_input():
    try:
        ports = input("Enter the Ports or Port you wanna scan (comma-separated): ")
        ports = [int(p.strip()) for p in ports.split(",")]
        host = input("Now the Host you want to scan: ")
        timeout = int(input("Enter Delay before scanning port: "))
        return host, ports, timeout
    except ValueError:
        print("Please enter valid information.")
        return None, None, None

        
     
     
     
     
if __name__=="__main__":
    host, port , timeout=take_input()
    if host and port:
        scanner = Port_scanner(host, port, timeout)
        scanner.run()