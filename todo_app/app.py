
from todo_app.data.trello_board import *
from todo_app.data.task import *
from operator import itemgetter
from flask import Flask, render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   lists = get_lists()
   all_tasks = []
   for list in lists:
      all_tasks.extend(get_cards_in_list(list))

   return render_template('index.html', title='To Do App', tasks=all_tasks)


@app.route('/items/add', methods = ['POST'])
def add_item():
   form_data = request.form
   task_title = form_data["title"]
   task_desc = form_data["description"]
   task_due_date = "12/09/2021"
   print(f"Adding task with {task_title} {task_desc}")
   
   
   add_task(task_title, task_desc, task_due_date)  
    
   return redirect('/')


@app.route('/items/complete', methods = ['POST', 'GET'])
def complete_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      complete_task(task_id)
         
   return redirect('/')


     
@app.route('/items/remove', methods = ['POST'])
def remove_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      
      delete_task(task_id)
      
   return redirect('/')


@app.route('/items/restart', methods = ['POST'])
def restart_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      
      reopen_task(task_id)
      
   return redirect('/')

if __name__ == '__main__':
    app.run()

