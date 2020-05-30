import sys
import bs4 as bs
import urllib.request
from time import strptime
from datetime import datetime
import mysql.connector
import arrow


def run(project_id, repo_path, cursor, **options):
    avg_issues = 0
    numberOfMonths = 0
    totalNoOfIssues = 0
    cursor.execute("SELECT url FROM projects WHERE id={0}".format(project_id))
    url = cursor.fetchone()[0].replace("api.","").replace("/repos","")
    print(url)
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
            for d in arrow.Arrow.range('month', start, end):
                numberOfMonths += 1
            print(numberOfMonths)
            issueFrequency = float(totalNoOfIssues)/(float(numberOfMonths)*1.0)
            print('issueFrequency:',issueFrequency)
            break
    # result = cursor.fetchone()
    # first_commit_date = result[0]
    # last_commit_date = result[1]

    # if first_commit_date is None or last_commit_date is None:
    #     return False, avg_issues

    # cursor.execute(
    #     '''
    #         SELECT COUNT(*)
    #         FROM issues i
    #         WHERE i.repo_id = {0}
    #     '''.format(project_id)
    # )

    # result = cursor.fetchone()
    # num_issues = result[0]

    # Compute the number of months between the first and last commit
    # delta = relativedelta.relativedelta(last_commit_date, first_commit_date)
    # num_months = delta.years * 12 + delta.months

    if numberOfMonths >= options.get('minimumDurationInMonths', 1):
        avg_issues = totalNoOfIssues / numberOfMonths 
    else:
        return False, avg_issues

    threshold = options['threshold']
    return avg_issues >= threshold, avg_issues

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
