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

def create_user(surname, givenname, mailsufix, newUserPassword):
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
    #user_id = create_response.json().get('id')

    assign_licence("fef3ca2d-1aae-488a-bb7b-15f234b8c2c9")

def assign_licence(user_id):
    licence_information = {
    "addLicenses": [
        {
        "disabledPlans": [],
        "skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"
        }
    ],
    "removeLicenses": []
    }

    licence_url = 'https://graph.microsoft.com/v1.0/users/{id}/assignLicense'.format(id=user_id)
    licence_result = requests.post(licence_url, headers=headers, json=licence_information)
    licence_response = licence_result.json()                                                        #Office Location setzten: https://docs.microsoft.com/de-de/archive/blogs/dsadsi/did-you-get-a-license-assignment-cannot-be-done-for-user-with-invalid-usage-location-error-when-applying-a-license-via-graph-api
    print(licence_response)

create_user("test", "Stefan", "@M365x293953.onmicrosoft.com", "ewtwerwrw123!!")