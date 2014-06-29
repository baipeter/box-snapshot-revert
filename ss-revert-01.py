import requests
import json

token = 'KVxHzSblcnWIAVV8O3NperFuU9nhIIDT'

# Retrieve all items in root folder

url = 'https://api.box.com/2.0/folders/0/items'
payload = ''
headers = {
    'Authorization': 'Bearer ' + token
}

r = requests.get(url, headers = headers)
response = json.loads(r.text)
print json.dumps(response, indent=4)