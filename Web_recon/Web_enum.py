import requests
from bs4 import BeautifulSoup
import os

print("""
    Welcome to Web_enumerator !
    Use the following commands if u need to do web recon!
      
    Fuzz-For Directory Fuzzing
    Crawl-to get data from web 
    Sub_enum-For Sub-domain Enumeration
""")

Make_choice=input("Enter Your Command:")

#Function for Scraping Web content using requests and then beatuifying with beatuifulsoup
def fetch_url():
    url=input("Enter your URL:")
    try:
        response=requests.get(url,timeout=10)
        print(f"Status code : {response.status_code}")
        status_messages = {
            200: "Success! Page fetched successfully.",
            301: "Redirected permanently.",
            302: "Redirected temporarily.",
            403: "Forbidden! You don't have permission to access this page.",
            404: "Not Found! Invalid URL.",
            500: "Internal Server Error on the site.",
            503: "Service Unavailable. Try again later."
         }
        
        
        if response.status_code!=200:
          print(status_messages.get(response.status_code,"Dont know wht happened man use some other tool"))
          return
        
        soup=BeautifulSoup(response.content,"html.parser")
        print(f" Site content:\n{soup.prettify()[:1000]}")
        print("\n")
        print(f" Title of Site is: {soup.title.string if soup.title else "no title found "}")
        print("\n")
        print("All links are:\n")
        
        for link in soup.find_all("a"):
            print(f"{link.get('href')}")

    except requests.exceptions.ConnectionError:
        print("Error has Occured While Connecting to the URL")
    except requests.exceptions.MissingSchema:
        print("Url has no http ot https in it !!")
    except Exception:
        print("Unknown Error occured")

#Function For Directory Fuzzing
def DirectoryFuzz():
    #You should first navigate to the same path as the wordlist.txt file before trying to run the tool for directory fuzzing 
    url=input("Enter your URL:")
    print("Finding Directories....\n")
    wordlist=input("Enter file name:")
    if os.path.exists(wordlist):
        with open(wordlist,"r") as f:
            for line in f:
                newpath=line.strip()
                new_url=f"{url.rstrip("/")}/{newpath}"
                try:
                    find_dir=requests.get(new_url,timeout=10)
                    if find_dir.status_code in [200,403]:
                        print(f"Found:{new_url} , (Status:{find_dir.status_code})")
                except requests.RequestException as e:
                    print(f"[-] Error with {new_url}: {e}")
    else: 
        print("Navigate to the required path Since your file wasn't found here or mayber try changing the name")

#Function for Finding Different SubDomains!
def Subdomain_enum():
    a=input("Enter Domain name of Site :")
    file_to_use=input("Enter file name:")
    print("Finding possible Subdomains....\n")
    if os.path.exists(file_to_use):
        with open(file_to_use,"r") as f:
            for line in f:
                sub=line.strip()
                Subdomain=f"https://{sub}.{a}"
                try:
                    req=requests.get(Subdomain,timeout=10)
                    if req.status_code in [200,404,302,301,403]:
                        print(f"Found:{Subdomain},(Status:{req.status_code})")

                except:
                    pass
    else:
        print("Navigate to the required path Since your file wasn't found here or mayber try changing the name")


switch={
    "crawl":lambda:fetch_url(),
    "fuzz":lambda:DirectoryFuzz(),
    "sub_enum":lambda:Subdomain_enum(),
}
switch.get(Make_choice,lambda:print("Invalid Choice"))()

while True:
    Make_choice=input("To exit use quit or exit:")
    if Make_choice in ['quit','exit']:
        break
    else:
        Make_choice=input("Enter Your Command:")
        switch.get(Make_choice,lambda:print("Invalid Choice"))()


