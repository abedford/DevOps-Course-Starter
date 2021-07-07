
#f#rom dotenv.main import find_dotenv, load_dotenv
from todo_app.data.todo_mongo_client import *
from dotenv.main import find_dotenv, load_dotenv
import pytest
import os

def test_can_connect_to_mongo_db_store_a_task_and_delete_it():

    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
    mongo_srv = os.getenv('MONGO_SRV')
    mongo_user = os.getenv('MONGO_USER')
    mongo_pwd = os.getenv('MONGO_PWD')
    mongo_connection = os.getenv('MONGO_CONNECTION')

    testClient = ToDoMongoClient(mongo_user, mongo_pwd, mongo_srv, "test_db", mongo_connection)
    tasks = testClient.get_all_tasks()
    current_no_of_tasks = len(tasks)
    
    task_id = testClient.add_task("test_task", "test description", "01/01/1900")
    list_of_tasks = testClient.get_all_tasks()
    assert(len(list_of_tasks) == current_no_of_tasks+1)
    testClient.delete_task(task_id)
    list_of_tasks = testClient.get_all_tasks()
    assert(len(list_of_tasks) == current_no_of_tasks)


