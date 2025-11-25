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
        if row[0]!= "owner_name" and row[0] not in repos:
            repos += [row[0]]
print(repos)
print(len(repos))

core=[]
peripheral=[]
issues=[]
discussions=[]

answered_by_core=["answered by core"]
answered_by_periphery=["answered by peripheral"]
answered_by_issues=["answered by issues"]
answered_by_others=["answered by discussions"]
answered_by_author=["answered by author"]

cont_answered_core_by_core=0
cont_answered_core_by_periphery=0
cont_answered_core_by_issues=0
cont_answered_core_by_others=0
cont_answered_core_by_author=0

cont_answered_periphery_by_core=0
cont_answered_periphery_by_periphery=0
cont_answered_periphery_by_issues=0
cont_answered_periphery_by_others=0
cont_answered_periphery_by_author=0

cont_answered_issues_by_core=0
cont_answered_issues_by_periphery=0
cont_answered_issues_by_issues=0
cont_answered_issues_by_others=0
cont_answered_issues_by_author=0

cont_answered_others_by_core=0
cont_answered_others_by_periphery=0
cont_answered_others_by_issues=0
cont_answered_others_by_others=0
cont_answered_others_by_author=0

cont = 0

with open('C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/RespondentsOfSelectedAnswers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["", "core", "peripheral", "issues", "discussions"])
    for i in range(len(repos)):
        repo = repos[i].split("/")
        owner = repo[0]
        name = repo[1]
        print("******************************************************************************")
        print(name)

        core = []
        peripheral = []
        issues = []
        discussions = []

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

        if len(core)!=0:
            repo = repos[i].split("/")
            owner = repo[0]
            name = repo[1]
            print("*************************************************")
            print(name)
            totalDiscussions = 0
            for item in dbDiscussions.find({'owner': owner,'project': name}):
                totalDiscussions = totalDiscussions + 1


            # teste = db.find({'project': name, 'answerChosenBy': {'$not: {null'}})
            # print(teste)
            for item in dbDiscussions.find({'owner': owner,'project': name,'answerChosenBy':{'$ne':None}}):
                # print("==============================")
                # print(item)
                print(item['answerChosenBy'])
                cont = cont + 1

                if item['author'] in core:
                    if item['answerChosenBy'] == item['author']:
                        cont_answered_core_by_author=cont_answered_core_by_author+1
                    if item['answerChosenBy'] in core:
                        cont_answered_core_by_core=cont_answered_core_by_core+1
                    elif item['answerChosenBy'] in peripheral:
                        cont_answered_core_by_periphery=cont_answered_core_by_periphery+1
                    elif item['answerChosenBy'] in issues:
                        cont_answered_core_by_issues=cont_answered_core_by_issues+1
                    elif item['answerChosenBy'] in discussions:
                        cont_answered_core_by_others=cont_answered_core_by_others+1
                elif item['author'] in peripheral:
                    if item['answerChosenBy'] == item['author']:
                        cont_answered_periphery_by_author=cont_answered_periphery_by_author+1
                    if item['answerChosenBy'] in core:
                        cont_answered_periphery_by_core=cont_answered_periphery_by_core+1
                    elif item['answerChosenBy'] in peripheral:
                        cont_answered_periphery_by_periphery=cont_answered_periphery_by_periphery+1
                    elif item['answerChosenBy'] in issues:
                        cont_answered_periphery_by_issues=cont_answered_periphery_by_issues+1
                    elif item['answerChosenBy'] in discussions:
                        cont_answered_periphery_by_others=cont_answered_periphery_by_others+1
                elif item['author'] in issues:
                    if item['answerChosenBy'] == item['author']:
                        cont_answered_issues_by_author=cont_answered_issues_by_author+1
                    if item['answerChosenBy'] in core:
                        cont_answered_issues_by_core=cont_answered_issues_by_core+1
                    elif item['answerChosenBy'] in peripheral:
                        cont_answered_issues_by_periphery=cont_answered_issues_by_periphery+1
                    elif item['answerChosenBy'] in issues:
                        cont_answered_issues_by_issues=cont_answered_issues_by_issues+1
                    elif item['answerChosenBy'] in discussions:
                        cont_answered_issues_by_others=cont_answered_issues_by_others+1
                elif item['author'] in discussions:
                    if item['answerChosenBy'] == item['author']:
                        cont_answered_others_by_author=cont_answered_others_by_author+1
                    if item['answerChosenBy'] in core:
                        cont_answered_others_by_core=cont_answered_others_by_core+1
                    elif item['answerChosenBy'] in peripheral:
                        cont_answered_others_by_periphery=cont_answered_others_by_periphery+1
                    elif item['answerChosenBy'] in issues:
                        cont_answered_others_by_issues=cont_answered_others_by_issues+1
                    elif item['answerChosenBy'] in discussions:
                        cont_answered_others_by_others=cont_answered_others_by_others+1

    print(cont)

    answered_by_core += [cont_answered_core_by_core,cont_answered_periphery_by_core,cont_answered_issues_by_core,cont_answered_others_by_core]
    answered_by_periphery += [cont_answered_core_by_periphery,cont_answered_periphery_by_periphery,cont_answered_issues_by_periphery,cont_answered_others_by_periphery]
    answered_by_issues += [cont_answered_core_by_issues,cont_answered_periphery_by_issues,cont_answered_issues_by_issues,cont_answered_others_by_issues]
    answered_by_others += [cont_answered_core_by_others,cont_answered_periphery_by_others,cont_answered_issues_by_others,cont_answered_others_by_others]
    answered_by_author += [cont_answered_core_by_author,cont_answered_periphery_by_author,cont_answered_issues_by_author,cont_answered_others_by_author]

    writer.writerows([answered_by_core])
    writer.writerows([answered_by_periphery])
    writer.writerows([answered_by_issues])
    writer.writerows([answered_by_others])
    writer.writerows([answered_by_author])