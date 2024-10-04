import os
import requests
import base64
import subprocess
import sys 
import json
import uuid

def createPullRequest(pull_request_url, new_branch_name, default_branch, message, headers,slug,projectKey):
    pull_request_data = {"title":message,"description":message,"state":"OPEN","fromRef":{"id":"refs/heads/"+new_branch_name,"repository":{"slug":slug,"project":{"key":projectKey}}},"toRef":{"id":"refs/heads/"+default_branch,"repository":{"slug":slug,"project":{"key":projectKey}}}}
    response = requests.post(pull_request_url, headers=headers, data=json.dumps(pull_request_data))
    print(response)
    if response.status_code == 201:
        print('Pull request created successfully.')
    else:
        print(f'Failed to create the pull request. Status Code: {response.status_code}')
        print(response.text)


def extractFilePath(filename, search_path='.'):
    print(filename)
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            file_path = os.path.join(root, filename)
            print(f'**** **** **** File "{filename}" found at: {file_path} **** **** ****')
            return file_path