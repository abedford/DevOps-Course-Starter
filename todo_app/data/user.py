from flask_login import UserMixin

class User( UserMixin ):

    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    id = ""
    
    def __repr__(self):
        return '<User{} with Role{}>'.format(self.username, self.role)

