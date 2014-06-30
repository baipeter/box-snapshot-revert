import requests
import json
import os
from sys import exit


def get_folder_contents(folderid):

    url = 'https://api.box.com/2.0/folders/' + str(folderid) + '/items'
    payload = ''
    headers = {
        'Authorization': 'Bearer ' + token
    }

    r = requests.get(url, headers = headers)
    response = json.loads(r.text)
    # print json.dumps(response, indent=4)

    return response


# Load access token
token = os.environ.get('BOX_ACCESS_TOKEN')
if token == None:
    print 'No token defined in environment. Exiting.'
    exit(1)


# Get root folder items
response = get_folder_contents(0)


# Process response
folders = []

for element in response['entries']:
    if element['type'] == 'folder':
        folders.append(element['id'])


# Get individual folder items
subFolders = []

for item in folders:
    print 'Getting contents of folder', item
    response = get_folder_contents(item)

    for element in response['entries']:
        if element['type'] == 'folder':
            subFolders.append(element['id'])

if subFolders:
    folders.extend(subFolders)


print folders