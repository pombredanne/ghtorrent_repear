fp = open("C:/xampp2/htdocs/ghtorrent/reaper/path/73853335/pttg-ip-hmrc-access-code/.drone.yml",'r')
totalNumberOfDependencyLines = 0
for x in fp:
    if("0." in x or "1." in x or "2." in x or "3." in x or "4." in x or "5." in x or "6." in x or "7." in x or "8." in x or "9." in x):
        print(x)
        totalNumberOfDependencyLines += 1
print('totalNumberOfDependencyLines: ',totalNumberOfDependencyLines)