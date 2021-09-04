import os
from threading import Thread
from dotenv.main import find_dotenv, load_dotenv
from todo_app.app import create_app
from todo_app.data.todo_mongo_client import *
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
    os.environ['FLASK_SKIP_LOGIN'] = "True"
    os.environ['MONGO_DB'] = "test_db"
    
    mongo_srv = os.getenv('MONGO_SRV')
    mongo_user = os.getenv('MONGO_USER')
    mongo_pwd = os.getenv('MONGO_PWD')
    mongo_connection = os.getenv('MONGO_CONNECTION')

    testClient = ToDoMongoClient(mongo_user, mongo_pwd, mongo_srv, "test_db", mongo_connection)
    
    
    admin_user = testClient.add_user("admin_user", "Admin")
    writer_user = testClient.add_user("writer_user", "Writer")
    reader_user = testClient.add_user("reader_user", "Reader")

    application = create_app()
        
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
        
    # Tear Down
    thread.join(1)
    testClient.delete_user(admin_user.id)
    testClient.delete_user(writer_user.id)
    testClient.delete_user(reader_user.id)
    

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox") #bypass OS security model
    options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems

   
    with webdriver.Chrome(options=options) as driver:
        yield driver

def test_user_admin(driver, test_app):
    before_XPath = "//*[@id='users']/tbody/tr["
    aftertd_XPath = "]/td["
    aftertr_XPath = "]"


    driver.get('http://localhost:5000/users')

    assert driver.title == 'To-Do App'

    num_rows = len (driver.find_elements_by_xpath("//*[@id='users']/tbody/tr"))

    assert num_rows == 4, "Should be 4 rows in the table"
    
    user1XPath = before_XPath + str(2) + aftertd_XPath + str(1) + aftertr_XPath
    user1UsernameCellText = driver.find_element_by_xpath(user1XPath).text

    user1XPath = before_XPath + str(2) + aftertd_XPath + str(2) + aftertr_XPath
    user1RoleCellText = driver.find_element_by_xpath(user1XPath).text

    assert user1UsernameCellText == "admin_user", "First user should be admin_user username"
    assert user1RoleCellText == "Admin", "First user should be admin role"

    user2XPath = before_XPath + str(3) + aftertd_XPath + str(1) + aftertr_XPath
    user2UsernameCellText = driver.find_element_by_xpath(user2XPath).text

    user2XPath = before_XPath + str(3) + aftertd_XPath + str(2) + aftertr_XPath
    user2RoleCellText = driver.find_element_by_xpath(user2XPath).text

    assert user2UsernameCellText == "writer_user", "Second user should be writer_user username"
    assert user2RoleCellText == "Writer", "First user should be writer role"

    user3XPath = before_XPath + str(4) + aftertd_XPath + str(1) + aftertr_XPath
    user3UsernameCellText = driver.find_element_by_xpath(user3XPath).text

    user3XPath = before_XPath + str(4) + aftertd_XPath + str(2) + aftertr_XPath
    user3RoleCellText = driver.find_element_by_xpath(user3XPath).text

    assert user3UsernameCellText == "reader_user", "Third user should be reader_user username"
    assert user3RoleCellText == "Reader", "Third user should be reader role"



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
        restart_button = driver.find_element_by_name("restart")
        assert False, "Restart button was not found"
    except NoSuchElementException:
        assert True, "Restart button was not found"

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
        
   


    

    
  