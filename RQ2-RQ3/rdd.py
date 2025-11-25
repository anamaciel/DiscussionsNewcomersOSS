import csv
import collections
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pymongo
from statistics import median

repos=[]
firstDates=[]

clientMongo = pymongo.MongoClient("localhost", 27017)
db = clientMongo.COLETA['repos']
dbIssues = clientMongo.COLETA['issues']
dbPulls = clientMongo.COLETA['pulls']
dbDiscussions = clientMongo.COLETA['discussions']
dbComments = clientMongo.COLETA['comments']
dbReplies = clientMongo.COLETA['replies']

with open('discussions_allprojects.csv',
          newline='', encoding="mbcs") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        #print(row)
        if row[0]!= "repo_name" and row[0] not in repos: 
            repos += [row[0]]
print(repos)
print(len(repos))

for repo in repos:
    first=False
    primeiraData=datetime.strptime("2016-11-01 00:00:00","%Y-%m-%d %H:%M:%S")
    menorData = datetime.strptime("2022-08-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    with open('discussions_allprojects.csv',
              newline='', encoding="mbcs") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if row[0] == repo:
                if row[6] == "False" and row[4] != "":
                    dataa = row[4]
                    dataa = dataa.replace("T", " ")
                    dataa = dataa.replace("Z", "")
                    primeiraData = datetime.strptime(dataa, "%Y-%m-%d %H:%M:%S")
                    if primeiraData < menorData:
                        menorData = primeiraData
        firstDates += [menorData]
        print(firstDates)
        print(len(firstDates))

owner=""
name=""
lang=""
pr=0
issues=0
datasIniciais=[datetime.strptime("2016-11-01 00:00:00","%Y-%m-%d %H:%M:%S")]*25
datasFinais = [datetime.strptime("2016-11-01 00:00:00", "%Y-%m-%d %H:%M:%S")] * 25

with open('dadosRDD.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["owner","name","month_start","month_end","time","intervention","time_after_intervention","time_issues_closed","merged","nonmerged","new_users_issues","new_users_pulls","users_issues","users_pulls","lang","pr_total","issues_total","pr_per_month","issues_per_month","total_number_pr_authors","total_number_issues_authors","agePulls","ageIssues"])
    for i in range(len(repos)):
        repo=repos[i].split("/")
        owner=repo[0]
        name=repo[1]
        print("*************************************************")
        print(name)
        for item in db.find({'name': name}):
            lang=item['language']
            pr=item['pulls_count']
            issues=item['issues_count']

        dataBase = firstDates[i]
        dataBase = firstDates[i] + relativedelta(days=15)
        month_start = firstDates[i] + relativedelta(days=-360)
        month_end = dataBase + relativedelta(days=+360)
        time=0
        time_zero=0
        time_after_intervention=0
        intervention=False

        vet_users_issues = []
        vet_users_pulls = []

        datasIniciais[12] = firstDates[i] - relativedelta(days=15)
        datasFinais[12] = firstDates[i] + relativedelta(days=15)


        month_start = datasIniciais[12]
        month_end = datasIniciais[12]

        for x in range(11, -1, -1):
            month_end = month_start - relativedelta(days=1)
            month_start = month_end - relativedelta(days=30)
            datasIniciais[x] = month_start
            datasFinais[x] = month_end
			
        month_start = datasIniciais[12]
        month_end = datasFinais[12]

        print(month_start, '=====', month_end)

        for x in range(13, 25):
            month_start = month_end + relativedelta(days=1)
            month_end = month_end + relativedelta(days=30)
            datasIniciais[x] = month_start
            datasFinais[x] = month_end

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(len(datasIniciais), '---', len(datasFinais))
        for y in range(len(datasIniciais)):
            print(datasIniciais[y], "-", datasFinais[y])

        print("month_start:", datasIniciais[0])
        print("month_end:", datasFinais[0])

        total_number_pr_authors = 0
        vet_total_number_pr_authors = []

        for item in dbPulls.find(
                {'created_at': {'$lt': dataBase.isoformat()}, 'name': name}):
            if item['user'] not in vet_total_number_pr_authors:
                vet_total_number_pr_authors += [item['user']]
            total_number_pr_authors = len(vet_total_number_pr_authors)

        # total_number_issues_authors
        total_number_issues_authors = 0
        vet_total_number_issues_authors = []

        for item in dbIssues.find(
                {'created_at': {'$lt': dataBase.isoformat()}, 'name': name}):
            if item['user_login'] not in vet_total_number_issues_authors:
                vet_total_number_issues_authors += [item['user_login']]
            total_number_issues_authors = len(vet_total_number_issues_authors)

        # age pulls
        # print("*********************************************")

        primeiraPull = dbPulls.find_one({'name': name}, sort=[("created_at", 1)])["created_at"]
        primeiraDiscussion = str(dataBase)
        # print(primeiraDiscussion)
        primeiraPull = primeiraPull.replace("T", " ")
        primeiraPull = primeiraPull.replace("Z", "")
        dataPrimeiraPull = datetime.strptime(primeiraPull, "%Y-%m-%d %H:%M:%S")
        
        dataPrimeiraDiscussion = datetime.strptime(primeiraDiscussion, "%Y-%m-%d %H:%M:%S")

        agePulls = dataPrimeiraDiscussion - dataPrimeiraPull
        agePulls = int(agePulls.days / 30)
        

        # age issues
        # print("*********************************************")

        primeiraIssue = dbIssues.find_one({'name': name}, sort=[("created_at", 1)])["created_at"]
        primeiraDiscussion = str(dataBase)
        primeiraIssue = primeiraIssue.replace("T", " ")
        primeiraIssue = primeiraIssue.replace("Z", "")
        dataPrimeiraIssue = datetime.strptime(primeiraIssue, "%Y-%m-%d %H:%M:%S")
        dataPrimeiraDiscussion = datetime.strptime(primeiraDiscussion, "%Y-%m-%d %H:%M:%S")

        ageIssues = dataPrimeiraDiscussion - dataPrimeiraIssue
        ageIssues = int(ageIssues.days / 30)
       

        for j in range(25):
            month_start = datasIniciais[j]
            month_end = datasFinais[j]
            intervention = False
            #print(j)

            dias_mediana = []
            for item in dbIssues.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name,
                     'state': 'closed'}):
                abertura = item['created_at']
                fechamento = item['closed_at']
                abertura = abertura.replace("T", " ")
                abertura = abertura.replace("Z", "")
                fechamento = fechamento.replace("T", " ")
                fechamento = fechamento.replace("Z", "")
                dataAbertura = datetime.strptime(abertura, "%Y-%m-%d %H:%M:%S")
                dataFechamento = datetime.strptime(fechamento, "%Y-%m-%d %H:%M:%S")
                dif = dataFechamento - dataAbertura
                
                dias_mediana += [dif.days]
            
            if len(dias_mediana) > 0:
                time_issues_closed = median(dias_mediana)
            else:
                time_issues_closed = 0
            

            # merged
            merged = 0
            for item in dbPulls.find({'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'merged_at':{'$ne': None}, 'name': name}):
                merged = merged + 1

            # merged
            nonmerged = 0
            for item in dbPulls.find({'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()},'merged_at': None, 'name': name}):
                    nonmerged = nonmerged + 1

            # new_users_issues

            new_users_issues = 0
            vet_new_users_issues = []
            for item in dbIssues.find(
                    {'created_at': {'$lt': month_start.isoformat()}, 'name': name}):
                if item['user_login'] not in vet_users_issues:
                    vet_users_issues += [item['user_login']]

            for item in dbIssues.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name}):
                if item['user_login'] not in vet_users_issues:
                    new_users_issues = new_users_issues + 1
                    vet_users_issues += [item['user_login']]
                    vet_new_users_issues += [item['user_login']]

            # new_users_pulls
            new_users_pulls = 0
            vet_new_users_issues = []

            for item in dbPulls.find(
                    {'created_at': {'$lt': month_start.isoformat()}, 'name': name}):
                if item['user'] not in vet_users_pulls:
                    vet_users_pulls += [item['user']]

            for item in dbPulls.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name}):
                if item['user'] not in vet_users_pulls:
                    new_users_pulls = new_users_pulls + 1
                    vet_users_pulls += [item['user']]

            # users_issues
            vet_users_issues_month = []
            users_issues = 0

            for item in dbIssues.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()},'name': name}):
                if item['user_login'] not in vet_users_issues_month:
                    users_issues = users_issues + 1
                    vet_users_issues_month += [item['user_login']]

            #users_pulls
            vet_users_pull_month = []
            users_pulls = 0

            for item in dbPulls.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name}):
                if item['user'] not in vet_users_pull_month:
                    users_pulls = users_pulls + 1
                    vet_users_pull_month += [item['user']]


            #issues_per_month

            issues_per_month = 0
            for item in dbIssues.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name}):
                issues_per_month = issues_per_month + 1

            #pr_per_month
            pr_per_month = 0
            for item in dbPulls.find(
                    {'created_at': {'$lt': month_end.isoformat(), '$gte': month_start.isoformat()}, 'name': name}):
                pr_per_month = pr_per_month + 1

            if month_start==datasIniciais[12]:
                intervention=True
            if intervention:
                print(
                    owner, name, month_start, month_end, 0, "TRUE", time_after_intervention,
                    time_issues_closed, merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr,issues,pr_per_month,issues_per_month,
                    total_number_pr_authors, total_number_issues_authors, agePulls, ageIssues)
                writer.writerow([owner, name, month_start, month_end, 0, "TRUE", time_after_intervention,
                    time_issues_closed,merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr,issues,pr_per_month,issues_per_month,
                    total_number_pr_authors, total_number_issues_authors, agePulls, ageIssues])
            else:
                time = time + 1
                if month_start<datasIniciais[12]:
                    print(owner, name, month_start, month_end, time, "FALSE", time_after_intervention,
                         time_issues_closed, merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr, issues,pr_per_month,issues_per_month,
                         total_number_pr_authors, merged, nonmerged, total_number_issues_authors, agePulls, ageIssues)
                    writer.writerow([owner, name, month_start, month_end, time, "FALSE", time_after_intervention,
                         time_issues_closed,merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr,issues,pr_per_month,issues_per_month,
                         total_number_pr_authors, total_number_issues_authors, agePulls, ageIssues])
                elif month_start>datasIniciais[12]:
                    time_after_intervention=time_after_intervention+1
                    print(owner, name, month_start, month_end, time, "TRUE", time_after_intervention,
                        time_issues_closed,merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr, issues,pr_per_month,issues_per_month,
                        total_number_pr_authors, total_number_issues_authors, agePulls, ageIssues)
                    writer.writerow([owner, name, month_start, month_end, time, "TRUE", time_after_intervention,
                        time_issues_closed,merged, nonmerged, new_users_issues, new_users_pulls, users_issues, users_pulls, lang, pr,issues,pr_per_month,issues_per_month,
                        total_number_pr_authors, total_number_issues_authors, agePulls, ageIssues])