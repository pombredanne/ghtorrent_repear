import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
import bs4 as bs
import urllib.request

QUERY = '''
SELECT url FROM projects WHERE id={0}
'''

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
def run(project_id, repo_path, cursor, **options):
    pr_rate = 0
    cursor.execute(QUERY.format(project_id))
    url = cursor.fetchone()[0].replace("api.","").replace("/repos","")
    urlList = ["/pulls","/pulls?q=is%3Apr+is%3Aclosed+","/pulls?q=is%3Apr+is%3Amerged+"]
    url_opr = url+urlList[0]
    url_cpr = url+urlList[1]
    url_mpr = url+urlList[2]
    page = urllib.request.urlopen(url_opr).read()
    dom = bs.BeautifulSoup(page,'lxml')
    opr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Open")[0])
    page = urllib.request.urlopen(url_cpr).read()
    dom = bs.BeautifulSoup(page,'lxml')
    cpr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Closed")[0])
    page = urllib.request.urlopen(url_mpr).read()
    dom = bs.BeautifulSoup(page,'lxml')
    mpr  = int(dom.body.find_all('a',class_='btn-link selected')[0].text.replace("\n","").split("Total")[0])
    print("----- METRIC: PULL REQUESTS -----")
    pr = mpr+cpr+opr
    if(pr > 0):
        pr_rate = float(mpr+cpr)/float(pr*1.0)
    threshold = options['threshold']
    pr_rate >= threshold, pr_rate
    print("PR rate: ",pr_rate)
    return (pr_rate >= threshold, pr_rate)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
