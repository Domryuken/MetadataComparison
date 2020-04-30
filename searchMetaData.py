import requests
from bs4 import BeautifulSoup
import re
import json
import csv

links = []
resultTitles = []
resultDescs = []
pageTitles = []
pageDescs = []

searchTerm = input("Enter search term: ")
print("...")

url = f"https://www.google.com/search?q={searchTerm.replace(' ', '+')}"
fileName = f"{searchTerm.replace(' ', '_')}_results"

def writeToCsv():

    file = open(f"{fileName}.csv", "w+", encoding="utf-8")
    writer = csv.writer(file)

    writer.writerow([f'=HYPERLINK("{url}","Search results for: {searchTerm}")', "Result meta description", "Page title", "Page meta description"])
    for i in range(len(resultDescs)):
        writer.writerow([f'=HYPERLINK("{links[i]}","{resultTitles[i]}")', resultDescs[i], pageTitles[i], pageDescs[i]])

def getPage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers = headers)
    return BeautifulSoup(page.content, 'html.parser')




resultsPage = getPage(url)
results = resultsPage("div", class_="rc")

for result in results:
        
    link = result.find("a").get("href")
    links.append(link)
    resultTitles.append(result.find("h3").getText())
    resultDescs.append(result.find("span", class_="st").getText())

    actualPage = getPage(link)
    
    pageTitle = actualPage.find("title").getText()
    if pageTitle is None:
        pageTitles.append("No title given")
    else:
        pageTitles.append(pageTitle)
        
    pageDesc = actualPage.find("meta", attrs={"name": re.compile("[d|D]escription")})
    if pageDesc is None:
        pageDescs.append("No description given")
    else:
        pageDescs.append(pageDesc.get("content"))

writeToCsv()


print("Saved as " + fileName)

        


