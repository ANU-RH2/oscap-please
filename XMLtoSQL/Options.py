__author__ = 'sauski'
# Small little class the parser hands back, contains options and inputs
# set buy the user.


class Options:

    def __init__(self, files, database_name, database_user):
        self.files = files
        self.database_name = database_name
        self.database_user = database_user

    def __str__(self):
        return '{Files: ' + ', '.join(self.files) + \
               ', Database Name: ' + self.database_name + \
               ', Database User: ' + self.database_user + '}'