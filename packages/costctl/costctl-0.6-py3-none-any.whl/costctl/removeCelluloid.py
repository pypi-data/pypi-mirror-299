from flask import Flask, render_template, request
import os
import requests
import base64
import subprocess
import sys 
import json
import uuid
import csv
from costctl.commonfunctions import createPullRequest, extractFilePath


def removeCelluloidFromJson(appName,base_directory):
    #need to replace this path with accurate config.json path in the celluloid repo
    # os.chdir('carbon-app-template')
    startingDirectory = base_directory+"/carbon-onprem/carbon-applications/genpop/apps/dev/sadc/application-manifests"
    fileName = 'config.json'
    json_file_path = extractFilePath(fileName, startingDirectory)
    target_app = appName

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Remove the JSON object with the specific application name
    data = [entry for entry in data if entry.get('carbon-app') != target_app]

    # Write the filtered content back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=2)


def main():
    target_directory = "carbon-onprem"
    base_directory = "/Users/4924041/Downloads"
    token = 'BBDC-NDQ0Mzc4MDM0NjI1Ol8dwPNJJG8GNi9pERhzP/0f6Zjz'
    #Bit'bucket credentials
    headers = {'Authorization': 'Bearer BBDC-NDQ0Mzc4MDM0NjI1Ol8dwPNJJG8GNi9pERhzP/0f6Zjz','Content-Type': 'application/json'}
    # Source and destination repository URLs
    SOURCE_REPO_URL = 'https://tools.lowes.com/stash/scm/~4924041/carbon-onprem.git'
    DEST_REPO_URL = 'https://tools.lowes.com/stash/scm/~4924041/carbon-onprem.git'

    if os.path.exists("/Users/4924041/Downloads/carbon-onprem"):
    # If the directory exists, perform a git pull
        try:
            subprocess.run((['git', 'pull']), cwd="/Users/4924041/Downloads/carbon-onprem", check=True)
            print(f'Pulled updates for /Users/4924041/Downloads/carbon-onprem.')
        except subprocess.CalledProcessError as e:
            print(f'Error pulling updates: {e}')
    else:
    # If the directory doesn't exist, clone the repository
        try:
            subprocess.run(['git', '-c', "http.extraHeader=Authorization': 'Bearer"+" "+token,"clone", SOURCE_REPO_URL,target_directory], check=True, cwd=base_directory)
            print(f'Cloned repository to {target_directory}.')
        except subprocess.CalledProcessError as e:
            print(f'Error cloning repository: {e}')
    # Clone the source repository

    with open('files/name.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        new_branch_name = 'master'
        subprocess.run(['ls'])
        os.chdir("/Users/4924041/Downloads/carbon-onprem")
        subprocess.run(['git', 'checkout', "master"])
        # subprocess.run(['git', 'checkout', '-b', new_branch_name])
        for row in reader:
            namespace, appName = row[0].strip(), row[1].strip()
            print("appname")
            print(appName)
            fileToRemove = appName+".yaml"
            #set default starting directory for search
            startingDirectory = base_directory+"/carbon-onprem/carbon-applications/genpop/apps/dev/sadc/application-manifests"
            #call function to find where this file is at in the directory
            filePath = extractFilePath(fileToRemove, startingDirectory)
            FILE_TO_REMOVE = str(filePath)
            print(FILE_TO_REMOVE)
            # Remove the fil
            try:
                os.remove(FILE_TO_REMOVE)
            except FileNotFoundError:
                print(f"The file '{FILE_TO_REMOVE}' does not exist in the repository.")
            
            #remove config from config.json
            removeCelluloidFromJson(appName,base_directory)
    #Commit changes
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Remove file'])
    subprocess.run(['git', 'push', 'origin', new_branch_name])

    # Create a pull request
    # pull_request_url = "https://tools.lowes.com/stash/rest/api/1.0/users/4924041/repos/carbon-onprem/pull-requests"
    # default_branch = 'master'
    # message = "PR to remove celluloid file for:"+fileToRemove
    # slug = "carbon-onprem"
    # projectKey = "~4924041"
    # createPullRequest(pull_request_url,new_branch_name,default_branch,message,headers,slug,projectKey)
    
    print("Final commands to run on the cluster:")
    print("kubectl delete deploy,virtualservice,svc,role,cm,authorizationpolicy,rolebinding,rollout -n" +" "+ namespace +" "+ appName)
    print("kubectl delete serviceaccount -n" +" "+ namespace + " " +appName+"-k8s-sa")

if __name__ == '__main__':
    main()



