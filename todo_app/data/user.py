from flask_login import UserMixin

class User( UserMixin ):

    def __init__(self, id, role):
        self.id = id
        self.role = role

    id = ""
    
    def __repr__(self):
        return '<User{} with Role{}>'.format(self.id, self.role)


# class Role:
#     def __init__(self, id, role):
#         self.id = id
#         self.role = role

    
#     def __repr__(self):
#         return '<Role{},{}>'.format(self.id, self.role)

