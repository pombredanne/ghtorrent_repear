import bs4 as bs
import urllib.request
from time import strptime
from datetime import datetime
import mysql.connector
import arrow
ghtorrentDb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ghtorrent"
)
project_id = 75357047
cursor = ghtorrentDb.cursor()
cursor.execute("SELECT url FROM projects WHERE id={0}".format(project_id))
url = cursor.fetchone()[0].replace("api.","").replace("/repos","")
print('url: '+url)
repoName = url.replace("https://github.com","")
repoName += "/commit/"
print(repoName)
page = urllib.request.urlopen(url).read()
dom = bs.BeautifulSoup(page,'lxml')
totalNoOfIssues  = int(dom.body.find_all('span',class_='Counter')[0].text.replace("\n",""))
print(totalNoOfIssues)
aList = dom.body.find_all('a')
#print(aList)
for shaKey in aList:
    if("master" not in shaKey.get('href') and repoName in shaKey.get('href')):
        print(shaKey.get('href'))
        shaKey =  shaKey.get('href').split("/")[4]
        print(totalNoOfIssues)
        nextIndex = str(totalNoOfIssues - (totalNoOfIssues%34))
        page = urllib.request.urlopen(url + '/commits').read()
        dom = bs.BeautifulSoup(page,'lxml')
        dateString = dom.body.find_all('div',class_='commit-group-title')[0].text.replace("\n","").replace("Commits on ","").replace(",","").split(" ")
        Y1 = int(dateString[2])
        M1 = int(strptime(dateString[0],'%b').tm_mon)
        D1 = int(dateString[1])
        end = datetime(Y1,M1,D1)
        print(url+'/commits/master?after='+shaKey+"+"+nextIndex)
        page = urllib.request.urlopen(url+'/commits/master?after='+shaKey+"+"+nextIndex).read()
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
        print('Number of Months: ',numberOfMonths)
        print('Total Number of Issues: ',totalNoOfIssues)
        if(numberOfMonths > 0):
          issueFrequency = float(totalNoOfIssues)/(float(numberOfMonths)*1.0)
        print('issueFrequency:',issueFrequency)
        break