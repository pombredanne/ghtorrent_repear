import collections
import sys
import bs4 as bs
import urllib.request
pr_rate = 0
url = "https://github.com/jonatanskogsfors/chrono"
print(url)
urlList = ["/pulls","/pulls?q=is%3Apr+is%3Aclosed+","/pulls?q=is%3Apr+is%3Amerged+"]
url_opr = url+urlList[0]
url_cpr = url+urlList[1]
url_mpr = url+urlList[2]
page = urllib.request.urlopen(url_opr).read()
dom = bs.BeautifulSoup(page,'lxml')
print(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n",""))
opr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Open")[0])
page = urllib.request.urlopen(url_cpr).read()
dom = bs.BeautifulSoup(page,'lxml')
cpr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Closed")[0])
page = urllib.request.urlopen(url_mpr).read()
dom = bs.BeautifulSoup(page,'lxml')
mpr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Total")[0])
print("opr: ",opr,",cpr: ",cpr,",mpr: ",mpr)
pr = mpr+cpr+opr
if(pr > 0):
    pr_rate = float(mpr+cpr)/float(pr*1.0)
print(pr_rate)