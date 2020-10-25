
from todo_app.data.session_items import *
from operator import itemgetter
from flask import Flask, render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   items = get_items()
   sorted_items = sorted(items, key = itemgetter('status'), reverse=True)
   return render_template('index.html', title='To Do App', items=sorted_items)


@app.route('/items/add', methods = ['POST'])
def add_items():
   
   form_data = request.form
   task = form_data["title"]
   add_item(task)
      
   return redirect('/')


@app.route('/items/complete', methods = ['POST', 'GET'])
def complete_item():
   if request.method == 'POST':
      form_data = request.form
      task_id = int(form_data["id"])
      existing_item = get_item(task_id)
      if (existing_item != None) and (existing_item['status'] != 'Completed'):
         updated_item = { 'id': task_id, 'status': 'Completed', 'title': existing_item['title'] }
         save_item(updated_item)
         
   return redirect('/')


      form_data = request.form
@app.route('/items/remove', methods = ['POST', 'GET'])
def remove_items():
   if request.method == 'POST':
      task_id = int(form_data["id"])
      
      remove_item_by_id(task_id)
      
   return redirect('/')


if __name__ == '__main__':
    app.run()
