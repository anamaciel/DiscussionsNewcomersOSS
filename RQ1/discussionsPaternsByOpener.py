import csv
import collections
from datetime import datetime
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

has_selected_answer=["Has selected answer"]
no_selected_answer=["No selected answer"]
no_response=["No response"]
by_author=["Answered by author"]

cont_has_selected_answer_core=0
cont_no_selected_answer_core=0
cont_no_response_core=0
cont_by_author_core=0

cont_has_selected_answer_others=0
cont_no_selected_answer_others=0
cont_no_response_others=0
cont_by_author_others=0

cont_has_selected_answer_peripheral=0
cont_no_selected_answer_peripheral=0
cont_no_response_peripheral=0
cont_by_author_peripheral=0

cont_has_selected_answer_issues=0
cont_no_selected_answer_issues=0
cont_no_response_issues=0
cont_by_author_issues=0

cont2=0

with open('C:/Users/anacm/Documents/DOUTORADO/GITHUB/Scripts/2024/PacoteReplicacao/RQ1/DiscussionPatternsByQuestioners.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["","core","peripheral","issues","discussions"])



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


        totalDiscussions=0
        answered=0
        comments=0
        replies=0

        for item in dbDiscussions.find({'owner': owner,'project': name}):
            totalDiscussions=totalDiscussions+1

        for item2 in dbDiscussions.find({'owner': owner,'project': name, 'answerChosenBy': {'$ne': None}}):
            cont2 = cont2 + 1
            if item2['author'] in core:
                cont_has_selected_answer_core = cont_has_selected_answer_core + 1
            elif item2['author'] in peripheral:
                cont_has_selected_answer_peripheral = cont_has_selected_answer_peripheral + 1
            elif item2['author'] in issues:
                cont_has_selected_answer_issues = cont_has_selected_answer_issues + 1
            elif item2['author'] in discussions:
                cont_has_selected_answer_others = cont_has_selected_answer_others + 1


        for item in dbDiscussions.find({'owner': owner,'project': name}):
            #print("==============================")
            #print(item)
            print(item['answerChosenBy'])
            contReplies = 0

            for itemReply in dbComments.find({'owner': owner,'project': name, 'numberDiscussion': item['number']}):
                contReplies = contReplies + 1

            #print("CONT REPLIES:", contReplies)


            if contReplies == 0:
                #print("entrou cont replies!")
                if item['author'] in core:
                    cont_no_response_core = cont_no_response_core + 1
                elif item['author'] in peripheral:
                    cont_no_response_peripheral = cont_no_response_peripheral + 1
                elif item['author'] in issues:
                    cont_no_response_issues = cont_no_response_issues + 1
                elif item['author'] in discussions:
                    cont_no_response_others = cont_no_response_others + 1
            elif item['answerChosenBy'] is None:
                if item['author'] in core:
                    cont_no_selected_answer_core = cont_no_selected_answer_core + 1
                elif item['author'] in peripheral:
                    cont_no_selected_answer_peripheral = cont_no_selected_answer_peripheral + 1
                elif item['author'] in issues:
                    cont_no_selected_answer_issues = cont_no_selected_answer_issues + 1
                elif item['author'] in discussions:
                    cont_no_selected_answer_others = cont_no_selected_answer_others + 1


        for item in dbDiscussions.find({'owner': owner,'project': name}):
            #print("==============================")
            #print(item)
            print(item['answerChosenBy'])
            contReplies = 0

            for itemComments in dbComments.find({'owner': owner,'project': name, 'numberDiscussion': item['number']}):
                if itemComments['isAnswer']:
                    if item['author']==itemComments['author']:
                        if item['author'] in core:
                            cont_by_author_core = cont_by_author_core + 1
                        elif item['author'] in peripheral:
                            cont_by_author_peripheral = cont_by_author_peripheral + 1
                        elif item['author'] in issues:
                            cont_by_author_issues = cont_by_author_issues + 1
                        elif item['author'] in discussions:
                            cont_by_author_others = cont_by_author_others + 1



    has_selected_answer += [cont_has_selected_answer_core,cont_has_selected_answer_peripheral,cont_has_selected_answer_issues,cont_has_selected_answer_others]
    no_selected_answer += [cont_no_selected_answer_core,cont_no_selected_answer_peripheral,cont_no_selected_answer_issues,cont_no_selected_answer_others]
    no_response += [cont_no_response_core,cont_no_response_peripheral,cont_no_response_issues,cont_no_response_others]
    by_author += [cont_by_author_core,cont_by_author_peripheral,cont_by_author_issues,cont_by_author_others]

    writer.writerows([has_selected_answer])
    writer.writerows([no_selected_answer])
    writer.writerows([no_response])
    writer.writerows([by_author])

