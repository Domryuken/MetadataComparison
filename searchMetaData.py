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
fileName = f"{searchTerm.replace(' ', '_')}_results.csv"

def writeToCsv():

    print(f"writing to file {fileName}")
    file = open(fileName, "w+", encoding="utf-8", newline='')
    writer = csv.writer(file)

    writer.writerow(["Ranking position", f'=HYPERLINK("{url}","Search results for: {searchTerm}")', "Implemented title", "Googles title", "Implemented meta description", "Googles meta description"])
    for i in range(len(resultDescs)):
        writer.writerow([i+1, links[i], pageTitles[i], resultTitles[i], pageDescs[i], resultDescs[i]])

def getPage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers = headers)
    return BeautifulSoup(page.content, 'html.parser')



def resultsForPage(number):
        
    resultsPage = getPage(f"{url}&start={number}")
    results = resultsPage("div", class_="rc")

    for result in results:
        
        link = result.find("a").get("href")
        resultTitle = result.find("h3").getText()
        resultDesc = result.find("span", class_="st").getText()

        actualPage = getPage(link)
        
        pageTitleElement = actualPage.find("title")
        pageTitle = "No title given" if pageTitleElement is None else pageTitleElement.getText()
            
        pageDescElement = actualPage.find("meta", attrs={"name": re.compile("[d|D]escription")})
        pageDesc = "No description given" if pageDescElement is None else pageDescElement.get("content")

        links.append(link)
        resultTitles.append(resultTitle)
        resultDescs.append(resultDesc)
        pageTitles.append(pageTitle)
        pageDescs.append(pageDesc)

        print(f"{link}, {pageTitle}, {resultTitle}, {pageDesc}, {resultDesc}")

resultsForPage(0)
resultsForPage(10)
resultsForPage(20)

writeToCsv()

        


