import requests
import json
import pandas as pd
import configparser

# Read in config data
config = configparser.ConfigParser()
config.read('ms_graph.ini')
if 'DEFAULT' in config:
    app_id = str(config.get('DEFAULT', 'APP_ID', fallback="There is no app id"))
    client_secret = str(config.get('DEFAULT', 'CLIENT_SECRET', fallback="There is no client secret"))
    tenant_id = str(config.get('DEFAULT', 'TENANT_ID', fallback="There is no tenant id"))
    #test_id = str(config.get('DEFAULT', 'TEST_ID', fallback="There is no test id"))

    admin_mail = str(config.get('TEST_DATA', 'ADMIN_MAIL', fallback="There is no admin mail"))
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

headers = {
 'Authorization': 'Bearer {}'.format(token)
}

def creat_user(surname, givenname, mailsufix, newUserPassword):
    userDisplayname = "{a_given} {a_surname}".format(a_given=givenname,a_surname=surname)
    # create user account
    user_information = {
    "accountEnabled": True,
    "displayName": "Test User",
    "mailNickname": "testuser",
    "userPrincipalName": "testuser{}".format(mailsufix) ,
    "passwordProfile" : {
        "forceChangePasswordNextSignIn": False,
        "password": newUserPassword
        }
    }

    #graph_url = 'https://graph.microsoft.com/v1.0/users/'
    #create_result = requests.post(graph_url, headers=headers, json=user_information)
    #create_response = create_result.json()
    #print(create_response)
    print(userDisplayname)


creat_user("test", "Stefan", "@M365x293953.onmicrosoft.com", "ewtwerwrw123!!")