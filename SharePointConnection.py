from sharepoint import SharePointSite, basic_auth_opener
url="https://fcs.allegisgroup.net/practices/biepm/Lists/Profile/Active%20Profile.aspx"
user, pwd = "user", "pwd"

opener = basic_auth_opener(url, user, pwd)

site = SharePointSite(url, opener)
for sp_list in site.lists:
    print sp_list.id, sp_list.meta['Title']

