import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json


# Query counts the number of distinct authors contributing to a project.
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''


def run(project_id, repo_path, cursor, **options):
    num_core_contributors = 0
    num_commits = 0
    commitList = []
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    print(repoName)
    os.chdir("../../path/")
    print(os.getcwd())
    for repos in os.listdir():
        if(repos == repoName):
            inner_os.chdir(repos)
            stream = os.popen('git shortlog -s -n').read().split("\n")
            totalNumberOfCommits = 0
            for commits in stream:
                commit = commits.replace(" ","")
                if(len(commit) > 0):
                    commitList.append(int(commit.split("\t")[0]))
                    totalNumberOfCommits += int(commit.split("\t")[0])
            num_commits = totalNumberOfCommits
            totalNumberOfCommits = (totalNumberOfCommits*4)/5
            commitList.sort(reverse=True)
            count = 0
            core_contributors = 0
            for commits in commitList:
                if(count > totalNumberOfCommits):
                    break
                count += commits
                core_contributors += 1
            print('core contributors: ',core_contributors)
            break
    
    # rows = cursor.fetchall()
    # if cursor.rowcount == 0:    # Non-existent history
    #     return False, num_core_contributors

    # commits = collections.OrderedDict()
    # for row in rows:
    #     commits[row[0]] = row[1]
    # num_commits = sum(commits.values())

    cutoff = options.get('cutoff', 1.0)
    aggregate = 0
    for v in commitList:
        num_core_contributors += 1
        aggregate += v
        if (aggregate / num_commits) >= cutoff:
            break

    threshold = options['threshold']
    num_core_contributors >= threshold, num_core_contributors
    return (num_core_contributors >= threshold, num_core_contributors)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
