import requests
import json
import os
from sys import exit

token = os.environ.get('BOX_ACCESS_TOKEN')
if token == None:
    print 'No token defined in environment. Exiting.'
    exit(1)

# Retrieve all items in root folder

url = 'https://api.box.com/2.0/folders/0/items'
payload = ''
headers = {
    'Authorization': 'Bearer ' + token
}

r = requests.get(url, headers = headers)
response = json.loads(r.text)
print json.dumps(response, indent=4)