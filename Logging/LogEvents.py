#         _____   ______      _______ _    _ _______ __   _ _______ _______
# |      |     | |  ____      |______  \  /  |______ | \  |    |    |______
# |_____ |_____| |_____|      |______   \/   |______ |  \_|    |    ______|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: Extended Edition
#
# This module contains the different types of logging objects, each object
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
__author__ = 'u5195918'


class AttributeNotFound:
    # There has been an issue extracting some attribute from the input file
    # print out which attribute we couldn't find. Shouldnt need to identify
    # file as the previous logged item should do that

    def __init__(self, attribute):
        self.attribute = attribute
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'Unable to find attribute ' + self.attribute


class AvailableCollectionTypes:
    # Log which collection types are available, not exactly majorly pressing
    # but can be useful in debugging
    def __init__(self, collections):
        self.collections = collections
        self.verbosity = 5
        self.fatal = False

    def __str__(self):
        available_types = ''
        for col in self.collections:
            available_types = available_types + col.name + ', '
        # remove trailing comma and space
        available_types = available_types[:-2]
        return 'Currently supported input types: ' + available_types


class InputOptionsReceived:
    # Log exactly which command line argument we've received
    def __init__(self, options):
        self.options = options
        self.fatal = False
        self.verbosity = 2

    def __str__(self):
        return 'Parameter Object Received: ' + str(self.options)

class NoInsertionsRequired:
    # The controller has deemed that no insertions are required
    # this indicates that all collections already exist in the database
    def __init__(self):
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'No collections deemed to require insertion'


class CollectionBuildFailed:
    # For some reason we have failed to build a collection, the actual reason
    # should be logged before this is called
    def __init__(self, collection):
        self.collection = collection
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'Failed to build collection ' + str(self.collection)


class DateError:
    # A date is incompatable with insertion to PSQL
    def __init__(self, date):
        self.date = str(date)
        self.verbosity = 1
        self.fatal = False

    def __str__(self):
        return 'Date ' + self.date + ' is outside acceptable ranges or is' \
                                     ' malformed'


class GeneralExecutionFailure:
    # Something non-specific has gone wrong when attempting to execute
    # a command on the database
    def __init__(self, execution_string, error):
        self.execution_string = execution_string
        self.error = str(error)
        self.verbosity = 1
        self.fatal = True

    def __str__(self):
        return 'Execution failure when attempting to execute command: ' +\
               self.execution_string + '. Database returned error: ' + \
               self.error


class NoDataExtracted:
    # We didn't actually get any information from the input files, we're done.
    def __init__(self):
        self.fatal = True
        self.verbosity = 1

    def __str__(self):
        return 'No data successfully extracted from input files'


class NoResultsFound:
    # Opened file yet found no results, somethign has gone wrong
    def __init__(self, machine_name):
        self.machine_name = machine_name
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'No results found in collection from machine: ' + \
               self.machine_name


class AllInsertionsComplete:
    # Finished inserting everything
    def __init__(self):
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'All database insertions complete'


class InsertionComplete:
    # Successfully completed insertion
    def __init__(self, schema_name):
        self.schema_name = schema_name
        self.fatal = False
        self.verbosity = 5

    def __str__(self):
        return 'Successful insertion into schema ' + self.schema_name


class InsertionError:
    # Error inserting into DB
    def __init__(self, schema_name, error):
        self.schema_name = schema_name
        self.error = error.rstrip()
        self.fatal = False
        self.verbosity = 3

    def __str__(self):
        return 'Error inserting into schema ' + self.schema_name + ' database' \
               ' returned error: ' + str(self.error)


class ObjectCreated:
    # Successfully created object
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.fatal = False
        self.verbosity = 3

    def __str__(self):
        return 'Successfully created ' + self.type + ' ' + self.name + ' in' \
               'in database'


class ObjectCreationFailure:
    # Failed to create object in DB
    def __init__(self, type, name, error):
        self.type = type
        self.name = name
        self.error = error.rstrip()
        self.fatal = True
        self.verbosity = 1

    def __str__(self):
        return 'Failed to create ' + self.type + ' ' + self.name + \
               ' in database, error returned from DB: ' + str(self.error)


class ObjectAlreadyExists:
    # The object already exists in the DB
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.fatal = False
        self.verbosity = 4

    def __str__(self):
        return self.type + ' ' + str(self.name) + ' already exists in database'


class ObjectCheckFailure:
    # Failed to check if something exists in database
    def __init__(self, type, name, error):
        self.type = type
        self.name = name
        self.error = error.rstrip()
        self.fatal = True
        self.verbosity = 1

    def __str__(self):
        return 'Failed to check the existence of ' + self.type + ' ' + \
               self.name + ' database returned error: ' + str(self.error)


class DBConnectionFailure:
    # Failure to connect to database
    def __init__(self, database_name, database_user):
        self.database_name = database_name
        self.database_user = database_user
        self.fatal = True
        self.verbosity = 1

    def __str__(self):
        return 'Failed to connect to database ' + self.database_name + \
               ' as user ' + self.database_user


class ConnectedToDB:
    # Successfully connected to Database
    def __init__(self, database_name, database_user):
        self.database_name = database_name
        self.database_user = database_user
        self.fatal = False
        self.verbosity = 2

    def __str__(self):
        return 'Successfully connected to database ' + self.database_name + \
               ' as user ' + self.database_user


class BuiltCollection:
    # Finalised created a collections Python representation, including
    # all the related objects.
    def __init__(self, collection):
        self.collection = collection.__str__().encode('ascii', 'ignore')
        self.fatal = False
        self.verbosity = 4

    def __str__(self):
        return 'Finished creating collection: ' + self.collection


class CreatedObject:
    # Created a python object with the following properties
    def __init__(self, name, object):
        self.name = name.encode('ascii', 'ignore')
        self.object = object.__str__().encode('ascii', 'ignore')
        self.fatal = False
        self.verbosity = 5

    def __str__(self):
        return 'Created ' + self.name + ' object: ' + self.object


class ParseFailure:
    # Failure to parse input file
    def __init__(self, filename, error):
        self.filename = filename
        self.error = str(error)
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'Unable to parse file ' + self.filename + ', ' \
               'it may be malformed, ElementTree returned: ' + self.error


class CannotIdentifyFileType:
    # None of the collections can handle this type of file
    def __init__(self, filename):
        self.filename = filename
        self.fatal = False
        self.verbosity = 1

    def __str__(self):
        return 'Cannot extract from ' + str(self.filename) + ' as no ' \
               'available collection can parse it'


class ExtractingFile:
    # XML extraction has begun
    def __init__(self, filename):
        self.filename = filename
        self.fatal = False
        self.verbosity = 2

    def __str__(self):
        return 'Began extraction on file ' + str(self.filename)


class CollectionTypeIdentified:
    # Successfully Identified type of XML file
    def __init__(self, filename, collection):
        self.filename = filename
        self.collection = collection.name
        self.fatal = False
        self.verbosity = 3

    def __str__(self):
        return 'File ' + str(self.filename) + ' identified as of type ' + \
            str(self.collection)


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

class SerializationError:
    """Error while serializing a python object for export to javascript"""
    def __init__(self, error):
        self.error = error
        self.verbosity = 1
        self.fatal = True

    def __str(self):
        return "Exception when trying to export to javascript" + str(self.error)


