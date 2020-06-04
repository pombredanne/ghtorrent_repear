import sys
from datetime import datetime
import bs4 as bs
import urllib.request
from time import strptime
from datetime import datetime
import attributes
import requests
from lib import utilities
import mysql.connector
ghtorrentDb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ghtorrent"
)
def getLastCommitDate(project_id):
    cursor = ghtorrentDb.cursor()
    cursor.execute("SELECT url FROM projects WHERE id={0}".format(project_id))
    url = cursor.fetchone()[0] + "/commits"
    uname = "Kowndinya2000"
    token = "94f54d47604013ae801126b1dac439762e19bdf7"
    page = requests.get(url).json()[0]["commit"]["committer"]["date"].split("T")[0]
    return page
from lib import dateutil
from lib import utilities

QUERY = '''
    SELECT MAX(c.created_at)
    FROM commits c
        JOIN project_commits pc ON pc.commit_id = c.id
    WHERE pc.project_id = {0} and c.created_at > 0
'''


def run(project_id, repo_path, cursor, **options):
    bresult = False
    rresult = 'dormant'

    #cursor.execute(QUERY.format(project_id))
    #result = cursor.fetchone()
    #last_commit_date = result[0]
    last_commit_date = getLastCommitDate(project_id)
    if last_commit_date is not None:
        # Compute the delta between the last commit in the database and today.
        # Note: today may be the date the GHTorrent dump was published by
        #       ghtorrent.org
        today = options.get('today', datetime.today().date())
        if isinstance(today, str):
            print('today: ',today)
            print('str: ',str)
            today = datetime.strptime(today, '%Y-%m-%d')
            print(today)
        last_commit_date_formatted = tuple(map(int,last_commit_date.split("-")))
        delta = dateutil.relativedelta(today, datetime(*last_commit_date_formatted))
        print('delta: ',delta)
        threshold = utilities.parse_datetime_delta(options['threshold'])
        bresult = delta <= threshold
        if bresult:
            rresult = 'active'

    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
