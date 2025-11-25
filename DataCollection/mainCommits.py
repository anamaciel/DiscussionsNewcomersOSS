import requests
import csv
import pymongo
import json
import os
from datetime import datetime
import time



client = pymongo.MongoClient("localhost", 27017)
db = client.COLETA

username=""
token=""

def verify_rate_limit():
    session = requests.Session()
    session.auth = (username, token)
    response = session.get('https://api.github.com/rate_limit')
    data_all = response.json()

    rate_limit_remaining = int(data_all['resources']['core']['remaining'])
    rate_limit_reset = int(data_all['resources']['core']['reset'])
    remaining_seconds=0
    reset_time = 0
    current_time = 0
    datetime_format = '%Y-%m-%d %H:%M:%S'
    reset_time = datetime.fromtimestamp(rate_limit_reset).strftime(datetime_format)
    current_time = datetime.now().strftime(datetime_format)
    remaining_seconds = (datetime.fromtimestamp(rate_limit_reset) - datetime.now()).total_seconds() + 5
    if rate_limit_remaining>1:
        #print(remaining_seconds)
        print('[API] Requests Remaining: {}'.format(rate_limit_remaining))
    else:
         print('The request limit is over. The process will sleep for %d seconds.' % remaining_seconds)
         print('The request limit will reset on: {}'.format(reset_time))
         time.sleep(remaining_seconds)

def get_data(owner, name, number):

    url = 'https://api.github.com/repos/{}/{}/commits/{}'.format(owner, name, str(number))
    print(url)
    session = requests.Session()
    session.auth = (username, token)
    verify_rate_limit()
    response = session.get(url)
    data = response.json()


    commit = {}
    commit['owner'] = owner
    commit['name'] = name
    commit['sha'] = data['sha']
    commit['node_id'] = data['node_id']
    commit['author_name'] = data['commit']['author']['name']
    commit['author_email'] = data['commit']['author']['email']
    commit['commit_author_date'] = data['commit']['author']['date']
    if data['committer'] is not None:
        commit['committer_login'] = data['committer']['login']
        commit['committer_type'] = data['committer']['type']
        commit['committer_email'] = data['commit']['committer']['email']
        commit['committer_date'] = data['commit']['committer']['date']
    else:
        commit['committer_login'] = ""
        commit['committer_type'] = ""
        commit['committer_email'] = ""
        commit['committer_date'] = ""
    commit['message'] = data['commit']['message']
    commit['url'] = data['commit']['url']
    commit['comment_count'] = data['commit']['comment_count']
    commit['verification'] = data['commit']['verification']['verified']
    commit['verification_reason'] = data['commit']['verification']['reason']
    commit['verification_signature'] = data['commit']['verification']['signature']
    commit['verification_payload'] = data['commit']['verification']['payload']
    commit['stats_total'] = data['stats']['total']
    commit['stats_additions'] = data['stats']['additions']
    commit['stats_deletions'] = data['stats']['deletions']

    return commit

def collect_repo_infos(owner, name):
    
    url = 'https://api.github.com/repos/{}/{}'.format(owner, name)
    session = requests.Session()
    session.auth = (username, token)
    verify_rate_limit()
    response = session.get(url)

    data = response.json()
    repo = {}
    repo['id'] = data['id']
    repo['owner'] = owner
    repo['name'] = name
    repo['full_name'] = data['full_name']
    repo['fork'] = data['fork']
    repo['stars'] = data['stargazers_count']
    repo['language'] = data['language']

    

    return repo['id']

def collect_commits(owner, name):

    repo_id = collect_repo_infos(owner, name)

    page = 1
    last_page = False
    while not last_page:
        print('Page {}'.format(page))

        url = 'https://api.github.com/repos/{}/{}/commits?page={}'.format(owner, name, page)
        print(url)
        session = requests.Session()
        session.auth = (username, token)
        verify_rate_limit()
        response = session.get(url)
        data_all = response.json()


        for data in data_all:
            commit = get_data(owner, name, data['sha'])
            commit['repo_id'] = repo_id
            db.commits.insert_one(commit)

        if 'Link' not in response.headers or 'rel="next"' not in response.headers['Link']:
            last_page = True
        else:
            page = page + 1


if __name__ == '__main__':

    projects_file = open('projects.csv', 'r')
    reader_projects = csv.reader(projects_file, delimiter=';')
    
    
    for row in reader_projects:
        owner = row[0]
        name = row[1]
        print('Collecting... {} {}'.format(owner, __name__))

        collect_commits(owner, name)
