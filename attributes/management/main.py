import sys
import bs4 as bs
import urllib.request
from time import strptime
from datetime import datetime
import mysql.connector
import arrow
import os
import os as inner_os
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    avg_issues = 0
    numberOfMonths = 0
    totalNoOfIssues = 0
    cursor.execute("SELECT url FROM projects WHERE id={0}".format(project_id))
    url = cursor.fetchone()[0].replace("api.","").replace("/repos","")
    page = urllib.request.urlopen(url).read()
    dom = bs.BeautifulSoup(page,'lxml')
    totalNoOfIssues  = int(dom.body.find_all('span',class_='Counter')[0].text.replace("\n",""))
    num_commits = 0
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            stream = inner_os.popen('git log --pretty=format:"%cd"').read().split("\n")
            num_commits = len(stream)
            numberOfMonths = 0
            if(num_commits > 1):
                prev = stream[num_commits-1].split(" ")
                Y1 = int(prev[4])
                M1 = int(strptime(prev[1],'%b').tm_mon)
                D1 = int(prev[2])
                start = datetime(Y1,M1,D1)
                prev = stream[0].split(" ")
                Y1 = int(prev[4])
                M1 = int(strptime(prev[1],'%b').tm_mon)
                D1 = int(prev[2])
                end = datetime(Y1,M1,D1)
                for d in arrow.Arrow.range('month', start, end):
                    numberOfMonths += 1
            issueFrequency = float(totalNoOfIssues)/(float(numberOfMonths)*1.0)
            print("----- METRIC: ISSUES -----")
            print('issueFrequency:',issueFrequency)
            break
    if numberOfMonths >= options.get('minimumDurationInMonths', 1):
        avg_issues = totalNoOfIssues / numberOfMonths 
    else:
        return False, avg_issues

    threshold = options['threshold']
    return avg_issues >= threshold, avg_issues

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
