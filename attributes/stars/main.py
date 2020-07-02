import sys
import requests
from lib import utilities


def run(project_id, repo_path, cursor, **options):
    threshold = options.get('threshold', 0)

    cursor.execute('SELECT url FROM projects WHERE id = {}'.format(project_id))
    record = cursor.fetchone()
    full_url = record[0]
    page = requests.get(full_url).json()["stargazers_count"]
    rresult = page
    bresult = True if rresult is not None and rresult >= threshold else False
    print("----- METRIC: STARS -----")
    print('stars: ',rresult,', ',bresult)
    return bresult, rresult

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
