import requests
from bs4 import BeautifulSoup
import pdfkit
import os
import sys
import wget

# For windows people
# path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
path_wkthmltopdf = r'/usr/local/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
# Fake user agent for pages that require a user agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

baseUrl = sys.argv[1]
startUrl = sys.argv[2]
fileType = sys.argv[3]

print("Crawling: " + baseUrl)
print("Starting at: " + startUrl)
print("Searching for filetype: " + fileType)

crawledPages = []
linksToDownload = []

def crawler(url, depth):
    if depth == 0:
        return None
    if url in crawledPages:
        return None
    else:
        crawledPages.append(url)
        
    if "http" not in url:
        url = "https://"+url
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    fileLinks = soup.findAll('a')
    
    for fileLink in fileLinks:
        try:
            href = fileLink["href"]

            if fileType in href and href not in crawledPages:
                linksToDownload.append(href)
                crawledPages.append(href)
            if ':' in href and fileType not in href and href not in crawledPages and baseUrl in href and "facebook" not in href and "pinterest" not in href and "subscribe" not in href and "google" not in href and "twitter" not in href:
                crawler(href, depth - 1)
            if href.startswith('/'):
                crawler("https://" + baseUrl + href,depth - 1)
            
        except Exception as e: 
            pass

crawler(startUrl, 2)

print("Pages: ", crawledPages)
print("Downloads: ", linksToDownload)
cwd = os.getcwd()
for file in linksToDownload:
    print("Downloading: " + file)
    wget.download(file, cwd + "/downloads/" + file.split("/")[-1])  
 