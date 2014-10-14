#               _____   _____  _______ _____  _____  __   _ _______
#              |     | |_____]    |      |   |     | | \  | |______
#              |_____| |          |    __|__ |_____| |  \_| ______|
#
#       Written By: Theodore Olsauskas-Warren - u5195918f
#               In: August 2014
#          Version: Extended Edition
#
# Simple object that is used to encapsulate the command line arguments handed to
# OSP. The default values are not set here, they are set in the Parser module.
# This object gets created by the parser, then passed to the relevant insertion
# or report generation module where it's contents are read.

__author__ = 'u5195918'


class Options:

    def __init__(self, files, database_name, database_user, log_file_name,
                 file_verbosity, std_out_verbosity, log_file_width):
        self.files = files
        self.database_name = database_name
        self.database_user = database_user
        self.log_file_name = log_file_name
        self.file_verbosity = file_verbosity
        self.std_out_verbosity = std_out_verbosity
        self.log_file_width = log_file_width

    def __str__(self):
        return '{Files: ' + ', '.join(self.files) + \
               ', Database Name: ' + self.database_name + \
               ', Database User: ' + self.database_user + '}'