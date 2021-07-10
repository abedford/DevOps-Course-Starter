

from todo_app.data.task import Task

import datetime
import pymongo
import ssl
import pprint
from bson import ObjectId

from os.path import join, dirname
from dotenv import load_dotenv
 
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
 
class ToDoMongoClient:

    def __init__(self, user, password, server, database, connection):
        
        self.client = pymongo.MongoClient(f"{connection}://{user}:{password}@{server}/{database}?w=majority", ssl=True, tlsAllowInvalidCertificates=True)
        print(f"Connected to {server}/{database}")
        self.database=self.client[database]
        self.task_collection = self.database.tasks

    def drop_collection(self):
        print(f"Dropping {self.task_collection.name} collection")
        self.task_collection.drop()
   
    """
        Gets all the tasks

        Returns: 
            a list of tasks in the db


        """
    def get_all_tasks(self):
        tasks = []
        print("Getting the tasks from the mongo db")
    
        task_objects = self.task_collection.find({})
        for task_object in task_objects:
           
            task = Task(task_object["_id"],task_object["title"], task_object["description"], task_object["status"], task_object["duedate"], task_object["modified_date"])
            tasks.append(task)

        return tasks

            
    """
        Updates a task by changing its status

        Args:
            task_id: The ID of the task to update.
            status: The new status of the task

        """
    def update_task(self, task_id, status):
        
        print("Updating a task")
        filter = { "_id": ObjectId(task_id) }
        newstatus = { "$set": { "status": status, "modified_date": datetime.datetime.utcnow()} }
    
        self.task_collection.update_one(filter, newstatus)


        

    """
        Completes a task by moving it to the completed list

        Args:
            task_id: The ID of the card to update.

        """
    def complete_task(self, task_id):
        print("Completing a task")
        self.update_task(task_id, 'Done')

    """
        Starts a task by moving it to the Doing list

        Args:
            task_id: The ID of the card to update.

        """
    def start_task(self, task_id):
        print("Starting a task")
        self.update_task(task_id, 'Doing')

    """
        Reopens a task by moving it to the To Do list

        Args:
            task_id: The ID of the card to update.

        """
    def reopen_task(self, task_id):
        print("Reopening a task")
        self.update_task(task_id, 'To Do')

    """
        Deletes a task

        Args:
            task_id: The ID of the card to delete.

        """
    def delete_task(self, task_id):
        
        print("Deleting a task")

        self.task_collection.delete_one({"_id": ObjectId(task_id)})

    
       

    """
        Adds a new task by creating a card with To Do status

        Args:
            task_name: The name of the task
            description: Description of the task
            duedate: The date it is due

        """
    def add_task(self, task_name, description="", duedate=""):
        
        print("Adding a new task")
        
        task = {"title": task_name, 
                "status": "To Do",
                "description": description,
                "duedate": duedate,
                "modified_date": datetime.datetime.utcnow()}

        
        task_id = self.task_collection.insert_one(task).inserted_id

        print(f"Task {task_id} added successfully")
        print(f"Tasks are now {self.task_collection.find()}")
        return task_id


