
from todo_app.data.todo_mongo_client import *
from todo_app.data.viewmodel import *
from flask import Flask, render_template, request, redirect
from flask_login import login_required
from flask_login import LoginManager
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
      print("Processing the login route")
      
      if request.method == 'GET':
         oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
         oauth_secret_id = os.getenv('OAUTH_SECRET_ID')

         client = WebApplicationClient(oauth_client_id)
         # Prepare and send a request to get tokens
         token_url, headers, body = client.prepare_token_request(
            "https://github.com/login/oauth/access_token",
            authorization_response=request.url,
            redirect_url=request.base_url,
            code="" # get the code somehow
         )
         token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(oauth_client_id, oauth_secret_id)
         )

         # Parse the tokens!
         
         token = client.parse_request_body_response(json.dumps(token_response.json()))

      return redirect(request.url)



   if __name__ == '__main__':
      app.run()

   login_manager = LoginManager() 
   login_manager.init_app(app)
   oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
   oauth_secret_id = os.getenv('OAUTH_SECRET_ID')
   client = WebApplicationClient(oauth_client_id)

 
   @login_manager.unauthorized_handler 
   def unauthenticated(): 
      # need to call GET https://github.com/login/oauth/authorize with clientid and redirect_uri
      authorize_endpoint = 'https://github.com/login/oauth/authorize'
      
      authorize_url = client.prepare_request_uri(
        authorize_endpoint, "http://127.0.0.1:5000/login/callback")
      return redirect(authorize_url)


      
      # returns http://127.0.0.1:5000/login/callback/?code=ee365f5d6af9dff0e7b9
      # Then we will post the access_token back to github
      # POST https://github.com/login/oauth/access_token
      # client_id
      # client secret
      # code
      # redirect_uri

   @login_manager.user_loader 
   def load_user(user_id): 
      return None 

   return app




