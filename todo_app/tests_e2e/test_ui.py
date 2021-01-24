import os
from threading import Thread

from todo_app.app import *
from todo_app.data.trello_board import *
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pytest

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable

    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    board = TrelloBoard(board_id = None, api_key = api_key, server_token = server_token, name = "test board")
    
    if board is not None:
        os.environ['BOARD_ID'] = board.board_id
    
        # construct the new application
        application = create_app(board)
        
        # start the app in its own thread.
        thread = Thread(target=lambda: application.run(use_reloader=False))
        thread.daemon = True
        thread.start()
        yield application
        
        # Tear Down
        thread.join(1)
        board.delete_board(board.board_id)
    else:
        print("Could not create a temporary trello board")


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

    driver = webdriver.Chrome(options=chrome_options)
    with webdriver.Chrome() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'
