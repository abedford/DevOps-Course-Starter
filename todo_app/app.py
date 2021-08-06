
from todo_app.data.todo_mongo_client import *
from todo_app.data.viewmodel import *
from flask import Flask, render_template, request, redirect
from flask_login import login_required
from flask_login import LoginManager
import os
import requests

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

   login_manager = LoginManager() 
   login_manager.init_app(app)

   #  All the routes and setup code etc
   @login_required
   @app.route('/')
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


   if __name__ == '__main__':
      app.run()


   

 
   @login_manager.unauthorized_handler 
   def unauthenticated(): 
      # need to call GET https://github.com/login/oauth/authorize with clientid and redirect_uri
      authorize_url = 'https://github.com/login/oauth/authorize?client_id=640c2ac9d976df608c2b&redirect_uri=http://127.0.0.1:5000/login/'
      
      print("Trying to redirect to github authorization")
      return redirect(authorize_url)
      
      # Then we will post the access_toekn back to github
      # POST https://github.com/login/oauth/access_token
      # client_id
      # client secret
      # code
      # redirect_uri

   @login_manager.user_loader 
   def load_user(user_id): 
      return None 

   return app




