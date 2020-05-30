import bs4 as bs
import urllib.request
from time import strptime
from datetime import datetime
import arrow
page = urllib.request.urlopen('https://github.com/rishaiittp/news').read()
dom = bs.BeautifulSoup(page,'lxml')
totalNoOfCommits  = int(dom.body.find_all('span',class_='text-emphasized')[0].text.replace("\n",""))
aList = dom.body.find_all('a')
for shaKey in aList:
    if("master" not in shaKey.get('href') and "/rishaiittp/news/commit/" in shaKey.get('href')):
        print(shaKey.get('href'))
        shaKey =  shaKey.get('href').split("/")[4]
        print(totalNoOfCommits)
        nextIndex = str(totalNoOfCommits - (totalNoOfCommits%34))
        page = urllib.request.urlopen('https://github.com/rishaiittp/news/commits').read()
        dom = bs.BeautifulSoup(page,'lxml')
        dateString = dom.body.find_all('div',class_='commit-group-title')[0].text.replace("\n","").replace("Commits on ","").replace(",","").split(" ")
        Y1 = int(dateString[2])
        M1 = int(strptime(dateString[0],'%b').tm_mon)
        D1 = int(dateString[1])
        end = datetime(Y1,M1,D1)
        print('https://github.com/rishaiittp/news/commits/master?after='+shaKey+"+"+nextIndex)
        page = urllib.request.urlopen('https://github.com/rishaiittp/news/commits/master?after='+shaKey+"+"+nextIndex).read()
        dom = bs.BeautifulSoup(page,'lxml')
        domGroup = dom.body.find_all('div',class_='commit-group-title')
        dateString = domGroup[len(domGroup)-1].text.replace("\n","").replace("Commits on ","").replace(",","").split(" ")
        Y2 = int(dateString[2])
        M2 = int(strptime(dateString[0],'%b').tm_mon)
        D2 = int(dateString[1])
        start = datetime(Y2,M2,D2)
        numberOfMonths = 0
        for d in arrow.Arrow.range('month', start, end):
            numberOfMonths += 1
        print(numberOfMonths)
        avgNumberOfCommitsPerMonth = float(totalNoOfCommits)/(float(numberOfMonths)*1.0)
        print('avg:',avgNumberOfCommitsPerMonth)
        break