import time

from python_graphql_client import GraphqlClient
import json
import pymongo
import csv

clientMongo = pymongo.MongoClient("localhost", 27017)
db = clientMongo.COLETA
client = GraphqlClient(endpoint="https://api.github.com/graphql")

numberDiscussion = 0
numbers = []

def make_query(after_cursor=None):
    query = """
    {rateLimit {
                    limit
                    cost
                    remaining
                    resetAt
                }
    repository(name: nameProject, owner: ownerProject) {
            discussion(number:numberDiscussion){
                number
                  comments(first: 1, after:AFTER){
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges{
                        node{
                        replies(first:100){
                            edges{
                            node{
                              author{
                                login
                              }
                              authorAssociation
                              body
                              bodyText
                              createdAt
                              isAnswer
                              isMinimized
                              minimizedReason
                              publishedAt
                              url
                              replyTo{
                                author{
                                  login
                                }
                              }
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
            }
      }
}
    """.replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")

    return query


def fetch_releases(oauth_token, ownerProject, nameProject, numberDiscussion):
    repos = []
    releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None

    ownerProject = "\"" + ownerProject + "\""
    nameProject = "\"" + nameProject + "\""
    cont = 0

    
    while has_next_page:
        
        data = client.execute(
            query=make_query(after_cursor).replace("ownerProject", ownerProject).replace("nameProject", nameProject).replace("numberDiscussion",numberDiscussion),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        
        if data["data"]["rateLimit"]["remaining"] <= 1:
            print("waiting...")
            time.sleep(1800)
        else:
            print()
            discussion = {}
            if data["data"]["repository"]["discussion"] is None:
                break
            if len(data["data"]["repository"]["discussion"]["comments"]["edges"]) == 0:
                break
            if data["data"]["repository"]["discussion"] != None and len(
                    data["data"]["repository"]["discussion"]["comments"]["edges"]) != 0:
                print("************************************************************************************************")
                print(data["data"]["repository"]["discussion"]["number"])
                print(ownerProject.replace("\"", ""),"--",nameProject.replace("\"", ""))
                
				replies = data["data"]["repository"]["discussion"]["comments"]["edges"][0]["node"]["replies"]["edges"]
                for reply in replies:
                    discussion['numberDiscussion'] = data["data"]["repository"]["discussion"]["number"]
                    discussion['owner'] = ownerProject.replace("\"", "")
                    discussion['project'] = nameProject.replace("\"", "")
                    if reply["node"]["author"] != None:
                        discussion["author"] = reply["node"]["author"]["login"]
                    else:
                        discussion["author"] = None
                    discussion["authorAssociation"] = reply["node"]["authorAssociation"]
                    discussion["body"] = reply["node"]["body"]
                    discussion["bodyText"] = reply["node"]["bodyText"]
                    discussion["createdAt"] = reply["node"]["createdAt"]
                    discussion["isAnswer"] = reply["node"]["isAnswer"]
                    discussion["isMinimized"] = reply["node"]["isMinimized"]
                    discussion["minimizedReason"] = reply["node"]["minimizedReason"]
                    discussion["publishedAt"] = reply["node"]["publishedAt"]
                    discussion["url"] = reply["node"]["url"]
                    if reply["node"]["replyTo"]["author"] != None:
                        discussion["replyTo"] = reply["node"]["replyTo"]["author"]["login"]
                    else:
                        discussion["replyTo"] = None
                    discussion["upvoteCount"] = reply["node"]["upvoteCount"]
                    discussion["reactionsTotal"] = reply["node"]["reactions"]["totalCount"]
                    discussion['THUMBS_UP'] = 0
                    discussion['THUMBS_DOWN'] = 0
                    discussion['LAUGH'] = 0
                    discussion['HOORAY'] = 0
                    discussion['CONFUSED'] = 0
                    discussion['HEART'] = 0
                    discussion['ROCKET'] = 0
                    discussion['EYES'] = 0
                    for reactions in reply["node"]["reactionGroups"]:
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
                    db.replies.insert_one(discussion)
                    discussion = {}

            has_next_page = data["data"]["repository"]["discussion"]["comments"]["pageInfo"]["hasNextPage"]
            after_cursor = data["data"]["repository"]["discussion"]["comments"]["pageInfo"]["endCursor"]

            cont += 1
    return releases


def runAllProjects():
    with open('projectsDiscussions.csv', newline='',
              encoding="mbcs") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            
            if (row[1] != "owner"):
                fetch_releases("token", row[1], row[2],row[0])

runAllProjects()
