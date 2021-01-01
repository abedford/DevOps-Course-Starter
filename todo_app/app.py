
from todo_app.data.trello_board import *
from todo_app.data.viewmodel import *
from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   cards = get_all_cards_on_board()
   item_view_model = ViewModel(cards)
   return render_template('index.html', title='To Do App',
      view_model=item_view_model)


@app.route('/items/add', methods = ['POST'])
def add_item():
   form_data = request.form
   task_title = form_data["title"]
   task_desc = form_data["description"]
   task_due_date = form_data["duedate"]
   print(f"Adding task with {task_title} {task_desc} {task_due_date}")
   
   
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


@app.route('/items/start', methods = ['POST'])
def start_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      
      start_task(task_id)
      
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

