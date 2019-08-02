from encodings import undefined
import requests


url = 'http://127.0.0.1:1996/users/add_roles'
payload = "{\n\t\"role_name\":\"user\"\n}"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'application/json'
}
response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False, timeout=undefined)
print(response.text)

import requests

url = 'http://127.0.0.1:1996/users/add_roles'
payload = "{\n\t\"role_name\":\"admin\"\n}"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'application/json'
}
response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False, timeout=undefined)
print(response.text)