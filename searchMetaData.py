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

url = "https://www.google.com/search?start=1&q=" + searchTerm.replace(" ", "+")
fileName = searchTerm.replace(" ", "_") + "_results"



def printOut():
    for i in range(len(resultDescs)):
        print("Result title: " + resultTitles[i])
        print("Page title: " + pageTitles[i])
        print("Result meta Description: " + resultDescs[i])
        print("Page meta Description: " + pageDescs[i])
        print("Link: " + links[i])
        print("=====================")



def writeToJson():
    file = open(fileName + ".json","w+")
    file.write('{"Search term":"' + searchTerm + '","Results":[')

    for i in range(len(resultDescs)):
        if i > 0:
            file.write(',')
        resultTitle = '"Result title":' + json.dumps(resultTitles[i])
        metaTitle = '"Page title":' + json.dumps(pageTitles[i])
        resultDescription = '"Result meta description":' + json.dumps(resultDescs[i])
        metaDescription = '"Actual meta description":' + json.dumps(pageDescs[i])
        link = '"Link":' + json.dumps(links[i])

        file.write("{" + resultTitle + "," + metaTitle + "," + resultDescription + "," + metaDescription + "," + link + "}")

    file.write(']}')
    file.close()


def writeToCsv():

    file = open(searchTerm.replace(" ", "_") + "_results.csv","w+")
    writer = csv.writer(file)

    writer.writerow([searchTerm, "Result meta description", "Page title", "Page meta description", "link"])
    for i in range(len(resultDescs)):
        writer.writerow([resultTitles[i], resultDescs[i], pageTitles[i], pageDescs[i], links[i]])
    

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

        


