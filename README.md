# create-pilot-graph

create pilot graph is a project of the WOC 2020/21 combining Microsoft Graph API with Python.

## The main goal of this project:
- Create new office user accounts form a CSV Import via MS Graph API


## Project steps:
1. [X] ~~Connect to MS Graph API~~
1. [X] ~~Create Useraccount~~
1. [X] ~~Lizenz einem User zuweisen~~
1. [X] ~~Generate a password~~
1. [X] ~~check if userPrincipalName already exists~~
1. [X] ~~Location für Lizenzzuweisung per PATCH setzen~~
1. [X] ~~Einladungsmail versenden~~
1. [X] ~~CSV einlesen~~
1. [X] ~~Umlaute ersetzten~~
1. [X] ~~Vorname/ Nachname validieren~~
1. [ ] CSV validieren -> passt private E-Mail Format 
1. [ ] Überprüfen welche Parameter beim erstellen des Users ausgefüllt seien müssen (private Mail für e-Mail Versand/ JobTitle/ preferedLanguage)
1. [ ] Code aufhübschen 
1. [ ] Neu angelegte User zu Gruppen hinzufügen
1. [ ] UI für Import + ini erstellen


## Standard API Functions:
| Function | Description | Link |
| ------ | ------ | ------ |
| createUser() | Creates a Azure AD user | [Link]() |
| uspExsist() | Checks if userPrincipalName already exists | [Link]() |
| assign_licence() | Assign licence to user | [Link]() |
| sendInvitationMail()| Sends a mail from an application. You need to set an account as a sender | [Link]() |


## Lessons learned
1. First steps with graph api is difficult (~ 3h for first connection)
1. VS Studio Live Share good tool for coding collaboration
1. Postman is a very good tool for testing the api
1. API Debugging is very difficult
1. Testteant is recommended 
1. Concentrate 


## Useful links
Links that helped us:

[Get Users](https://docs.microsoft.com/de-de/graph/api/user-list?view=graph-rest-1.0&tabs=http#code-try-29)

[Query parameter](https://docs.microsoft.com/en-us/graph/query-parameters?context=graph%2Fapi%2F1.0&view=graph-rest-1.0#filter-parameter)

[Use count in query](https://developer.microsoft.com/en-us/office/blogs/build-advanced-queries-with-count-filter-search-and-orderby/)

[Acess values in json python](https://stackoverflow.com/questions/11241583/python-accessing-data-in-json-object)


## Contributer:
- Arthur
- Stefan
- Roman
- Moritz

