
from todo_app.data.status import Status
from todo_app.data.task import Task
import requests
import json
import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
 
class TrelloBoard:

    def __init__(self, board_id, api_key, server_token):
        self.board_id = board_id
        self.api_key = api_key
        self.server_token = server_token


    """
        Gets all the cards available on the board

        Returns: 
            a list of tuples representing the lists available on the board (id, name)


        """
    def get_all_cards_on_board(self):
        tasks = []
        print("Getting the cards from the trello board")
    
        get_cards_query = f"https://api.trello.com/1/boards/{self.board_id}/cards?key={self.api_key}&token={self.server_token}"
        response = requests.get(get_cards_query)
        if (response.status_code == 200):
            json_response = response.json()
            
            for value in json_response:
                card_id = value['id']
                
                card_status = "Unknown"
                get_list_for_card_query = f"https://api.trello.com/1/cards/{card_id}/list?key={self.api_key}&token={self.server_token}"
                response = requests.get(get_list_for_card_query)
                if (response.status_code == 200):
                    json_response_for_list = response.json()
                    card_status = json_response_for_list['name']
                due_date, last_modified = self.calculate_due_date_and_last_modified_date(value['due'],value['dateLastActivity'])
                new_task = Task(card_id, value['name'], value['desc'], card_status, due_date, last_modified)
                tasks.append(new_task)

        return tasks


    """
        Gets the lists available on the board

        Returns: 
            a list of tuples representing the lists available on the board (id, name)


        """
    def get_lists(self):
        statuses = []
        print("Getting the lists from the trello board")
    
        get_lists_query = f"https://api.trello.com/1/boards/{self.board_id}/lists?key={self.api_key}&token={self.server_token}"
        response = requests.get(get_lists_query)
        if (response.status_code == 200):
            json_response = response.json()
        
            for value in json_response:
                statuses.append(Status(value['id'], value['name']))

        return statuses

    def calculate_due_date_and_last_modified_date(self, due_date_str, last_modified_str):
        due_date = None
        last_modified = None
        if due_date_str is not None:
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        if last_modified_str is not None:
            last_modified = datetime.datetime.strptime(last_modified_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return due_date, last_modified
            
    def get_cards_in_list(self, list):
        tasks = []
        
        get_cards_query = f"https://api.trello.com/1/lists/{list.id}/cards?key={self.api_key}&token={self.server_token}"
        response = requests.get(get_cards_query)
        if (response.status_code == 200):
            json_response = response.json()

            for value in json_response:
                due_date, last_modified = self.calculate_due_date_and_last_modified_date(value['due'],value['dateLastActivity'])
                
                new_task = Task(value['id'], value['name'], value['desc'], list.title, due_date, last_modified)
                tasks.append(new_task)

        return tasks


    def get_list_id_from_name(self, list_name):
        lists = self.get_lists()
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
    def update_task(self, card_id, list_name):
        
        print("Updating a task")
        
        list_id = self.get_list_id_from_name(list_name)
        
        update_card_query = f"https://api.trello.com/1/cards/{card_id}?key={self.api_key}&token={self.server_token}&idList={list_id}"

        response = requests.put(update_card_query)
        if (response.status_code == 200):
            print("Task updated successfully")


        

    def get_last_modified_time_for_a_task(self, id):
        modified_time = None
        print(f"Getting the last modified time for card {id}")

        time_query = f"https://api.trello.com/1/cards/{id}/dateLastActivity?key={self.api_key}&token={self.server_token}"

        response = requests.put(time_query)
        if (response.status_code == 200):
            json_response = response.json()

            modified_time = json_response["_value"]
            
        return modified_time   

    """
        Completes a task by moving it to the completed list

        Args:
            card_id: The ID of the card to update.

        """
    def complete_task(self, card_id):
        print("Completing a task")
        self.update_task(card_id, 'Done')

    """
        Starts a task by moving it to the Doing list

        Args:
            card_id: The ID of the card to update.

        """
    def start_task(self, card_id):
        print("Starting a task")
        self.update_task(card_id, 'Doing')

    """
        Reopens a task by moving it to the To Do list

        Args:
            card_id: The ID of the card to update.

        """
    def reopen_task(self, card_id):
        print("Reopening a task")
        self.update_task(card_id, 'To Do')

    """
        Deletes a task

        Args:
            card_id: The ID of the card to delete.

        """
    def delete_task(self, card_id):
        
        print("Deleting a task")
    
        delete_task_query = f"https://api.trello.com/1/cards/{card_id}?key={self.api_key}&token={self.server_token}"

        response = requests.delete(delete_task_query)
        if (response.status_code == 200):
            print("Task deleted successfully")

    """
        Adds a new task by creating a card on the To Do List

        Args:
            task_name: The name of the task

        """
    def add_task(self, task_name, description="", duedate=""):
        
        print("Adding a new task")
        
        url = "https://api.trello.com/1/cards"

        todo_list_id = self.get_list_id_from_name("To Do")

        add_task_query = f"https://api.trello.com/1/cards?key={self.api_key}&token={self.server_token}&name={task_name}&desc={description}&due={duedate}&idList={todo_list_id}"

        response = requests.post(add_task_query)

        if (response.status_code == 200):
            print("Task added successfully")


