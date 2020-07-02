import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
import arrow
from time import strptime
from datetime import datetime

QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            stream = inner_os.popen('git for-each-ref --format="%(refname:short) | %(creatordate)" refs/tags/* --sort=creatordate').read().split("\n")
            totalNumberOfReleases = 0
            release_score = 0
            today = options.get('today', datetime.today().date())
            if isinstance(today, str):
                today = datetime.strptime(today, '%Y-%m-%d')
            print('today: ',today)
            if(len(stream) > 3 ):
                if(len(stream)-2 > 0):
                    time1 = stream[len(stream)-2].split("| ")[1].split(" ") # Latest release date
                    Y1 = int(time1[4])
                    M1 = int(strptime(time1[1],'%b').tm_mon)
                    D1 = int(time1[2])
                    end = datetime(Y1,M1,D1)
                    time2 = stream[0].split("| ")[1].split(" ") # First release date
                    Y2 = int(time2[4])
                    M2 = int(strptime(time2[1],'%b').tm_mon)
                    D2 = int(time2[2])            
                    start = datetime(Y2,M2,D2)
                    numberOfDays = 0
                    for d in arrow.Arrow.range('day', start, end):
                        numberOfDays += 1
                    totalNumberOfReleases = len(stream)-1
                    averageReleaseTime = numberOfDays/totalNumberOfReleases # In number of days
                    timeNow = str(today).split(" ")[0].split("-")
                    Y2 = int(timeNow[0])
                    M2 = int(timeNow[1])
                    D2 = int(timeNow[2])
                    now = datetime(Y1,M2,D2)
                    daysPassed = 0
                    for d in arrow.Arrow.range('day',end,now):
                        daysPassed += 1
                    if(daysPassed <= averageReleaseTime):
                        release_score = 1
                    print("----- METRIC: RELEASES -----")
                    print("numberOfDays: ",numberOfDays)
                    break
    threshold = options['threshold']
    return (release_score >= threshold, release_score)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
