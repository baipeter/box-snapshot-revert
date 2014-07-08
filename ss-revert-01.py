import requests
import json
import os
import dateutil.parser
from datetime import datetime
from sys import exit


# Initial Settings

targetDateStr = '2014-07-04T19:16:41-07:00'    # Files uploaded to Box after this date will be reverted to a version before this date.
targetDate = dateutil.parser.parse(targetDateStr)


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


def get_file_info(fileid):
    
    url = 'https://api.box.com/2.0/files/' + str(fileid)
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

    return json.loads(r.text)


def get_file_past_versions(fileid):

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

    return json.loads(r.text)


def check_file_mod_date(fileid):

    modifiedDate = dateutil.parser.parse(get_file_info(fileid)['modified_at'])

    if modifiedDate > targetDate:

        versionInfoArray = []

        pastVersionInfo = get_file_past_versions(fileid)
        store_modified_info(pastVersionInfo, versionInfoArray)

        if versionInfoArray > 0:

            choose_good_version(fileid, versionInfoArray)

        else:

            print 'No versions exist prior to target date.'



def store_modified_info(fileVersionInfo, versionInfoArray):

    for version in fileVersionInfo['entries']:

        modifiedAt = dateutil.parser.parse(version['modified_at'])
        versionInfoArray.append([modifiedAt, version['id']])


def promote_version(fileid, versionid):

    url = 'https://api.box.com/2.0/files/' + str(fileid) + '/versions/current'
    headers = {
        'Authorization': 'Bearer ' + token
    }

    data = {"type": "file_version", "id" : str(versionid)}
    data = json.dumps(data)

    r = requests.post(url, headers = headers, data = data)

    if '401' in str(r.status_code):
        print 'Error: 401 Unauthorized. Check your access token. Exiting.'
        exit(1)
    elif r.text == '':
        print 'Unexpected response from server. Exiting.'
        exit(1)

    return json.loads(r.text)



def choose_good_version(fileid, versionInfoArray):

    print 'choosing good version for fileid', fileid

    for version in versionInfoArray:    # bug: this picks ANY version earlier than target date. We want LATEST version that is earlier than target date.

        if version[0] < targetDate:

            selectedVersion = version[1]

            print 'promoting versionid %s for fileid %s' % (str(selectedVersion), str(fileid))

            promote_version(fileid, selectedVersion)

            break


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




# for each item in folder, print its version info if it's a file
# if the current modified date is beyond the target date, search past versions

for item in firstFolderContents['entries']:
    if item['type'] == 'file':
        print 'file id %s (%s)' % (item['id'], item['name'])

        check_file_mod_date(item['id'])



        # fileVersionInfo =  get_file_past_versions(item['id'])
        # if fileVersionInfo['total_count'] > 0:

        #     versionInfoArray = []

        #     store_modified_info(fileVersionInfo, versionInfoArray)
        #     print versionInfoArray





