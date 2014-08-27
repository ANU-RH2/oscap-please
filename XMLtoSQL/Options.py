#               _____   _____  _______ _____  _____  __   _ _______
#              |     | |_____]    |      |   |     | | \  | |______
#              |_____| |          |    __|__ |_____| |  \_| ______|
#
#       Written By: Theodore Olsauskas-Warren - u5195918f
#               In: August 2014
#          Version: MVP
#
# Simple object that captures the expected command line arguments for the
# XMLtoSQL component. This object is created by the command line parser then
# handed to the XMLtoSQL controller object. It is expected that this will grow
# to accommodate other command line arguments in future, conspicuously missing
# is any concept of a database user password.
# TODO Add functionality for database user password.

__author__ = 'u5195918'


class Options:

    def __init__(self, files, database_name, database_user):
        self.files = files
        self.database_name = database_name
        self.database_user = database_user

    def __str__(self):
        return '{Files: ' + ', '.join(self.files) + \
               ', Database Name: ' + self.database_name + \
               ', Database User: ' + self.database_user + '}'