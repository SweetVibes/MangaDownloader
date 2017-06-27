from bs4 import BeautifulSoup
import requests
import os
import re
import time
from urllib.request import Request
from urllib.request import urlopen

numberExtractor = re.compile(r"\d+")
def getcontent(mangaurl):
    res = requests.get(mangaurl, timeout=30, headers=headers)
    res.raise_for_status()
    return res


def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)


def getTitleAndPage(soup):
    mangaInfoContent = soup.find(id="mangainfo")
    title = mangaInfoContent.h1.text
    title = title.replace(":", "").strip()
    page = mangaInfoContent.span.text
    page = page.replace("-", "").strip()
    mangaInfo = {"title": title, "page": page}
    return mangaInfo


def getSoup(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup


def getChapterNumber(mangaInfo):
    chn = mangaInfo["title"][-3:].strip()
    match = numberExtractor.search(chn)
    return int(match.group())


def downloadImage(imgURL, pageNumber):
    request = Request(imgURL, None, headers)
    resource = urlopen(request)
    output = open(pageNumber + ".jpg", "wb")
    output.write(resource.read())
    output.close()


def getAllImageUrls(chapterNumber, soup):
    chn = chapterNumber
    print('Downloading chapter number '+str(chapterNumber))
    while chapterNumber != chn + 1:
        imgHolder = soup.find(id="imgholder")
        nextUrl = hostName + imgHolder.a['href']
        imgURL = imgHolder.img['src']
        nextPageContent = getcontent(nextUrl)
        soup = getSoup(nextPageContent.text)
        info = getTitleAndPage(soup)
        chapterNumber = getChapterNumber(info)
        downloadImage(imgURL, info["page"])
        print("Downloaded "+info["page"])
        print(info,chapterNumber)



def startDownload(mangaurl):
    mangaContent = getcontent(mangaurl)
    soup = getSoup(mangaContent.text)
    mangaInfo = getTitleAndPage(soup)
    createFolder(mangaInfo["title"])
    chapterNumber = getChapterNumber(mangaInfo)
    getAllImageUrls(chapterNumber, soup)


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent': user_agent, }
folderPath = r"B:\Manga"
createFolder(folderPath)
mangaUrl = "http://www.mangapanda.com/naruto-gaiden-the-seventh-hokage/10"
hostName = "http://www.mangapanda.com"
startDownload(mangaUrl)