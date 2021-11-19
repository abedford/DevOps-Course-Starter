
from todo_app.data.todo_mongo_client import *
from todo_app.data.viewmodel import *
from todo_app.data.user import *
from flask import Flask, render_template, request, redirect, session
from flask_login import login_required
from flask_login import LoginManager
from flask_login import login_user
from flask_login import current_user
import os
import requests
from oauthlib.oauth2 import WebApplicationClient
import logging
from loggly.handlers import HTTPSHandler 
from logging import Formatter
import logging.config
import time

# create logger
logger = logging.getLogger('todo_app')
logging.config.fileConfig('python.conf')
logging.Formatter.converter = time.gmtime
logger.setLevel(logging.DEBUG)
 
# create console handler and set level to debug
ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)






def create_app():
   app = Flask(__name__)
   item_view_model = None
   app.logger.info ("Starting the app logger") 
   log_level = os.getenv('LOG_LEVEL')
   app.logger.setLevel(log_level)

   loggly_token = os.getenv('LOGGLY_TOKEN')
   if loggly_token is not None: 
      app.logger.info ("Setting up the loggly log") 
      handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{loggly_token}/tag/todo-app') 
      handler.setFormatter( 
        Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s") 
      )  
      app.logger.addHandler(handler) 
   else:
      app.logger.info("Loggly token was not found")


   logger.info("Starting the app")
   disable_login = os.getenv('FLASK_SKIP_LOGIN')
   if disable_login == "True":
      logger.info("Switching off authentication in the app config for testing purposes")      
      app.config['LOGIN_DISABLED'] = True
   mongo_srv = os.getenv('MONGO_SRV')
   db_name = os.getenv('MONGO_DB')
   mongo_user = os.getenv('MONGO_USER')
   mongo_pwd = os.getenv('MONGO_PWD')
   mongo_connection = os.getenv('MONGO_CONNECTION')

   logger.info("Setting up Mongo Client with user: %s, database: %s, mongo_connection: %s", mongo_user, db_name, mongo_connection)
   mongo_client = ToDoMongoClient(mongo_user, mongo_pwd, mongo_srv, db_name, mongo_connection)

   oauth_client_id = os.getenv('OAUTH_CLIENT_ID')
   oauth_secret_id = os.getenv('OAUTH_CLIENT_SECRET')

   logger.info("Setting up Login Manager")
   login_manager = LoginManager() 
   login_manager.init_app(app)
   client = WebApplicationClient(oauth_client_id)

   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
   secret_key = oauth_secret_id
   writer_role = "Writer"
   reader_role = "Reader"
   admin_role = "Admin"




   #  All the routes and setup code etc
   @app.route('/')
   @login_required
   def index():
      app.logger.info("Opening index page")
      show_all = request.args.get('show_all')
      
      show_all_bool = show_all == "yes"
      app.logger.info("Getting all tasks")
      tasks = mongo_client.get_all_tasks()
      item_view_model = ViewModel(tasks)
      # We want to only show certain buttons and links to writers or admins UNLESS login is disabled (ie. we are running tests)
      writer_bool = (disable_login or current_user.role == writer_role)
      admin_bool = (disable_login or current_user.role == admin_role)
      return render_template('index.html', title='To Do App',
         view_model=item_view_model, show_all=show_all_bool, writer=writer_bool, admin=admin_bool)

   @app.route('/items/add', methods = ['POST'])
   @login_required
   def add_item():
      
      if (disable_login or current_user.role == writer_role):
         form_data = request.form
         task_title = form_data["title"]
         task_desc = form_data["description"]
         task_due_date = form_data["duedate"]
         app.logger.info("Adding a new task, details: %s | %s | %s" , task_title, task_desc, task_due_date)
         mongo_client.add_task(task_title, task_desc, task_due_date) 
      else:
         logger.error(f"Reader Role is not allowed to add a task")
      return redirect('/')

   @app.route('/items/complete', methods = ['POST', 'GET'])
   @login_required
   def complete_item():
      if (disable_login or current_user.role == writer_role):
         
         form_data = request.form
         task_id = form_data["id"]
         logger.info("Completing a task with ID: %s", task_id)
         mongo_client.complete_task(task_id)
      else:
         logger.error(f"Reader Role is not allowed to complete a task")
      return redirect('/')


     
   @app.route('/items/remove', methods = ['POST'])
   @login_required
   def remove_item():
      if (disable_login or current_user.role == writer_role ):
         form_data = request.form
         task_id = form_data["id"]
         logger.info("Deleting a task with ID: %s", task_id)
         mongo_client.delete_task(task_id)
      else:
         logger.error(f"Reader Role is not allowed to remove a task")
      return redirect('/')


   @app.route('/items/start', methods = ['POST'])
   @login_required
   def start_item():
      if (disable_login or current_user.role == writer_role):
         form_data = request.form
         task_id = form_data["id"]
         logger.info("Starting a task with ID: %s", task_id)
         mongo_client.start_task(task_id)
      else:
         logger.error(f"Reader Role is not allowed to start a task")
      return redirect('/')

   @app.route('/users/', methods = ['GET'])
   @login_required
   def get_users():
      if (disable_login or current_user.role == admin_role):
         
         users = mongo_client.get_all_users()
         
         return render_template('users.html', title='User Admin',
            users=users)
      else:
         logger.error(f"This page is only for administrators")

   @app.route('/users/update', methods = ['POST'])
   @login_required
   def update_user():
      if (disable_login or current_user.role == admin_role):
         form_data = request.form
         user_id_to_update = form_data["id"]
         new_role = form_data["new_role"]
         logger.info("Updating a user with ID: %s to new role: %s", user_id_to_update, new_role)
         mongo_client.update_user(user_id_to_update, new_role)
      else:
         logger.error(f"Reader Role is not allowed to update a task")
      return redirect('/users')

   @app.route('/items/restart', methods = ['POST'])
   @login_required
   def restart_item():
      if (disable_login or current_user.role == writer_role):
         if request.method == 'POST':
               form_data = request.form
               task_id = form_data["id"]
               logger.info("Restarting a task with ID: %s", task_id)
               mongo_client.reopen_task(task_id)
      else:
         logger.error(f"Reader Role is not allowed to restart a task")   
      return redirect('/')

   @app.route('/login/callback', methods = ['GET'])
   def login():
      logger.info(f"Logging you in as a user") 
      code = request.args.get("code")
      
      code = request.args.get("code")
      # Prepare and send a request to get tokens
      token_url, headers, body = client.prepare_token_request(
         "https://github.com/login/oauth/access_token",
         authorization_response=request.url,
         code=code  
      )

      headers['Accept'] = 'application/json'

      token_response = requests.post(
         token_url,
         headers=headers,
         data=body,
         auth=(oauth_client_id, oauth_secret_id)
      )
         
         
      client.parse_request_body_response(token_response.text)
      # access token is now stored in the client.access_token param

      userinfo_endpoint = "https://api.github.com/user"
      uri, headers, body = client.add_token(userinfo_endpoint)
      userinfo_response = requests.get(uri, headers=headers, data=body)
      
      login_id = userinfo_response.json()["login"]
      logger.debug(f"Looking for {login_id} in the database")
      # see if we can find the user in the database already
      user = mongo_client.get_user_by_username(login_id)
      if user is None:
         # new users get added with Reader rights
         logger.debug(f"Creating new user with {login_id} and reader role")
         user = mongo_client.add_user(login_id, reader_role)           
      
      # Begin user session by logging the user in
      logger.info(f"Logging in to the session")
      session['username'] = user.username
      login_user(user)
      return redirect('/')



   if __name__ == '__main__':
      app.run(ssl_context="adhoc")
 
   @login_manager.unauthorized_handler 
   def unauthenticated(): 
      authorize_endpoint = 'https://github.com/login/oauth/authorize'
      logger.info(f"User is unauthenticated, redirecting to authentication service")
      authorize_url = client.prepare_request_uri(
        authorize_endpoint, "https://test-alb-terx-todo-app-service.azurewebsites.net/login/callback")
      return redirect(authorize_url)

   @login_manager.user_loader 
   def load_user(user_id):
      # get the user from the database if it exists
      logger.info(f"Loading user")
      result_user = mongo_client.get_user_by_id(user_id)
      
      return result_user

   return app




