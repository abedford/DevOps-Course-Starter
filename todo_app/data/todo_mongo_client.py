

from todo_app.data.user import User
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
        self.user_collection = self.database.users

    def drop_collection(self):
        print(f"Dropping {self.task_collection.name} collection")
        self.task_collection.drop()
        self.user_collection.drop()
   
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

    """
        Adds a new user with a username and a role

        Args:
            username: The username/login of the user
            role: The role of the user

    """
    def add_user(self, username, role):
        
        new_user = {"username": username,
                "role": role}

        
        user= self.database.users.insert_one(new_user)

        print(f"User {user} added successfully with {user.inserted_id} as the ID and {role} as the role")
        return User(user.inserted_id, username, role)

    """
        Deletes a user

        Args:
            user_id: The ID of the user to delete.

        """
    def delete_user(self, user_id):
        
        print("Deleting a user")

        self.database.users.delete_one({"_id": ObjectId(user_id)})

    """
        Gets user by userid

        Args:
            user_id: The id of the user

    """
    def get_user_by_id(self, user_id):
        
        print(f"Looking for user with user_id {user_id}")
    
        user_object = self.database.users.find_one({"_id": ObjectId(user_id)})
        if not user_object:
            print("Didn't find the user")
            return None
        print("Found the user, returning user object")
        return User(user_object["_id"], user_object["username"], user_object["role"])

    """
        Gets user by username

        Args:
            username: The username of the user to get

    """
    def get_user_by_username(self, username):
        
        print(f"Looking for user with username {username}")
    
        user_object = self.database.users.find_one({"_id": username})
        if not user_object:
            print("Didn't find the user")
            return None
        print("Found the user, returning user object")
        return User(user_object["_id"], user_object["username"], user_object["role"])

    """
        Gets all the users that exist in the database

        Args:

    """    
    def get_all_users(self):
        users = []
        print("Getting the users from the mongo db")
    
        user_objects = self.database.users.find({})
        for user_object in user_objects:
           
            user = User(user_object["_id"],user_object["username"], user_object["role"])
            users.append(user)

        return users

    """
        Updates a user with a new role

        Args:
            userid: The id of the user
            description: The new role for the user

    """
    def update_user(self, userid, role):
        
        print(f"Updating a user {userid} with role {role}")
        filter = { "_id": ObjectId(userid) }
        newrole = { "$set": { "role": role} }
    
        self.database.users.update_one(filter, newrole)



