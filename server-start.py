import http.server
import socketserver

from flask import Flask, render_template, request, redirect, url_for
import requests
from database_operation import add_users_to_db
from database_operation import verify_user_credentials

# Define the port you want the server to listen on
PORT = 8000

# Define the directory path you want to serve files from
DIRECTORY = ""

# Change the current working directory to the specified directory
# This is necessary because SimpleHTTPRequestHandler serves files relative to the current directory
import os
#os.chdir(DIRECTORY)


# Create a TCP server
#with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    #print("Server started at port", PORT)
    
    # Start serving requests indefinitely
    #httpd.serve_forever()

app = Flask("parkSF")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Call the function to add users to the database
        add_users_to_db(username, password)

        # Redirect to a success page or render a success template
        return render_template('register.html', success_message="Registration successful!")
    else:
        # Render the registration form template for GET requests
        return render_template('register.html')


@app.route('/login2', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database to verify the user credentials
        if verify_user_credentials(username, password):
            # Redirect to the main page or any other page on successful login
            return redirect(url_for('get_main'))
        else:
            # If the credentials are not valid, render the login form again with an error message
            error_message = "Invalid username or password."
            return render_template('login2.html', error_message=error_message)
    else:
        # Render the login form template for GET requests
        return render_template('login2.html')

@app.route(r'/users')
def get_faciltiies():
    url = "https://osp.cit.cc.api.here.com/parking/segments?bbox=41.389405513925354,2.127549994463742,41.38042236108416,2.139522979169079&geometryType=tpegOpenLR&geometryType=segmentAnchor"
    api_key = request.args.get('api_key')
    headers = {'Authorization' : 'Bearer ' + api_key}
    response = requests.get(url, headers=headers)
    print(response.status_code)
    #print(response)
    return str(response.status_code)

@app.route(r'/')
def get_main():
    return render_template("main.html")

@app.route(r'/login.html')
def get_login():
    return render_template("login.html")

@app.route(r'/register.html')
def get_register():
    return render_template("register.html")

@app.route(r'/login2.html')
def get_login2():
    return render_template("login2.html")

@app.route(r'/main.html')
def get_logout():
    return render_template("main.html")

app.run(debug=True)