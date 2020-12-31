import datetime
class Task:
    

    def __init__(self, id, title, description = "", status = "To Do", duedate=datetime.time()):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.duedate = duedate

