from NetRecon.net_scan import Port_scanner
from Web_recon.Web_enum import Web_rec

def net_rec():
    try:
        ports = input("Enter the Ports or Port you wanna scan (comma-separated): ")
        ports = [int(p.strip()) for p in ports.split(",")]
        host = input("Now the Host you want to scan: ")
        timeout = int(input("Enter Delay before scanning port: "))
        return host, ports, timeout
    except ValueError:
        print("Please enter valid information.")
        return None, None, None

def web_scrape():
    try:
        print("""
Use the following commands if u need to do web recon:
fuzz     - For Directory Fuzzing
crawl    - To get data from web
sub_enum - For Sub-domain Enumeration
""")
        command = input("Enter the Command you want to perform: ").strip().lower()

        if command == "crawl":
            url = input("Enter URL to use: ").strip()
            web = Web_rec(url)
            web.fetch_url(url) 
        elif command == "fuzz":
            url = input("Enter URL to fuzz: ").strip()
            file_to_use=input("Wnter Wordlist to use:")
            web = Web_rec(url,file_to_use)
            web.DirectoryFuzz(url,file_to_use)  
        elif command == "sub_enum":
            Domain = input("Enter domain for subdomain enumeration: ").strip()
            file_to_use=input("Wnter Wordlist to use:")
            web = Web_rec(Domain,file_to_use)
            web.Subdomain_enum(Domain,file_to_use)  
        else:
            print("Invalid command.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("""
Choose an option:
1 - Network Scan
2 - Web Recon
""")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # Network scanning
        host, ports, timeout = net_rec()
        if host and ports:
            scanner = Port_scanner(host, ports, timeout)
            scanner.run()
    elif choice == "2":
        # Web scraping / recon
        web_scrape()
    else:
        print("Invalid choice. Exiting.")
