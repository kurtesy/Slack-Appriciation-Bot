from sharepoint import SharePointSite, basic_auth_opener
url="https://fcs.allegisgroup.net/practices/biepm/Lists/Profile/Active%20Profile.aspx"
user, pwd = "corporate\\npatel", "qwerty@123"

opener = basic_auth_opener(url, user, pwd)

site = SharePointSite(url, opener)
for sp_list in site.lists:
    print sp_list.id, sp_list.meta['Title']




"""import requests
from requests_ntlm import HttpNtlmAuth

url="https://fcs.allegisgroup.net/practices/biepm/Lists/Profile/Active%20Profile.aspx"
user, pwd = "corporate\\npatel", "qwerty@123"
headers = {'accept': 'application/json;odata=verbose'}
r = requests.get(url, auth=HttpNtlmAuth(user, pwd), headers=headers)
print r.status_code
print r.content
print r.json()"""
