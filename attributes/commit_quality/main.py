import collections
import sys
import os
import os as inner_os
from lib.core import Tokenizer
from lib.utilities import url_to_json
from spellchecker import SpellChecker


# Query counts the number of distinct authors contributing to a project.
QUERY = '''
SELECT name FROM projects WHERE id={0}
'''
def run(project_id, repo_path, cursor, **options):
    num_core_commits = 0
    num_commits = 0
    commitList = []
    cursor.execute(QUERY.format(project_id))
    repoName = cursor.fetchone()[0]
    #print(repoName)
    #print(os.getcwd())
    os.chdir("path/"+str(project_id)+"/")
    stri = os.getcwd() 
    #print(os.getcwd())
    for repos in os.listdir():
        if(repos == repoName):
            os.chdir(repos)
            Dirs = []
            Files = []
            for (root,dirs,files) in inner_os.walk("",topdown=True):
                Dirs.append(dirs.lower())
                Files.append(files.lower())
            stream = inner_os.popen('git log --pretty=format:"%s"').read().split("\n")
            totalNumberOfCommits = len(stream)
            keywords = ['access', 'add ', 'aggregate', 'aggregating', 'aggregation', 'alias', 'allocate', 'allocating', 'allocation', 'apache', 'api', 'append', 'args', 'argument', 'assert', 'attribute', 'audit ', 'authentic', 'automatic', 'boot', 'branch ', 'bug', 'build', 'bytes', 'cache', 'caching', 'call', 'callback', 'catch', 'change', 'changing', 'check', 'clean', 'code', 'coding', 'commit', 'config', 'construct', 'contribute', 'contributing', 'contribution', 'copyright', 'correct', 'database', 'debug', 'decode', 'decoding', 'depend', 'deploy', 'deprecate', 'deprecating', 'description', 'discover', 'document', 'driver', 'encode', 'encoding', 'error ', 'escape', 'escaping', 'exception', 'exit', 'export', 'feedback', 'file', 'filter ', 'fix', 'force ', 'forcing', 'fork', 'format', 'handle', 'handling', 'identification', 'identify', 'ignore', 'ignoring', 'implement', 'import ', 'initial', 'insert', 'install', 'integrate', 'integrating', 'interrupt', 'iterate', 'iterating', 'iteration', 'kernel', 'launch ', 'license', 'licensing', 'lock', 'logic', 'logs', 'loop', 'make', 'manifest', 'merge', 'merging', 'missed', 'missing', 'mode', 'module', 'move', 'namespace', 'new', 'null', 'optimise', 'optimising', 'optimize', 'optimizing', 'overload', 'override', 'overriding', 'param', 'plugin', 'privacy', 'props', 'publish', 'pull ', 'query', 'random', 'redundance', 'redundant', 'refactor', 'reference', 'referencing', 'release', 'releasing', 'remote', 'remove ', 'removing', 'replace', 'replacing', 'report', 'request', 'resolve', 'resolving', 'restore', 'restoring', 'revert', 'review', 'roll', 'scan', 'search', 'secure', 'security', 'serial', 'signature', 'stream', 'support', 'sync', 'test', 'test', 'thread', 'threshold', 'timeout', 'token', 'tool ', 'trace ', 'tracing', 'track', 'tranlating', 'translate', 'trigger', 'truncate', 'truncating', 'truncation', 'unit ', 'update', 'updating', 'upgrade', 'upgrading', 'url', 'utf', 'version','#1','#2','#3','#4','#5','#6','#7','#8','#9','#0']         
            for commits in stream:
                commits = commits.lower()
                flag = False
                for ab in keywords:
                    if(ab in commits):
                        num_core_commits += 1
                        #print("core_commit: ",commits)
                        flag = True
                        break
                if(flag):
                    continue
                else:
                    flag2 = False
                    for ab in Dirs:
                        if(ab in commits):
                            num_core_commits += 1
                            #print("core_commit: ",commits)
                            flag2 = True
                            break
                    if(flag2):
                        continue
                    else:
                        for ab in Files:
                            if(ab in commits):
                                num_core_commits += 1
                                #print("core_commit: ",commits)
                                break
                trim_commit = commits.replace("."," ")
                trim_commit = commits.replace("?"," ")
                trim_commit = commits.replace("/"," ")
                trim_commit = commits.replace("'"," ")
                trim_commit = commits.replace('"'," ")
                trim_commit = commits.replace('@'," ")
                trim_commit = commits.replace('$'," ")
                trim_commit = commits.replace('%'," ")
                trim_commit = commits.replace('^'," ")
                trim_commit = commits.replace('&'," ")
                trim_commit = commits.replace('('," ")
                trim_commit = commits.replace(')'," ")
                trim_commit = commits.replace('['," ")
                trim_commit = commits.replace(']'," ")
                trim_commit = commits.replace('{'," ")
                trim_commit = commits.replace('}'," ")
                trim_commit = commits.replace('_'," ")
                trim_commit = commits.replace('-'," ")
                trim_commit = commits.replace(","," ")
                trim_commit = commits.replace(":","")
                trim_commit = commits.replace("\""," ")
                trim_commit = commits.replace("!"," ")
                trim_commit = commits.replace("â€œ"," ")
                trim_commit = commits.replace("â€˜"," ")
                trim_commit = commits.replace("*"," ")
                spell = SpellChecker()
                misspelled = spell.unknown(trim_commit)
                if(len(list(misspelled)) == 0):
                    print('trim_commit: ',trim_commit)
                    num_core_commits += 1
                #print('Non-Core_commit: ',commits)
            print('core commits: ',num_core_commits)
            commits_ratio = 0
            if(totalNumberOfCommits > 0):
                commits_ratio = float(num_core_commits)/float(totalNumberOfCommits*1.0)
            break
    threshold = options['threshold']
    return (commits_ratio >= threshold, commits_ratio)
if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
