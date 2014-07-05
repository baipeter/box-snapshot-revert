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

def get_file_info(fileid):
    pass

def get_file_past_versions(fileid):
    pass

    url = 'https://api.box.com/2.0/files/' + str(fileid) + '/versions'
    headers = {
        'Authorization': 'Bearer ' + token
    }

    r = requests.get(url, headers = headers)

    if '401' in str(r.status_code):
        print 'Error: 401 Unauthorized. Check your access token. Exiting.'
        exit(1)
    elif r.text == '':
        print 'Unexpected response from server. Exiting.'
        exit(1)

    response = json.loads(r.text)


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

# allFolders = []
# seek_folder(0, allFolders)
# print allFolders

# pick a folder and explore

firstFolderContents = get_folder_contents(2167061144)
print json.dumps(firstFolderContents, indent=4)

for entry in firstFolderContents['entries']:
    if entry['type'] == 'file':
        print 'file id %s (%s)' % (entry['id'], entry['name'])

        # show version info


