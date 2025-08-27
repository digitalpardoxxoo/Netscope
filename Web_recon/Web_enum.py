import requests
from bs4 import BeautifulSoup
url=input("Enter your URL:")



def fetch_url(url):
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
          print(status_messages.get(response.status_code,"Dont know wht happened ask google"))
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
        
fetch_url(url)
