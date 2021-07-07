import os
from unittest.mock import Mock, patch
import pytest
import mongomock
from dotenv.main import find_dotenv, load_dotenv

from todo_app.app import *

dummy_task_id = ""
db_client = pymongo.MongoClient("test.mongodb.net")

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    

    with mongomock.patch(servers=(('test.mongodb.net', 27017),)):
        # Create the new app.
        test_app = create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client


def test_index_page(client):
    
    # set up some data
    dummy_task_id = add_dummy_task()
    response = client.get('/')

    assert response.status_code == 200

    string = response.data.decode('utf-8')
    assert "Dummy Task" in string


def test_add_task(client):
    data = {
        "title": "Dummy Task 2",
        "description": "Dummy Description 2",
        "duedate": datetime.datetime.utcnow()
    }
    
    response = client.post('/items/add', data=data)

    assert response.status_code == 302

    response = client.get('/')

    assert response.status_code == 200

    string = response.data.decode('utf-8')
    assert "Dummy Task 2" in string


def test_complete_task(client):
    dummy_task_id = add_dummy_task("Doing")
    data = {'id': dummy_task_id}
    response = client.post('/items/complete', data=data)

    assert response.status_code == 302


def test_remove_task(client):
    dummy_task_id = add_dummy_task()
    data = {'id': dummy_task_id}
    
    response = client.post('/items/remove', data=data)

    assert response.status_code == 302


def test_start_task(client):
     
    dummy_task_id = add_dummy_task()
    data = {'id': dummy_task_id}

    response = client.post('/items/start', data=data)

    assert response.status_code == 302
 

def test_restart_task(client):
   
    dummy_task_id = add_dummy_task("Done")
    data = {'id': dummy_task_id}

    response = client.post('/items/restart', data=data)

    assert response.status_code == 302


def add_dummy_task(status="To Do"):
    
       
    task = {"title": "Dummy Task", 
                "status": status,
                "description": "",
                "duedate": datetime.datetime.utcnow(),
                "modified_date": datetime.datetime.utcnow()}

    task_collection = db_client["test_db"].tasks
    task_id = task_collection.insert_one(task).inserted_id
    return task_id


def check_task_exists(task_name):
    task_collection = db_client["test_db"].tasks
    
    filter = { "title": task_name }
    result = task_collection.find_one(filter)
    print(f"Found {len(result)} results")
    return len(result)

