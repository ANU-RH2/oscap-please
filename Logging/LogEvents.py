#         _____   ______      _______ _    _ _______ __   _ _______ _______
# |      |     | |  ____      |______  \  /  |______ | \  |    |    |______
# |_____ |_____| |_____|      |______   \/   |______ |  \_|    |    ______|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: MVP
#
# This module contains the different types of logging objects, east object
# represents a different event that can be logged by the logging class.
# Essentially, when you want to log something create one of these and fill it
# out with the relevant information, then pass it to the logging class for
# entry into the file. Verbosity level represents at which level the event
# will be printed, verbosity levels are from 1 to 5 in increase order of the
# volume of events logged. This means that the more critical the event is, the
# lower verbosity value it has (so it appears more often). Events marked as
# fatal will end program execution, their text will also be prepended with the
# 'FATAL:' prefix and will be printed to the terminal regardless of verbosity
# level.
# TODO Get developers to flesh this out with more logging events
__author__ = 'u5195918'


class LogWidthSizeError:
    # Log Object for when a user specifies an invalid log width size
    def __init__(self, requested_size, new_size):
        self.requested_size = requested_size
        self.new_size = new_size
        self.verbosity = 1
        self.fatal = False

    def __str__(self):
        return 'Log width cannot be set to ' + str(self.requested_size) + \
               ', it must be greater than 40. it has been automatically ' \
               'set to the default of ' + str(self.new_size)


class DatabaseConnError:
    # Log Object for an error connecting to the PSQL database
    def __init__(self, db_name, db_user):
        self.db_user = db_user
        self.db_name = db_name
        self.verbosity = 1
        self.fatal = True

    def __str__(self):
        return 'Error connecting to database ' + self.db_name + \
               '. Please check that it is available and that user ' + \
               self.db_user + ' can connect.'


class RelationCreationError:
    # Log object for an issue creating the relation
    def __init__(self, db_name, relation_name):
        self.db_name = db_name
        self.relation_name = relation_name
        self.verbosity = 3
        self.fatal = True

    def __str__(self):
        return 'Error creating relation ' + self.relation_name + \
               ' in database ' + self.db_name + '.'


class RelationAlreadyExists:
    # Log object for when the relation attempting to be created already exists
    def __init__(self, db_name, relation_name):
        self.db_name = db_name
        self.relation_name = relation_name
        self.verbosity = 4
        self.fatal = False

    def __str__(self):
        return 'Relation ' + self.relation_name + ' already exists in ' \
               'database ' + self.db_name + '.'