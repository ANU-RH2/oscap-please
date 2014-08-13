__author__ = 'Sauski'
# Controller class, responsible for
# Coordinating the extraction to storing process

import xml.etree.ElementTree as ET
from OSP.XMLtoSQL import Definition, XCCDFCollection,\
    OVALCollection, SQLInterface, Options


class Controller:

    # Class is handed in an XMLtoSQL options object containing files
    # and database information
    def __init__(self, options):
        self.options = options

    def extract_and_insert(self):
        # Some name spacing issues here
        # Honestly I don't even know what is going on here,
        # I typed it and it worked.
        collection_types = (XCCDFCollection.XCCDFCollection,
                            OVALCollection.OVALCollection)

        collections = []

        # Loop through each of the input files
        for input_file in self.options.files:
            # Parse XML File
            # Remove any namespace while we're at it!
            tree = ET.iterparse(input_file)
            for _, el in tree:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
            root = tree.root

            # Which of our collections can handle this file?
            for collection in collection_types:
                if collection.is_of_type(root):
                    col = collection(root)
                    collections.append(col)

        for collection in collections:
            collection.build_definitions()

        # Collections are built, moving onto phase two: database insertion
        interface = SQLInterface.SQLInterface(self.options.database_name,
                                              self.options.database_user)

        interface.create_table(Definition.Definition.schema)

        for collection in collections:
            for definition in collection.definitions:
                interface.insert_into_table(definition)










