import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
from spellchecker import SpellChecker
import re
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    num_core_commit_words = 0
    totalNumberOfCommitWords = 0
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            Dirs = []
            Files = []
            for (root,dirs,files) in inner_os.walk("",topdown=True):
                Dirs.append(dirs.lower())
                Files.append(files.lower())
            stream = inner_os.popen('git log --pretty=format:"%s"').read().split("\n")
            for commits in stream:
                commits = commits.lower()
                for ab in Dirs:
                    if(ab in commits):
                        commits.replace(ab,"")
                        num_core_commit_words += 1
                        totalNumberOfCommitWords += 1
                for ab in Files:
                    if(ab in commits):
                        commits.replace(ab,"")
                        num_core_commit_words += 1
                        totalNumberOfCommitWords += 1
                nr = re.sub("[^0123456789 ]","",commits)
                nr = ' '.join(nr.split())
                totalNumberOfCommitWords += len(nr.split())
                trim_commit = re.sub("[^a-zA-Z ]+", "", commits)
                trim_commit = ' '.join(trim_commit.split())
                #trim_commit = re.sub(r"\b[0-9]\b", "", trim_commit)
                # print('trim: ',len(trim_commit.split()))
                totalNumberOfCommitWords += len(trim_commit.split())
                spell = SpellChecker()
                trim_commit = re.sub(r"\b[a-zA-Z]\b", "", trim_commit)
                trim_commit = re.sub(r"\b[a-zA-Z][a-zA-Z]\b", "", trim_commit)
                trim_commit = trim_commit.split()
                spelled = spell.known(trim_commit)
                # print('spelled: ',spelled)
                num_core_commit_words += len(spelled)
            print("----- METRIC: COMMIT QUALITY -----")
            commits_ratio = 0
            # print('total: ',totalNumberOfCommitWords)
            # print('core: ',num_core_commit_words)
            if(totalNumberOfCommitWords > 0):
                commits_ratio = float(num_core_commit_words)/float(totalNumberOfCommitWords*1.0)
                print('core commits ratio: ',commits_ratio)
            break
    threshold = options['threshold']
    return (commits_ratio >= threshold, commits_ratio)
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
