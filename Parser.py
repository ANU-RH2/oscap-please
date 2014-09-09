#                  _____  _______  ______ _______ _______  ______
#                 |_____] |_____| |_____/ |______ |______ |_____/
#                 |       |     | |    \_ ______| |______ |    \_
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: MVP
#          Modified: 09/09/2014 by Thomas Antioch - u5006059
#
# This is a simple command line parsing module, basically it is handed the
# user inputted command line arguments and then generated an SQLtoXML options
# object from them. It is my hope that this is the level where the disparate
# OSP components will come together. Currently there are some edge cases that
# are missed on the parsing, it is my intention that when OSP comes together
# to move to a library based parsing system.
#TODO include other OSP component inputs.

__author__ = 'u5195918'
import os.path
import XMLtoSQL.Options
from XMLtoSQL import Controller
import makereport


def print_help(arguments):
    # Arguments is never technically used, but is needed here anyway
    # as the function is picked blindly from a dictionary
    print 'usage: OSP.py [-h | -r | -i file [file ...] ' \
          '[-db dbname] [-dbuser dbuser]]'
    print ''
    print 'Insert OpenSCAP audit results into database and generate reports'
    print ''
    print ' -h           show this help message and exit'
    print ' -i           insert reports into database (can '
    print ' -r           generate a report from database'
    print 'positional arguments:'
    print '  file        an openscap XML audit result file'
    print '  dbname      name of the PSQL database to connect to, ' \
          'default is osp'
    print '  dbuser      user to connect to database through, default is' \
          ' postgres'
    print ''
    print 'optional arguments:'
    print '  -db         connect to specific database'
    print '  -dbuser     specify database username'
    quit()


def invalid_argument(argument):
    print 'Invalid, Missing or Malformed Option or Argument: ' + argument
    print 'Use -h for help'
    quit()


def missing_file(filename):
    print 'File ' + filename + ' not found, skipping'


def input_files(arguments):
    # List of files passed in
    files = []
    # Set Defaults
    database_name = 'osp'
    database_user = 'postgres'
    # Loop over the files
    i = 2
    argument = arguments[i]

    while argument != '-db' and argument != '-dbuser':
        # Loop until we find a DB option
        # Does the file exist?
        if os.path.isfile(argument):
            files.append(argument)
        else:
            missing_file(argument)

        i += 1
        argument = arguments[i]

    while i < len(arguments):
        # More to do, must have handed in a database option
        # Did we get handed a database?
        if arguments[i] == '-db':
            try:
                database_name = arguments[i + 1]
            except IndexError:
                invalid_argument(arguments[i])

        elif arguments[i] == '-dbuser':
            try:
                database_user = arguments[i + 1]
            except IndexError:
                invalid_argument(arguments[i])

        i += 1

    # Create an options object to hand back
    options = XMLtoSQL.Options.Options(files, database_name, database_user)
    controller = Controller.Controller(options)
    controller.extract_and_insert()

def make_report(arguments):
    makereport.gen_report();

inputs = {'-h': print_help,
          '-i': input_files,
          '-r': make_report}


def parse(arguments):
    # Any of the possible input paths leads to either an options object,
    # or the end of the program.

    # Did we even get any arguments?
    if len(arguments) == 1:
        print_help('')
        return
    else:
        return inputs.get(arguments[1], invalid_argument)(arguments)


