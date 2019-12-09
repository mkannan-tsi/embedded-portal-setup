import tableauserverclient as TSC
from flask import Flask, render_template, request, json, session, redirect, url_for
import sys
import os
import csv

SERVER_NAME = "http://<ip-address>/"
SERVER_SITE = 'template'
SERVER_USERNAME = "admin" ###REST API admin username and password###
SERVER_PASSWORD = "Tableau123"
PREVIEW_FOLDER_LOCATION = os.getcwd() + "/static/images/previews/%s/"
PREVIEW_FILE_EXTENSION = ".png"
FILE_NAME = "data/Users.csv" ###User information###
USER_ROLE = "ExplorerCanPublish"

##########Function to return server information##########
def retrieveServerInfo ():
    return SERVER_NAME, SERVER_SITE

def setPagination ():
    return TSC.RequestOptions(pagesize=1000)

##########Function to check if the user exists already##########
def retrieveUserInfo (username):
    with open(FILE_NAME, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if username == row['Email']:
                return True
    return False

##########Function to generate username from email address##########
def getUsersName(email):
    index = email.find ('@')
    return email[:index]

def stripCharacter (name):
    name = name.replace (" ", "")
    name = name.replace ("?", "")
    name = name.replace (".", "_")
    name = name.replace ("&", "")
    name = name.replace ("(", "")
    name = name.replace (")", "")
    return name

##########Function to allow the user to sign into the application##########
def loginUserToApp():
    #Logging into Application
    password = str(request.form['inputPassword'])
    email = str(request.form['inputEmail'])
        
    try :
        loggedInToApp = retrieveUserInfo(email)
        if loggedInToApp == True:
            session['user'] = getUsersName(email)   
    except :
        loggedInToApp = False 

    return loggedInToApp

##########Function to allow the user to create a new user##########
def signUpUserForApp():
    email = str(request.form['inputEmail'])
    userExists = retrieveUserInfo(email)
    if userExists == False:
        password = str(request.form['inputPassword'])   
        persona = str(request.form['inputPersona'])     
        addUser = addNewUser(email, password, persona)
        if addUser == True:
            return True
    
    return False

##########Adding the user to the set of web app users and to Tableau Server##########
def addNewUser (email, password, persona): 
    username = getUsersName(email)
    try:
        with open(FILE_NAME, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([username,email,password,persona])
                    
        server, isUserLoggedInToServerAsAdmin = loginToServer()
        server.version = '3.0'
        user = TSC.UserItem(username, USER_ROLE)
        user = server.users.add(user)
        user.email = email
        user = server.users.update(user, password)
        return True
    except:
        pass
    return False

##########Logging into the Server as an admin. Depending on the context, this login may impersonate a specific user##########
def loginToServer (*args):
    server = TSC.Server(SERVER_NAME)
    if args:
        try :
            tableau_auth = TSC.TableauAuth(SERVER_USERNAME, SERVER_PASSWORD, SERVER_SITE, user_id_to_impersonate=args[0])
            server.auth.sign_in(tableau_auth)
            isUserLoggedInToServer = True
        except:
            isUserLoggedInToServer = False
    else :
        try:
            server.auth.sign_out()
            tableau_auth = TSC.TableauAuth(SERVER_USERNAME, SERVER_PASSWORD, SERVER_SITE)
            server.auth.sign_in(tableau_auth)
            isUserLoggedInToServer = True
        except:
            isUserLoggedInToServer = False
    
    return server, isUserLoggedInToServer

##########Logging into the Server as an admin. Depending on the context, this login may impersonate a specific user##########
def loginAsUser ():
    request_options = setPagination()
    isUserLoggedInToServer = False 
    server, isUserLoggedInToServerAsAdmin = loginToServer()
    user_id = ""
    if isUserLoggedInToServerAsAdmin == True:
        username = session['user']
        request_options.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                             TSC.RequestOptions.Operator.Equals,
                             username))
        try:
            all_user_items, pagination_item = server.users.get (request_options)
            if all_user_items:
                user_id = all_user_items[0].id
                server, isUserLoggedInToServer = loginToServer (user_id)
        except:
            isUserLoggedInToServer = False 
    return server, isUserLoggedInToServer, user_id 

##########Using the REST API to generate thumbnails for appropriate visualizations##########
def showViews(user_id, user):
    request_options = setPagination()
    views = []
    workbooks = []
    if user_id:
        server, isUserLoggedInToServer = loginToServer(user_id)
        if isUserLoggedInToServer == True:        
            try:   
                all_workbook_items, pagination_item = server.workbooks.get(request_options)
                for j in all_workbook_items:
                    try:
                        server.workbooks.populate_views(j)
                        for i in j.views:
                            views.append(i.name)
                            workbooks.append (j.name)
                            server.views.populate_preview_image(i)
                            location = PREVIEW_FOLDER_LOCATION % (user)
                            if not os.path.exists(location):
                                os.makedirs(location)
                            with open(location + j.name + "_" + i.name + PREVIEW_FILE_EXTENSION, 'wb') as f:
                                f.write(i.preview_image)
                            f.close()
                    except:
                        pass
            except:
                pass
    return views, workbooks