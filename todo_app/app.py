
from todo_app.data.trello_board import *
from todo_app.data.viewmodel import *
from flask import Flask, render_template, request, redirect


    


def create_app():
   app = Flask(__name__)
   item_view_model = None
   board_id = os.getenv('BOARD_ID')
   api_key = os.getenv('API_KEY')
   server_token = os.getenv('SERVER_TOKEN')
   trello_board = TrelloBoard(board_id, api_key, server_token)
   #  All the routes and setup code etc


   @app.route('/')
   def index():
      show_all = request.args.get('show_all')
      
      show_all_bool = show_all == "yes"
      print(f"Show all value is {show_all_bool}")
      cards = trello_board.get_all_cards_on_board()
      item_view_model = ViewModel(cards)
      return render_template('index.html', title='To Do App',
         view_model=item_view_model, show_all=show_all_bool)


   @app.route('/items/add', methods = ['POST'])
   def add_item():
      form_data = request.form
      task_title = form_data["title"]
      task_desc = form_data["description"]
      task_due_date = form_data["duedate"]
      print(f"Adding task with {task_title} {task_desc} {task_due_date}")
      
      
      trello_board.add_task(task_title, task_desc, task_due_date)  
      
      return redirect('/')

   @app.route('/items/complete', methods = ['POST', 'GET'])
   def complete_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         trello_board.complete_task(task_id)
            
      return redirect('/')


     
   @app.route('/items/remove', methods = ['POST'])
   def remove_item():

      if request.method == 'POST':
         
         form_data = request.form
         task_id = form_data["id"]
         print(f"The form data for delete is: {form_data}")
         trello_board.delete_task(task_id)
         
      return redirect('/')


   @app.route('/items/start', methods = ['POST'])
   def start_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         
         trello_board.start_task(task_id)
         
      return redirect('/')

   @app.route('/items/restart', methods = ['POST'])
   def restart_item():
      if request.method == 'POST':
         form_data = request.form
         task_id = form_data["id"]
         
         trello_board.reopen_task(task_id)
         
      return redirect('/')


   if __name__ == '__main__':
      app.run()


   return app




