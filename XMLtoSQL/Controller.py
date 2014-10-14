#  _______  _____  __   _ _______  ______  _____                _______  ______
#  |       |     | | \  |    |    |_____/ |     | |      |      |______ |_____/
#  |_____  |_____| |  \_|    |    |    \_ |_____| |_____ |_____ |______ |    \_
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This object is essentially the API for the XMLtoSQL component of OSP. It is
# handed an Options object representing the input then told to go off and
# extract and insert. It handles creating the appropriate collection objects
# and making sure that they are the correct ones for the file. It also kicks
# off the SQL insertion process. Any extra collections need only be added to the
# list contained in this object (whilst also added to the package overall)
# and they will automatically be included in the matching process.

__author__ = 'u5195918'


import xml.etree.ElementTree as ET
from XMLtoSQL import Definition, XCCDFCollection,\
    OVALCollection, SQLInterface, Collection, Machine, Group, Test
from Logging.LogEvents import *


class Controller:

    # Class is handed in an XMLtoSQL options object containing files
    # and database information
    def __init__(self, options, logger):
        self.files = options.input_files
        self.database_name = options.database_name
        self.database_user = options.database_user
        self.logger = logger

    def extract_and_insert(self):
        # Some name spacing issues here
        # Honestly I don't even know what is going on here,
        # I typed it and it worked.
        collection_types = (XCCDFCollection.XCCDFCollection,
                            OVALCollection.OVALCollection)

        self.logger.log(AvailableCollectionTypes(collection_types))

        collections = []

        # Loop through each of the input files
        for input_file in self.files:
            self.logger.log(ExtractingFile(input_file))

            # Parse XML File
            try:
                # Remove any namespace while we're at it!
                tree = ET.iterparse(input_file)
                for _, el in tree:
                    # strip all namespaces
                    el.tag = el.tag.split('}', 1)
                    # last element is the actual name
                    el.tag = el.tag[len(el.tag) - 1]

                root = tree.root

            except Exception, e:
                self.logger.log(ParseFailure(input_file, e))
                continue

            # Which of our collections can handle this file?
            # If we can't handle it, print a warning
            can_handle = False
            for collection in collection_types:
                if collection.is_of_type(root):
                    self.logger.log(CollectionTypeIdentified(input_file,
                                                             collection,))
                    can_handle = True
                    col = collection(root, self.logger)
                    collections.append(col)

            if not can_handle:
                self.logger.log(CannotIdentifyFileType(input_file))

        for collection in collections:

            if not collection.build_definitions():
                collections.remove(collection)
                self.logger.log(CollectionBuildFailed(collection))
                continue

            self.logger.log(BuiltCollection(collection))

        # Should we both inserting? Did we actually extract anything?
        if not collections:
            self.logger.log(NoDataExtracted())

        # Collections are built, moving onto phase two: database insertion
        interface = SQLInterface.SQLInterface(self.database_name,
                                              self.database_user,
                                              self.logger)

        # Create single enum type
        # Not really large enough to warrant it's own class
        interface.create_enum('OUTCOME', ('Pass', 'Fail', 'Not Applicable'))

        schemas = (Group.Group, Machine.Machine, Definition.Definition,
                   Collection.Collection, Test.Test)

        for cls in schemas:
            interface.create_table(cls)

        # Did we actually end up inserting something?
        inserted = False
        for collection in collections:

            # Before we go through the usual insertion phase, lets
            # just check whether or not this collection exists in the
            # database, saves us the trouble of inserting all the
            # associated tests and such

            if interface.check_existence(collection):
                self.logger.log(ObjectAlreadyExists('Collection',
                                                    str(collection)))
                continue

            inserted = True
            # Group First
            interface.insert_into_table(collection.machine.group)
            # Then Name
            interface.insert_into_table(collection.machine)
            # Then the collection
            interface.insert_into_table(collection)
            # Then the tests
            for test in collection.tests:
                interface.insert_into_table(test.definition)
                interface.insert_into_table(test)

        if inserted:
            self.logger.log(AllInsertionsComplete())
        else:
            self.logger.log(NoInsertionsRequired())










