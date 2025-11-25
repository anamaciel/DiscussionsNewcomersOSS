from python_graphql_client import GraphqlClient
import json
import pymongo
import csv
import time


clientMongo = pymongo.MongoClient("localhost", 27017)
db = clientMongo.COLETA
client = GraphqlClient(endpoint="https://api.github.com/graphql")




def make_query(after_cursor=None):
    query = """
{rateLimit {
                limit
                cost
                remaining
                resetAt
            }    
repository(name: nameProject, owner: ownerProject) {
        discussions(first: 1, after:AFTER){
            pageInfo {
                hasNextPage
                endCursor
            }            
            nodes{
                id
                number
                title            
                bodyText
                createdAt
                author{
                     login
                }
                authorAssociation
                category {
                    name
                }
                url
                answerChosenAt
                upvoteCount
                answerChosenBy{
                    login
                }            
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
""".replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")


    return query


def fetch_releases(oauth_token,ownerProject,nameProject):
    repos = []
    releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None
    ownerProject="\""+ownerProject+"\""
    nameProject = "\"" + nameProject + "\""
    

    while has_next_page:
        
        data = client.execute(
            query=make_query(after_cursor).replace("ownerProject",ownerProject).replace("nameProject",nameProject),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        #print("data",data)
        if data["data"]["rateLimit"]["remaining"]<=1:
            time.sleep(1800)
            print("waiting...")
        else:
            print()
            
            print(data)
            
            discussion={}
            print("==============================================================================================")
            
            print(data["data"]["repository"]["discussions"]["nodes"][0]["number"],'--', nameProject.replace("\"", ""))
            
            if data["data"]["repository"]["discussions"]["nodes"][0]["author"]!= None:
                discussion['id']=data["data"]["repository"]["discussions"]["nodes"][0]["id"]
                discussion['number']=data["data"]["repository"]["discussions"]["nodes"][0]["number"]
                discussion['owner']=ownerProject.replace("\"","")
                discussion['project'] = nameProject.replace("\"", "")
                discussion['title']=data["data"]["repository"]["discussions"]["nodes"][0]["title"]
                discussion['bodyText'] = data["data"]["repository"]["discussions"]["nodes"][0]["bodyText"]
                discussion['createdAt']=data["data"]["repository"]["discussions"]["nodes"][0]["createdAt"]
                discussion['author'] = data["data"]["repository"]["discussions"]["nodes"][0]["author"]["login"]
                discussion['authorAssociation'] = data["data"]["repository"]["discussions"]["nodes"][0]["authorAssociation"]
                discussion['category'] = data["data"]["repository"]["discussions"]["nodes"][0]["category"]["name"]
                discussion['url'] = data["data"]["repository"]["discussions"]["nodes"][0]["url"]
                discussion['answerChosenAt']=data["data"]["repository"]["discussions"]["nodes"][0]["answerChosenAt"]
                discussion['upvoteCount']=data["data"]["repository"]["discussions"]["nodes"][0]["upvoteCount"]
                if data["data"]["repository"]["discussions"]["nodes"][0]["answerChosenBy"]!= None:
                    discussion['answerChosenBy']=data["data"]["repository"]["discussions"]["nodes"][0]["answerChosenBy"]["login"]
                else:
                    discussion['answerChosenBy'] = None
                discussion['reactionsTotal']=data["data"]["repository"]["discussions"]["nodes"][0]["reactions"]["totalCount"]
                discussion['THUMBS_UP']=0
                discussion['THUMBS_DOWN']=0
                discussion['LAUGH']=0
                discussion['HOORAY']=0
                discussion['CONFUSED']=0
                discussion['HEART']=0
                discussion['ROCKET']=0
                discussion['EYES']=0
                for reactions in data["data"]["repository"]["discussions"]["nodes"][0]["reactionGroups"]:
                    if reactions["content"]=="THUMBS_UP":
                        discussion['THUMBS_UP']=reactions["users"]["totalCount"]
                    if reactions["content"]=="THUMBS_DOWN":
                        discussion['THUMBS_DOWN'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="LAUGH":
                        discussion['LAUGH'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="HOORAY":
                        discussion['HOORAY'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="CONFUSED":
                        discussion['CONFUSED'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="HEART":
                        discussion['HEART'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="ROCKET":
                        discussion['ROCKET'] = reactions["users"]["totalCount"]
                    if reactions["content"]=="EYES":
                        discussion['EYES'] = reactions["users"]["totalCount"]
                db.discussions.insert_one(discussion)



            has_next_page = data["data"]["repository"]["discussions"]["pageInfo"]["hasNextPage"]
            after_cursor = data["data"]["repository"]["discussions"]["pageInfo"]["endCursor"]
    return releases

def runAllProjects():
    with open('projects.csv',
              newline='', encoding="mbcs") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            print(row[0],"--",row[1])
            if(row[0]!="owner"):
                fetch_releases("token", row[0],row[1])

runAllProjects()
