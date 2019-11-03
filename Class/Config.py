

class Config:
    """Manual configuration of database

    Return parameters of mysql
    """
    def __init__(self):
        self.host = ""
        self.user = ""
        self.passwd = ""
        self.database = ""

    def config(self):
        self.host="localhost"
        self.user="testeur"
        self.passwd="testeur"
        self.database="test"
        return self.host, self.user, self.passwd, self.database