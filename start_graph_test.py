#import libraries
import requests
import json
import pandas as pd
import configparser

# Read in config data
config = configparser.ConfigParser()
config.read('ms_graph.ini')
if 'CONNECTION' in config:
    app_id = str(config.get('DEFAULT', 'APP_ID', fallback="There is no app id"))
    client_secret = str(config.get('DEFAULT', 'CLIENT_SECRET', fallback="There is no client secret"))
    tenant_id = str(config.get('DEFAULT', 'TENANT_ID', fallback="There is no tenant id"))
    test_user_mail = str(config.get('TEST_DATA', 'TEST_USER', fallback="There is no test user"))
else:
    print('DEFAULT is not found')

#Get token to sign in as application
token_url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id)
token_data = {
 'grant_type': 'client_credentials',
 'client_id': app_id,
 'client_secret': client_secret,
 'scope':'https://graph.microsoft.com/.default', 
}
token_r = requests.post(token_url, data=token_data)
token = token_r.json().get('access_token')

#print(token)

headers = {
 'Authorization': 'Bearer {}'.format(token)
}

# Use the token using microsoft graph endpoints
users_url = 'https://graph.microsoft.com/v1.0/users/{}'.format(test_user_mail)

users_url_all = 'https://graph.microsoft.com/v1.0/users'

user_response_data = json.loads(requests.get(users_url_all, headers=headers).text)
print(user_response_data)
