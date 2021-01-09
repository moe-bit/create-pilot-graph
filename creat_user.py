import requests
import json
import pandas as pd
import configparser
import secrets
import string

# Read in config data
config = configparser.ConfigParser()
config.read('ms_graph.ini')
if 'CONNECTION' in config:
    app_id = str(config.get('CONNECTION', 'APP_ID', fallback="There is no app id"))
    client_secret = str(config.get('CONNECTION', 'CLIENT_SECRET', fallback="There is no client secret"))
    tenant_id = str(config.get('CONNECTION', 'TENANT_ID', fallback="There is no tenant id"))
    
    admin_mail = str(config.get('TEST_DATA', 'ADMIN_MAIL', fallback="There is no test admin mail"))
    domain = str(config.get('TEST_DATA', 'DOMAIN', fallback="There is no test domain"))
    invitor = str(config.get('TEST_DATA', 'INVITOR', fallback="There is no test invitor"))
else:
    print('CONNECTION parameters are not found')



# Get token to sign in as application
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
 'Authorization': 'Bearer {}'.format(token),
 # needed for counting
 'ConsistencyLevel' : 'eventual'
}

# Generate a secure password
def generatePassword():
    possibleCharc = string.ascii_letters + string.digits + string.punctuation
    # for a 20-character password
    password = ''.join(secrets.choice(possibleCharc) for i in range(20))

    return password

# Checks if a given name matches requierements and format it nicely
def checkName(name):
    correctName = name.title()
    return correctName

# Create a username
def createUserName(surname, givenname):
    username = '{person_givenname}.{person_surname}'.format(person_givenname=givenname, person_surname=surname)
    return username

# Creat UserPrincipalName 
def create_UsP(surname, givenname, domain):
    username = createUserName(surname, givenname)
    lowerUsername = username.lower()
    usp = '{uspPrefix}{domain}'.format(uspPrefix=lowerUsername, domain=domain)

    return usp

# Check if username already exists
def uspExist(userPrincipalName):
    # instead of using v1.0 in query you need to use beta to be able to count result
    users_url = 'https://graph.microsoft.com/beta/users?$count=true&$filter=startswith(userPrincipalName, \'{}\' )'.format(userPrincipalName)
    user_response_data = json.loads(requests.get(users_url, headers=headers).text)
    
    # check if result is > 0
    return user_response_data['@odata.count'] > 0

# Creat Azure AD User
def create_user(surname, givenname, domain, privateMail):
    correctSur = checkName(surname)
    correctGiven = checkName (givenname)
    userPrincipalName = create_UsP(correctSur, correctGiven, domain)

    if uspExist(userPrincipalName):
        print("usp = {} already exists!".format(userPrincipalName))
    
    else:
        mailNickname = createUserName(correctSur, correctGiven)
        createdPassword = generatePassword()

        userDisplayName = "{person_given} {person_surname}".format(person_given=correctGiven, person_surname=correctSur)
        
        user_information = {
        "accountEnabled": True,
        "surName" : correctSur,
        "givenName" : correctGiven,
        "displayName": userDisplayName,
        "mailNickname": mailNickname,
        "mail" : userPrincipalName,
        "userPrincipalName": userPrincipalName,
        "usageLocation": "DE",
        "passwordProfile" : {
            "forceChangePasswordNextSignIn": False,
            "password": createdPassword
            }
        }
        
        # Request to create user
        graph_url = 'https://graph.microsoft.com/v1.0/users/'
        create_result = requests.post(graph_url, headers=headers, json=user_information)
        create_response = create_result.json()
        print(create_response)
        
        user_id = create_response['id']

        print(user_id)

        if assign_licence(user_id):
            sendInvitationMail(privateMail, createdPassword, correctGiven, userPrincipalName)
        else:
            print("No Mail sended!")

# Assing licence to a user: It's important to set the usage location before
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
    licence_response = licence_result.json()                                                        
    
    print(licence_response)
    return True

# The application sends an invitation mail from a specified account to the new account 
def sendInvitationMail(privateMail, password, givenName, userPrincipalName):
    htmlMail = """\
        <html>
            <body>
            <p>Hallo {name},</p>
            <p>wir d&uuml;rfen dich herzlich bei uns willkommen hei&szlig;en. Hier sind deine Zugangsdaten:</p>
            <p>&nbsp;</p>
            <p><strong>Benutzername</strong>: {username} </p>
            <p><strong>Passwort</strong>: {userPwd} </p>
            <p>&nbsp;</p>
            <p>Du kannst dich hier anmelden: <a href="http://www.office.com">www.office.com</a></p>
            <p>&nbsp;</p>
            <p>Gru&szlig;,</p>
            <p>Bereichsleitung IT</p>
            </body>
        </html>
        """.format(name=givenName, username=userPrincipalName, userPwd=password)
    
    
    mail = {
    "message": {
        "subject": "Testmail",
        "body": {
        "contentType": "html",
        "content": htmlMail
        },
        "toRecipients": [
        {
            "emailAddress": {
            "address": privateMail
            }
        }
        ],
    },
    "saveToSentItems": "false"
    }   

    mailGraphUrl = 'https://graph.microsoft.com/v1.0/users/{}/sendMail'.format(invitor)
    mailResult = requests.post(mailGraphUrl, headers=headers, json=mail)
    print(mailResult)




# Test output
#create_user("test12", "Stefan", domain)
#uspExist('stefan.test02@M365x293953.onmicrosoft.com')
#print(uspExist('s'))
#print(uspExist('y'))

create_user("Test","Peter", domain, "test@gmx.de")