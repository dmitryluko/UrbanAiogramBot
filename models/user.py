class User:
    def __init__(self, username, mail, age, balance=1000, id=None):
        self.id = id
        self.username = username
        self.mail = mail
        self.age = age
        self.balance = balance
