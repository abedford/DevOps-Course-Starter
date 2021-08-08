
from todo_app.data.todo_mongo_client import *
from todo_app.data.viewmodel import *
from todo_app.data.user import *
from flask import Flask, render_template, request, redirect, session
from flask_login import login_required
from flask_login import LoginManager
from flask_login import login_user
import os
import requests
import json
from oauthlib.oauth2 import WebApplicationClient



def create_app(db_name = ""):
   app = Flask(__name__)
   item_view_model = None

   mongo_srv = os.getenv('MONGO_SRV')
   if db_name == "":
      db_name = os.getenv('MONGO_DB')
   mongo_user = os.getenv('MONGO_USER')
   mongo_pwd = os.getenv('MONGO_PWD')
   mongo_connection = os.getenv('MONGO_CONNECTION')

   mongo_client = ToDoMongoClient(mongo_user, mongo_pwd, mongo_srv, db_name, mongo_connection)

   oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
   oauth_secret_id = os.getenv('OAUTH_CLIENT_SECRET')

   login_manager = LoginManager() 
   login_manager.init_app(app)
   client = WebApplicationClient(oauth_client_id)

   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


   #  All the routes and setup code etc
   @app.route('/')
   @login_required
   def index():
      show_all = request.args.get('show_all')
      
      show_all_bool = show_all == "yes"
      print(f"Show all value is {show_all_bool}")
      tasks = mongo_client.get_all_tasks()
      item_view_model = ViewModel(tasks)
      return render_template('index.html', title='To Do App',
         view_model=item_view_model, show_all=show_all_bool)


   @app.route('/items/add', methods = ['POST'])
   def add_item():
      form_data = request.form
      task_title = form_data["title"]
      task_desc = form_data["description"]
      task_due_date = form_data["duedate"]
      
      mongo_client.add_task(task_title, task_desc, task_due_date) 
      
      return redirect('/')

   @app.route('/items/complete', methods = ['POST', 'GET'])
   def complete_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         mongo_client.complete_task(task_id)
            
      return redirect('/')


     
   @app.route('/items/remove', methods = ['POST'])
   def remove_item():

      if request.method == 'POST':
         
         form_data = request.form
         task_id = form_data["id"]
         mongo_client.delete_task(task_id)
         
      return redirect('/')


   @app.route('/items/start', methods = ['POST'])
   def start_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         mongo_client.start_task(task_id)
         
      return redirect('/')

   @app.route('/items/restart', methods = ['POST'])
   def restart_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         mongo_client.reopen_task(task_id)
         
      return redirect('/')

   @app.route('/login/callback', methods = ['GET'])
   def login():
      code = request.args.get("code")
      #print(f"Processing the login route code is: {code}")
      
      if request.method == 'GET':
         code = request.args.get("code")
         # Prepare and send a request to get tokens
         token_url, headers, body = client.prepare_token_request(
            "https://github.com/login/oauth/access_token",
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code  # get the code somehow
         )

         headers['Accept'] = 'application/json'

         token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(oauth_client_id, oauth_secret_id)
         )
         
         
         client.parse_request_body_response(json.dumps(token_response.json()))
         # access token is now stored in the client.access_token param

         userinfo_endpoint = "https://api.github.com/user"
         uri, headers, body = client.add_token(userinfo_endpoint)
         userinfo_response = requests.get(uri, headers=headers, data=body)
         print("")
         print(userinfo_response.content)
         print("")
         #if userinfo_response.json().get("email_verified"):
         unique_id = userinfo_response.json()["login"]
         #else:
         #   return "User email not available or not verified by GitHub.", 400
         print(f"Unique id is {unique_id}")

         # Create a user in your db with the information provided
         # by GitHub
         user = User(unique_id)
         print(f"User created {user}")

         # Begin user session by logging the user in
         session['username'] = unique_id
         login_user(user)
         return redirect('/')



   if __name__ == '__main__':
      app.run(ssl_context="adhoc")
 
   @login_manager.unauthorized_handler 
   def unauthenticated(): 
      authorize_endpoint = 'https://github.com/login/oauth/authorize'
      
      authorize_url = client.prepare_request_uri(
        authorize_endpoint, "http://127.0.0.1:5000/login/callback")
      return redirect(authorize_url)

   @login_manager.user_loader 
   def load_user(user_id): 
      return User(user_id)

   return app




