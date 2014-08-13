__author__ = 'sauski'

# Command line option parsing object.
# Basically you hand it the input string and it
# gives you back a list of file names
# This is also responsible for throwing errors
# for bad input etc.

#TODO HAS ONLY BEEN EDITED FOR XMLTOSQL
import os.path

import OSP.XMLtoSQL.Options


def print_help(arguments):
    print 'usage: OSP.py [-h] [-i file [file ...] ' \
          '[-db dbname] [-dbuser dbuser]]'
    print ''
    print 'Insert openscap audit results into database'
    print ''
    print 'positional arguments:'
    print '  file        an openscap XML audit result file'
    print '  dbname      name of the PSQL database to connect to, ' \
          'default is OSP'
    print '  dbuser      user to connect to database through, default is' \
          ' postgres'
    print ''
    print 'optional arguments:'
    print '  -h          show this help message and exit'
    print '  -i          list of files to insert'
    print '  -db         connect to specific database'
    print '  -dbuser     specify database username'


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
    database_name = 'OSP'
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
    options = OSP.XMLtoSQL.Options.Options(files, database_name, database_user)
    return options

inputs = {'-h': print_help,
          '-i': input_files}


def parse(arguments):
    # Any of the possible input paths leads to either an options object,
    # or the end of the program.

    # Did we even get any arguments?
    if len(arguments) == 1:
        print_help('')
        return
    else:
        return inputs.get(arguments[1], invalid_argument)(arguments)


