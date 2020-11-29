class Task:
    

    def __init__(self, id, title, status = "To Do") -> None:
        self.id = id
        self.title = title
        self.status = status


    def __str__(self):
     return f"ID: {self.id} Status: {self.status}"
