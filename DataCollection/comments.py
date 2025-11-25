import time

from python_graphql_client import GraphqlClient
import json
import pymongo
import csv


clientMongo = pymongo.MongoClient("localhost", 27017)
db = clientMongo.COLETA
client = GraphqlClient(endpoint="https://api.github.com/graphql")

numberDiscussion=0
numbers=[]

def make_query(after_cursor=None):
    query="""
    {rateLimit {
                    limit
                    cost
                    remaining
                    resetAt
                }
    repository(name: nameProject, owner:ownerProject) {
            discussion(number:numberDiscussion){                            
                number
                  comments(first: 1, after:AFTER){
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges{
                      node{
                        author{
                          login
                        }
                        authorAssociation
                        body
                        bodyText
                        createdAt
                        id
                        isAnswer
                        isMinimized
                        lastEditedAt
                        minimizedReason
                        publishedAt
                        url
                        upvoteCount    
                         reactions{
                            totalCount
                        }
                        reactionGroups{              						
                            content
                            users {
                                totalCount
                            }                
                        }         
                  }
                }
              }
            }
          }
      }
    
    """.replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")

    return query


def fetch_releases(oauth_token,ownerProject, nameProject, numberDiscussion):
    repos = []
    releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None
    ownerProject = "\"" + ownerProject + "\""
    nameProject = "\"" + nameProject + "\""
    cont=0

    while has_next_page:
        data = client.execute(
            query=make_query(after_cursor).replace("ownerProject", ownerProject).replace("nameProject", nameProject).replace("numberDiscussion",numberDiscussion),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        if data["data"]["rateLimit"]["remaining"]<=1:
            time.sleep(1800)
            print("waiting...")
        else:
            discussion={}
            print("==============================================================================================")
           
            print(ownerProject.replace("\"", ""),"--", nameProject.replace("\"", ""))
            if data["data"]["repository"]["discussion"] is None:
                break
            if len(data["data"]["repository"]["discussion"]["comments"]["edges"])==0:
                break
            if data["data"]["repository"]["discussion"] != None and len(data["data"]["repository"]["discussion"]["comments"]["edges"])!=0:
                discussion['owner'] = ownerProject.replace("\"", "")
                discussion['project'] = nameProject.replace("\"", "")
                print(data["data"]["repository"]["discussion"]["number"])

                discussion['numberDiscussion'] = data["data"]["repository"]["discussion"]["number"]
                if data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["author"] is None:
                    discussion["author"]="None"
                else:
                    discussion["author"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["author"]["login"]
                if data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["authorAssociation"] is None:
                    discussion["authorAssociation"]="None"
                else:
                    discussion["authorAssociation"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["authorAssociation"]
                discussion["body"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["body"]
                discussion["bodyText"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["bodyText"]
                discussion["createdAt"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["createdAt"]
                discussion["isAnswer"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["isAnswer"]
                discussion["isMinimized"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["isMinimized"]
                discussion["lastEditedAt"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["lastEditedAt"]
                discussion["minimizedReason"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["minimizedReason"]
                discussion["publishedAt"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["publishedAt"]
                discussion["url"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["url"]
                discussion["upvoteCount"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["upvoteCount"]
                discussion["reactionsTotal"] = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["reactions"]["totalCount"]
                discussion['THUMBS_UP'] = 0
                discussion['THUMBS_DOWN'] = 0
                discussion['LAUGH'] = 0
                discussion['HOORAY'] = 0
                discussion['CONFUSED'] = 0
                discussion['HEART'] = 0
                discussion['ROCKET'] = 0
                discussion['EYES'] = 0
                comment=data["data"]["repository"]["discussion"]["comments"]["edges"][0]
                for reactions in comment["node"]["reactionGroups"]:
                    
                    if reactions["content"] == "THUMBS_UP":
                        discussion['THUMBS_UP'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "THUMBS_DOWN":
                        discussion['THUMBS_DOWN'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "LAUGH":
                        discussion['LAUGH'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "HOORAY":
                        discussion['HOORAY'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "CONFUSED":
                        discussion['CONFUSED'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "HEART":
                        discussion['HEART'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "ROCKET":
                        discussion['ROCKET'] = reactions["users"]["totalCount"]
                    if reactions["content"] == "EYES":
                        discussion['EYES'] = reactions["users"]["totalCount"]
                db.comments.insert_one(discussion)

                has_next_page = data["data"]["repository"]["discussion"]["comments"]["pageInfo"]["hasNextPage"]
                after_cursor = data["data"]["repository"]["discussion"]["comments"]["pageInfo"]["endCursor"]
            cont+=1
    return releases

def runAllProjects():
    with open('COLETAdiscussions.csv', newline='',
              encoding="mbcs") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (row[1] != "owner"):
                fetch_releases("token", row[1], row[2],row[0])

runAllProjects()
