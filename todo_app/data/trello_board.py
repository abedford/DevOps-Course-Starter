
from todo_app.data.status import Status
from todo_app.data.task import Task
import requests
import json

import os
from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
 
board_id = os.getenv('BOARD_ID')
api_key = os.getenv('API_KEY')
server_token = os.getenv('SERVER_TOKEN')
    

 

"""
    Gets all the cards available on the board

    Returns: 
        a list of tuples representing the lists available on the board (id, name)


    """
def get_all_cards_on_board():
    tasks = []
    print("Getting the cards from the trello board")
   
    get_cards_query = f"https://api.trello.com/1/boards/{board_id}/cards?key={api_key}&token={server_token}"
    response = requests.get(get_cards_query)
    if (response.status_code == 200):
        json_response = response.json()
    
        print(json_response)
        
        for value in json_response:
            card_id = value['id']
            
            card_status = "Unknown"
            get_list_for_card_query = f"https://api.trello.com/1/cards/{card_id}/list?key={api_key}&token={server_token}"
            response = requests.get(get_list_for_card_query)
            if (response.status_code == 200):
                json_response_for_list = response.json()
                print(json_response_for_list)
                card_status = json_response_for_list['name']
                print(f"Card status is {card_status}")

            new_task = Task(card_id, value['name'], value['desc'], card_status, value['due'])
            tasks.append(new_task)

    return tasks


"""
    Gets the lists available on the board

    Returns: 
        a list of tuples representing the lists available on the board (id, name)


    """
def get_lists():
    statuses = []
    print("Getting the lists from the trello board")
   
    get_lists_query = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={server_token}"
    response = requests.get(get_lists_query)
    if (response.status_code == 200):
        json_response = response.json()
    
        for value in json_response:
            statuses.append(Status(value['id'], value['name']))

    return statuses

def get_cards_in_list(list):
    tasks = []
    
    get_cards_query = f"https://api.trello.com/1/lists/{list.id}/cards?key={api_key}&token={server_token}"
    response = requests.get(get_cards_query)
    if (response.status_code == 200):
        json_response = response.json()

        for value in json_response:
            new_task = Task(value['id'], value['name'], value['desc'], list.title, value['due'])
            tasks.append(new_task)

    return tasks


def get_list_id_from_name(list_name):
    lists = get_lists()
    for list in lists:
        if ( list.title == list_name):
            return list.id
    
    print("Didn't find list name, returning empty string")
    return ""

        
"""
    Updates a task by moving it from one list to another

    Args:
        card_id: The ID of the card to update.
        list_name: The name of the list you want the card to be in

    """
def update_task(card_id, list_name):
    
    print("Updating a task")
    
    list_id = get_list_id_from_name(list_name)
    
    update_card_query = f"https://api.trello.com/1/cards/{card_id}?key={api_key}&token={server_token}&idList={list_id}"

    response = requests.put(update_card_query)
    if (response.status_code == 200):
        print("Task updated successfully")
    

"""
    Completes a task by moving it to the completed list

    Args:
        card_id: The ID of the card to update.

    """
def complete_task(card_id):
    print("Completing a task")
    update_task(card_id, 'Done')

"""
    Completes a task by moving it to the To Do list

    Args:
        card_id: The ID of the card to update.

    """
def reopen_task(card_id):
    print("Reopening a task")
    update_task(card_id, 'To Do')

"""
    Deletes a task

    Args:
        card_id: The ID of the card to delete.

    """
def delete_task(card_id):
    
    print("Deleting a task")
   
    delete_task_query = f"https://api.trello.com/1/cards/{card_id}?key={api_key}&token={server_token}"

    response = requests.delete(delete_task_query)
    if (response.status_code == 200):
        print("Task deleted successfully")

"""
    Adds a new task by creating a card on the To Do List

    Args:
        task_name: The name of the task

    """
def add_task(task_name, description="", duedate=""):
    
    print("Adding a new task")
    
    url = "https://api.trello.com/1/cards"

    todo_list_id = get_list_id_from_name("To Do")

    query = {
    'key': os.getenv('API_KEY'),
    'token': os.getenv('SERVER_TOKEN')   ,
    'idList': f'{todo_list_id}',
    'name': task_name,
    'desc': description,
    'due': duedate
    }

    response = requests.request(
        "POST",
        url,
        params=query
        )

    print(query)

    print(response)    
    if (response.status_code == 200):
        print("Task added successfully")


