import facebook
import requests
import json

# open json file for reading
with open('facebook.json', 'r') as f:
    data = json.load(f)

# read user info
user_short_token = data['user']['short_token']
user_long_token = data['user']['long_token']

# read app info
app_id = data['app']['id']
app_secret = data['app']['secret']

# read page info
page_token = data['page']['token']
page_id = data['page']['id']

host = "https://graph.facebook.com"
endpoint = "/oauth/access_token"

# get first long-lived user token
if user_long_token == 'None':
    user_long_token = requests.get(
        "{}{}?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(
            host, endpoint, app_id, app_secret, user_short_token)).json()['access_token']

    # update value
    data['user']['long_token'] = user_long_token

    # get first permanent page token
    graph = facebook.GraphAPI(access_token=user_long_token, version="2.7")
    pages_data = graph.get_object("/me/accounts")

    for item in pages_data['data']:
        if item['id'] == page_id:
            page_token = item['access_token']

    # update value
    data['page']['token'] = page_token

# use stored permanent page token to request a new one
else:
    page_token = requests.get(
        "{}{}?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(
                host, endpoint, app_id, app_secret, page_token)).json()['access_token']

    # update value
    data['page']['token'] = page_token

# open json file for writing
with open('facebook.json', 'w') as f:
    json.dump(data, f, indent=4)