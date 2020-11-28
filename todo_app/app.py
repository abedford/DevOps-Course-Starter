
from todo_app.data.session_items import *
from todo_app.data.trello_board import *
from operator import itemgetter
from flask import Flask, render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   lists = get_lists()
   all_cards = []
   for list in lists:
      all_cards.extend(get_cards_in_list(list))

   print(all_cards)
   # sorted_cards = sorted(all_cards, key = itemgetter('status'), reverse=True)
   return render_template('index.html', title='To Do App', items=all_cards)


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


###  update a card from one board to the other
### https://api.trello.com/1/cards/5fb8296676b04e7c6bfd1d74?key=1b2fee4ea3ee014a8fb424eb98524969&token=e17fc953a77e0043ac42e271e4a25d68d4115b492d42dcf8f811935d441fb0b5&idList=5fb8296a9626b51f4c9a4df6