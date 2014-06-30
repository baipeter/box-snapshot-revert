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
    
    #check for errors
    if '401' in str(r.status_code):
        print 'Error: 401 Unauthorized. Check your access token. Exiting.'
        exit(1)
    elif r.text == '':
        print 'Unexpected response from server. Exiting.'
        exit(1)

    response = json.loads(r.text)
    # print json.dumps(response, indent=4)

    return response

def seek_folder(ID, allFolders):

    print 'seeking folder %d' % ID
    response = get_folder_contents(ID)
    
    for element in response['entries']:
        if element['type'] == 'folder':
            seek_folder(int(element['id']), allFolders)

    allFolders.append(ID)

# Load access token
token = os.environ.get('BOX_ACCESS_TOKEN')
if token == None:
    print 'No token defined in environment. Exiting.'
    exit(1)


# get all folders
allFolders = []
seek_folder(0, allFolders)

print allFolders