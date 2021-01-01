import datetime
class Task:
    

    def __init__(self, id, title, description = "", status = "To Do", duedate=datetime.time()):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.duedate = duedate

    def is_doing(self):
        return self.status == "Doing"

    def is_done(self):
        return self.status == "Done"

    
    def is_to_do(self):
        return self.status == "To Do"