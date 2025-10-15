# main.py
from NetRecon.net_scan import Port_scanner
from Web_recon.Web_enum import Web_rec
import time


def proxy_mode():
    """
    Run network scan via a selected normal proxy (no Tor).
    Only uses proxies already defined in Port_scanner.PROXIES.
    """
    print("\n--- Proxy Mode ---")
    try:
        host, ports, timeout = net_rec()
        if not (host and ports):
            return

        # Use proxies from Port_scanner.PROXIES if available
        available_proxies = getattr(Port_scanner, "PROXIES", [])

        if not available_proxies:
            print(
                "No proxies defined. You can set Port_scanner.PROXIES in NetRecon.net_scan."
            )
            print("Running direct without proxy.")
            selected_proxy = None
        else:
            print("\nAvailable proxies:")
            for idx, proxy in enumerate(available_proxies):
                print(f"{idx} - {proxy}")

            try:
                proxy_index = int(
                    input("Select proxy index (-1 for direct/no proxy): ").strip()
                )
            except ValueError:
                print("Invalid input. Using no proxy.")
                proxy_index = -1

            if 0 <= proxy_index < len(available_proxies):
                selected_proxy = available_proxies[proxy_index]
                print(f"Using proxy: {selected_proxy}")
            else:
                selected_proxy = None
                print("Running direct without proxy.")

        scanner = Port_scanner(host, ports, timeout, proxy=selected_proxy)
        start = time.time()
        scanner.run()
        print(f"Done in {time.time()-start:.2f}s")
    except Exception as e:
        print(f"Error in Proxy mode: {e}")


def net_rec():
    try:
        ports = input("Enter the Ports or Port you wanna scan (comma-separated): ")
        ports = [int(p.strip()) for p in ports.split(",")]
        host = input("Now the Host you want to scan: ").strip()
        timeout = int(input("Enter Delay before scanning port (seconds): "))
        return host, ports, timeout
    except ValueError:
        print("Please enter valid information.")
        return None, None, None


def web_scrape():
    print(
        """
Use the following commands if u need to do web recon:
fuzz     - For Directory Fuzzing
crawl    - To get data from web
sub_enum - For Sub-domain Enumeration
"""
    )
    command = input("Enter the Command you want to perform: ").strip().lower()

    if command == "crawl":
        url = input("Enter URL to use: ").strip()
        web = Web_rec(url)
        web.fetch_url(url)
    elif command == "fuzz":
        url = input("Enter URL to fuzz: ").strip()
        file_to_use = input("Enter Wordlist to use: ").strip()
        web = Web_rec(url, file_to_use)
        web.DirectoryFuzz(url, file_to_use)
    elif command == "sub_enum":
        Domain = input("Enter domain for subdomain enumeration: ").strip()
        file_to_use = input("Enter Wordlist to use: ").strip()
        web = Web_rec(Domain, file_to_use)
        web.Subdomain_enum(Domain, file_to_use)
    else:
        print("Invalid command.")


if __name__ == "__main__":
    print(
        """
Choose an option:
1 - Network Scan
2 - Web Recon
3 - Network Scan via Proxy
"""
    )
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        host, ports, timeout = net_rec()
        if host and ports:
            scanner = Port_scanner(host, ports, timeout)
            start = time.time()
            scanner.run()
            print(f"Done in {time.time()-start:.2f}s")
    elif choice == "2":
        web_scrape()
    elif choice == "3":
        proxy_mode()
    else:
        print("Invalid choice. Exiting.")
