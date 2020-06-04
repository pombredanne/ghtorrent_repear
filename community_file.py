# 75356963
import mysql.connector
import os
import os as inner_os
ghtorrentDb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ghtorrent"
)
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
project_id = 73853368
cursor = ghtorrentDb.cursor()
cursor.execute("SELECT name FROM projects WHERE id={0}".format(project_id))
repoName = cursor.fetchone()[0]
print(repoName)
os.chdir("path/"+str(project_id)+"/")
print(os.getcwd())
for repos in os.listdir():
    if(repos == repoName):
        inner_os.chdir(repos)
        stream = removeNonAscii(os.popen('git shortlog -s -n').read()).split("\n")
        commitList = []
        totalNumberOfCommits = 0
        for commits in stream:
            print(commits)
            commits.encode('UTF-8')
            commit = commits.replace(" ","")
            if(len(commit) > 0):
                commitList.append(int(commit.split("\t")[0]))
                totalNumberOfCommits += int(commit.split("\t")[0])
        totalNumberOfCommits = (totalNumberOfCommits*4)/5
        commitList.sort(reverse=True)
        #print('len: ',len(commitList))
        count = 0
        core_contributors = 0
        for commits in commitList:
            if(count > totalNumberOfCommits):
                break
            count += commits
            core_contributors += 1
        print('core contributors: ',core_contributors)
        break
             
# 75356963
# import os
# import os as inner_os
# repoName = "linguist"
# print(repoName)
# os.chdir("../../path/")
# print(os.getcwd())
# for repos in os.listdir():
#     if(repos == repoName):
#         inner_os.chdir(repos)
#         stream = os.popen('git shortlog -s -n').read().split("\n")
#         commitList = []
#         totalNumberOfCommits = 0
#         for commits in stream:
#             commit = commits.replace(" ","")
#             if(len(commit) > 0):
#                 commitList.append(int(commit.split("\t")[0]))
#                 totalNumberOfCommits += int(commit.split("\t")[0])
#         totalNumberOfCommits = (totalNumberOfCommits*4)/5
#         commitList.sort(reverse=True)
#         print('len: ',len(commitList))
#         count = 0
#         core_contributors = 0
#         for commits in commitList:
#             if(count > totalNumberOfCommits):
#                 break
#             count += commits
#             core_contributors += 1
#         print('core contributors: ',core_contributors)
#         break
             
