
#f#rom dotenv.main import find_dotenv, load_dotenv
from todo_app.data.todo_mongo_client import *
import pytest
import os

def test_can_get_all_tasks():

    mongo_srv = os.getenv('MONGO_SRV')
    mongo_user = os.getenv('MONGO_USER')
    mongo_pwd = os.getenv('MONGO_PWD')

    testClient = ToDoMongoClient(mongo_user, mongo_pwd, mongo_srv, "test_db")
    list_of_tasks = testClient.get_all_tasks()
    assert(len(list_of_tasks) == 0)
    task_id = testClient.add_task("test_task", "test description", "01/01/1900")
    list_of_tasks = testClient.get_all_tasks()
    assert(len(list_of_tasks) == 1)
    testClient.remove_task(task_id)
    list_of_tasks = testClient.get_all_tasks()
    assert(len(list_of_tasks) == 0)


