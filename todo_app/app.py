
from todo_app.data.session_items import add_item, get_items
from flask import Flask, render_template, request

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   items = get_items()
   return render_template('index.html', title='To Do App', items=items)


@app.route('/items/add', methods = ['POST', 'GET'])
def add_items():
   if request.method == 'POST':
      form_data = request.form
      task = form_data["title"]
      add_item(task)

      return index()
        
   return index()

if __name__ == '__main__':
    app.run()
