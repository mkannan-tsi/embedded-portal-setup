from flask import Flask, render_template, request, json, session, redirect, url_for
from cryptography.fernet import Fernet
import tableauserverclient as TSC
import string
import random
from RestCalls import *
import requests
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))

key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

@app.route("/")
def main():
	return render_template('index.html')

##########Rendering the login page##########
@app.route('/login', methods=['GET'])
def login():
	##########Continuing the previous session if it exists##########
	try:
		isUserLoggedInToApp = session['isUserLoggedIn']
	except:
		isUserLoggedInToApp = False

	if isUserLoggedInToApp == True:
		return redirect(url_for('showGrid'))
	else:
		return render_template('login.html')

##########Logging out the user and killing the session##########
@app.route ('/logout')
def logout():
	try:
		session.clear()
	except:
		pass
	return redirect (url_for('login'))

##########Actually logging in the user##########
@app.route('/loginRedirect', methods=['GET', 'POST'])
def loginAction():	
	##########Checking if user is authenticated##########
	session['isUserLoggedIn'] = loginUserToApp()
	isUserLoggedInToApp = session['isUserLoggedIn']
	if isUserLoggedInToApp == True:
		return redirect(url_for('showGrid'))
	else:
		state = "There is an error in logging in. Please re-try."
		return render_template('login.html', message = state)

##########Rendering the new user sign up page##########
@app.route('/signUp', methods=['GET'])
def signUp():
	return render_template('signUp.html')

##########Actually signing up the new user##########
@app.route('/signUpRedirect', methods=['GET', 'POST'])
def signUpAction():	
	isUserCreated = signUpUserForApp()
	if isUserCreated == True:
		state = "User created! Please sign in"
		return render_template('login.html', success_message = state)
	else:
		state = "User creation had an issue. Please try again"
		return render_template('signUp.html', message = state)

##########Rendering the page with all available visualizations##########
@app.route('/grid', methods=['GET', 'POST'])
def showGrid():
	##########Checking if user is authenticated##########
	try:
		isUserLoggedInToApp = session['isUserLoggedIn']
	except:
		isUserLoggedInToApp = False

	##########Signing into the REST API to display permissioned visualizations##########
	if isUserLoggedInToApp == True :
		server, isUserLoggedInToServer, user_id = loginAsUser()
		user = session['user']
		views, workbooks = showViews(user_id, user)
		timestamp = time.time()
		return render_template('grid.html', view = views, workbook = workbooks, user=user, timestamp = timestamp)
	else:
		state = "Please log in first"
		return render_template('login.html', message = state)

##########Rendering a specific visualization##########
@app.route('/workbook=<string:workbook>+view=<string:view>')
def view(workbook, view):
	##########Checking if user is authenticated##########
	try:
		isUserLoggedInToApp = session['isUserLoggedIn']
	except:
		isUserLoggedInToApp = False

	##########Generating a trusted ticket##########	
	if isUserLoggedInToApp == True :
		worksheet = stripCharacter(view)	
		server, site = retrieveServerInfo()
		url = server+"/trusted"
		user = session['user']
		payload =  {'username' : user, 'target_site' : site}
		r = requests.post(url, params = payload)	
		ticket = r.text
		return render_template('view.html', server=server, site=site, ticket=ticket, workbook=workbook, worksheet=worksheet, user=user)

	else:
		state = "Please log in first"
		return render_template('login.html', message = state)
  
if __name__ == "__main__":
	# setDefaultEncoding ()
	app.run(host= '0.0.0.0', port = 5000, debug = True)