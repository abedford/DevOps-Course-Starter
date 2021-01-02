import datetime
class Task:
    

    def __init__(self, id, title, description = "", status = "To Do", duedate=datetime.time()):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.duedate = duedate
        self.modified_date = datetime.datetime.now()

    def is_doing(self):
        return self.status == "Doing"

    def is_done(self):
        return self.status == "Done"

    def is_to_do(self):
        return self.status == "To Do"

    def set_mofidied_date(self, date):
        self.modified = date