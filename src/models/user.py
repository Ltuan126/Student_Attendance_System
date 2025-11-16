
class User:
    def __init__(self, user_id, name, email, password, role):
        self.id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        # Backwards-compatible aliases used by some CLI code
        self.user_id = user_id
        self.username = name

class Student(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role="student")

class Lecturer(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role="lecturer")

class Admin(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password, role="admin")
