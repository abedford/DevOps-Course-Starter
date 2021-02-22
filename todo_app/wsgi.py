from todo_app.app import app

def start(environ, start_fn):
    start_fn('200 OK', [('Content-Type', 'text/plain')])
    app.run()
