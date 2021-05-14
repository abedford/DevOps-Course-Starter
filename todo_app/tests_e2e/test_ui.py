import os
from threading import Thread
from dotenv.main import find_dotenv, load_dotenv
from todo_app.app import create_app
from todo_app.data.trello_board import TrelloBoard
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

import pytest

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    
    board_id = TrelloBoard.create_new_board(api_key, server_token, "test board")
    
    if board_id is not None:
        os.environ['BOARD_ID'] = board_id
    
        # construct the new application
        application = create_app()
        
        # start the app in its own thread.
        thread = Thread(target=lambda: application.run(use_reloader=False))
        thread.daemon = True
        thread.start()
        yield application
        
        # Tear Down
        thread.join(1)
        TrelloBoard.delete_board(api_key, server_token, board_id)
    else:
        print("Could not create a temporary trello board")


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox") #bypass OS security model
    options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems

   
    with webdriver.Chrome(options=options) as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    sample_text = "Test Task"
    new_task_text_field = driver.find_element_by_id("task_title")
    new_task_text_field.send_keys(sample_text)

    sample_text = "Test Task Description"
    new_task_text_field = driver.find_element_by_id("task_description")
    new_task_text_field.send_keys(sample_text)
    
    print("Creating a new task")
    driver.find_element_by_id("add_task_button").click()

    print("Starting the task")
    driver.find_element_by_name("start").click()


    print("Completing the task")
    driver.find_element_by_name("complete").click()


    driver.find_element_by_name("restart").click()

    driver.find_element_by_name("delete-todo").click()
    time.sleep(1)

    try:
        start_button = driver.find_element_by_name("start")
        assert False, "Start button was found"
    except NoSuchElementException:
        assert True, "Start button was not found"
        
    try:
        complete_button = driver.find_element_by_name("complete")
        assert False, "Complete button was not found"
    except NoSuchElementException:
        assert True, "Complete button was not found"
        
    try:
        restart_button = driver.find_element_by_name("restart")
        assert False, "Restart button was not found"
    except NoSuchElementException:
        assert True, "Restart button was not found"


    

    
  