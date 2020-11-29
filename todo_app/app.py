
from todo_app.data.session_items import *
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

   print(all_tasks)
   # sorted_cards = sorted(all_cards, key = itemgetter('status'), reverse=True)
   return render_template('index.html', title='To Do App', tasks=all_tasks)


@app.route('/items/add', methods = ['POST'])
def add_items():
   
   form_data = request.form
   task = form_data["title"]
   
   add_task(task)   
   return redirect('/')


@app.route('/items/complete', methods = ['POST', 'GET'])
def complete_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      complete_task(task_id)
         
   return redirect('/')


     
@app.route('/items/remove', methods = ['POST', 'GET'])
def remove_items():
   if request.method == 'POST':
      form_data = request.form
      task_id = form_data["id"]
      
      delete_task(task_id)
      
   return redirect('/')


if __name__ == '__main__':
    app.run()

