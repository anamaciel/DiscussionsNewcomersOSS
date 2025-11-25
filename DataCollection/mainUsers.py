from get import get
import csv
import pymongo
import json
import os


client = pymongo.MongoClient("localhost", 27017)
db = client.coleta
token = ""

def get_users_file(path):
    users=[]
    cont=0
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            if cont>0:
                users += [row[0].replace(" ","")]
                print(row[0])
            cont+=1
    return users


def get_data(users):
    
    
    for user in users:
        url = 'https://api.github.com/users/{}?access_token={}'.format(user,token)
        
        data = get(url).json()

        user = {}
        user['login'] = data['login']
        user['id'] = data['id']
        user['type'] = data['type']
        user['name'] = data['name']
        user['public_repos'] = data['public_repos']
        user['public_gists'] = data['public_gists']
        user['followers'] = data['followers']
        user['following'] = data['following']
        user['created_at'] = data['created_at']
        user['updated_at'] = data['updated_at']
        user['company'] = data['company']
        user['blog'] = data['blog']
        user['location'] = data['location']
        user['email'] = data['email']
        user['bio'] = data['bio']
        user['twitter_username'] = data['twitter_username']
        

        db.users.insert_one(user)


if __name__ == '__main__':
    users = get_users_file("users.csv")
    get_data(users)
    
   
