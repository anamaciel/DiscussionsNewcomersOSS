import csv
import collections
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pymongo

repos=[]

clientMongo = pymongo.MongoClient("localhost", 27017)

dbDiscussions = clientMongo.Base2024['discussions']
dbComments = clientMongo.Base2024['comments']
dbReplies = clientMongo.Base2024['replies']
dbIssues = clientMongo.Base2024['issues']
dbPulls = clientMongo.Base2024['pulls']
dbCommits = clientMongo.Base2024['commits']
dbUsersCores = clientMongo.Base2024['usersRoles']

dbDiscussions.create_index([('owner', pymongo.ASCENDING),('project', pymongo.ASCENDING),('author', pymongo.ASCENDING),('createdAt', pymongo.ASCENDING)])
dbComments.create_index([('owner', pymongo.ASCENDING),('project', pymongo.ASCENDING),('author', pymongo.ASCENDING),('createdAt', pymongo.ASCENDING)])
dbReplies.create_index([('owner', pymongo.ASCENDING),('project', pymongo.ASCENDING),('author', pymongo.ASCENDING),('createdAt', pymongo.ASCENDING)])
dbIssues.create_index([('owner', pymongo.ASCENDING),('name', pymongo.ASCENDING),('user_login', pymongo.ASCENDING)])
dbPulls.create_index([('owner', pymongo.ASCENDING),('name', pymongo.ASCENDING),('user', pymongo.ASCENDING)])


with open('C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/repos/repos.csv',
          newline='', encoding="mbcs") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        #print(row)

        if row[0]!= "owner_name" and row[0] not in repos:
            repos += [row[0]]
print(repos)
print(len(repos))

core=[]
peripheral=[]
issues=[]
discussions=[]

with open('C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/commentsRepliesPerROLEPercent.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Core developers","Peripheral developers","Issues reporters","Discussions contributors"])
    for i in range(len(repos)):
        core = []
        peripheral = []
        issues = []
        discussions = []
        repo = repos[i].split("/")
        owner = repo[0]
        name = repo[1]
        print("******************************************************************************")
        print(name)
        for item in dbUsersCores.find({'owner': owner, 'project': name, 'role': 'core'}):
            core += [item['login']]

        for item in dbPulls.find({'owner': owner, 'name': name}):
            if item['user'] not in core and item['user'] not in peripheral:
                peripheral += [item['user']]

        for item in dbIssues.find({'owner': owner, 'name': name}):
            if item['user_login'] not in core and item['user_login'] not in peripheral and item['user_login'] not in issues:
                issues += [item['user_login']]

        for item in dbDiscussions.find({'owner': owner, 'project': name}):
            if item['author'] not in core and item['author'] not in peripheral and item['author'] not in issues and item['author'] not in discussions:
                discussions += [item['author']]

        for item in dbComments.find({'owner': owner, 'project': name}):
            if item['author'] not in core and item['author'] not in peripheral and item['author'] not in issues and item['author'] not in discussions:
                discussions += [item['author']]

        for item in dbReplies.find({'owner': owner, 'project': name}):
            if item['author'] not in core and item['author'] not in peripheral and item['author'] not in issues and item['author'] not in discussions:
                discussions += [item['author']]

        print(owner, name, len(core), len(peripheral), len(issues), len(discussions))

        contCore=0
        contPeripheral=0
        contIssues=0
        contOthers=0
        contALL=0

        for item in dbComments.find({'owner': owner,'project':name}):
            if item['author'] in core or item['author'] in peripheral or item['author'] in issues or item['author'] in discussions:
                contALL = contALL+1

        for item in dbReplies.find({'owner': owner,'project':name}):
            if item['author'] in core or item['author'] in peripheral or item['author'] in issues or item['author'] in discussions:
                contALL = contALL + 1

        for item in dbComments.find({'owner': owner,'project': name}):
            if item['author'] in core:
                contCore=contCore+1
            if item['author'] in peripheral:
                contPeripheral=contPeripheral+1
            if item['author'] in issues:
                contIssues=contIssues+1
            if item['author'] in discussions:
                contOthers=contOthers+1

        for item in dbReplies.find({'owner': owner,'project': name}):
            if item['author'] in core:
                contCore = contCore + 1
            if item['author'] in peripheral:
                contPeripheral = contPeripheral + 1
            if item['author'] in issues:
                contIssues = contIssues + 1
            if item['author'] in discussions:
                contOthers = contOthers + 1

        print("TUDO:",contALL)
        print("contCore:", contCore)
        print("contPeripheral:", contPeripheral)
        print("contIssues:", contIssues)
        print("contOthers:", contOthers)
        print("TUDO:", contALL,"-",contCore+contPeripheral+contIssues+contOthers)


        percCore = (contCore*100)/contALL
        percPeripheral = (contPeripheral*100)/contALL
        percIssues = (contIssues*100)/contALL
        percOthers = (contOthers*100)/contALL

        print(percCore,percPeripheral,percIssues,percOthers)
        writer.writerow([percCore,percPeripheral,percIssues,percOthers])







