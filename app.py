import requests
import json
import flask
import time
from flask import request, json, Response


def generate_stars_count_list(response_json, stars_count_list):
    for repo in response_json:
        star_count_of_repo = {}
        star_count_of_repo['name'] = repo['name']
        star_count_of_repo['stars'] = repo['stargazers_count']
        stars_count_list.append(star_count_of_repo)
    return stars_count_list


def stars_in_repo(repo):
    return repo['stars']


def get_top3(stars_count_list, top3_repos):
    print("hello", stars_count_list)
    stars_count_list.sort(key = stars_in_repo, reverse = True)  
    top3_repos.append(stars_count_list[0])
    top3_repos.append(stars_count_list[1])
    top3_repos.append(stars_count_list[2])
    return top3_repos

def get_top_repos(org_name):
    url = "https://api.github.com"
    requested_org = org_name
    org_repos_url = url + "/orgs/" + requested_org + "/" + "repos"
    
    re = requests.get(org_repos_url)
    if (re.status_code == 201 or re.status_code == 200):
        response_json = re.json()
        stars_count_list = []

        stars_count_list = generate_stars_count_list(response_json, stars_count_list) 
        # print(stars_count_list)

        top3_repos = []
        top3_repos = get_top3(stars_count_list, top3_repos)

        # Type changed to dict with desirable header from list
        top3_repos = {"results": top3_repos}
        return top3_repos
    
    else: # In case of other status codes display the same error messages
        return re.text
    


# Defining and creating the API
app = flask.Flask(__name__)
# app.config["DEBUG"] = True


# For requests sent to root
@app.route('/')
def home():
    return "This is the homepage, please follow the procedure to get to the desired page"


# The desired routing for valid requests
@app.route('/repos', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        request_json = json.dumps(request.json)
        dict_request = json.loads(request_json)
        org_name = dict_request['org']
        top3_repos = get_top_repos(org_name)
        top3_repos_json = json.dumps(top3_repos)
        resp = Response(top3_repos_json, status = 200, mimetype = 'application/json')
        return resp
    else:
        message = json.dumps("Unsupported media file type")
        resp = Response(message, status = 415, mimetype = 'application/json')
        return resp


if __name__ == '__main__':
    app.run()
