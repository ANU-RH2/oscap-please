#  _______  _____  __   _ _______  ______  _____                _______  ______
#  |       |     | | \  |    |    |_____/ |     | |      |      |______ |_____/
#  |_____  |_____| |  \_|    |    |    \_ |_____| |_____ |_____ |______ |    \_
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: MVP
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
    OVALCollection, SQLInterface


class Controller:

    # Class is handed in an XMLtoSQL options object containing files
    # and database information
    def __init__(self, options):
        self.files = options.files
        self.database_name = options.database_name
        self.database_user = options.database_user

    def extract_and_insert(self):
        # Some name spacing issues here
        # Honestly I don't even know what is going on here,
        # I typed it and it worked.
        collection_types = (XCCDFCollection.XCCDFCollection,
                            OVALCollection.OVALCollection)

        collections = []

        # Loop through each of the input files
        for input_file in self.files:
            # Parse XML File
            # Remove any namespace while we're at it!
            tree = ET.iterparse(input_file)
            for _, el in tree:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
            root = tree.root

            # Which of our collections can handle this file?
            # If we can't handle it, print a warning
            can_handle = False
            for collection in collection_types:
                if collection.is_of_type(root):
                    can_handle = True
                    col = collection(root)
                    collections.append(col)

            if not can_handle:
                print 'No Collection Object to Parse ' + input_file

        for collection in collections:
            collection.build_definitions()

        # Collections are built, moving onto phase two: database insertion
        interface = SQLInterface.SQLInterface(self.database_name,
                                              self.database_user)

        interface.create_table(Definition.Definition.schema)

        for collection in collections:
            for definition in collection.definitions:
                interface.insert_into_table(definition)










