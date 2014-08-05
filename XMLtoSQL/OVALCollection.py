__author__ = 'Sauski'
# A collection is a file basically
# They are uniquely identified by the date they were
# run as well as the computer name.
import Definition

class OVALCollection:


    def __init__(self, machineName, date, XMLRoot):
        self.machineName = machineName
        self.date = date
        self.XMLRoot = XMLRoot
        self.definitions = []

    def __str__(self):
        return  "(Machine Name: " + self.machineName + \
                " Date: " + self.date + ")"

    def buildDefinitions(self):
        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        oval_definitions = self.XMLRoot.find('oval_definitions')
        definitions = oval_definitions.find('definitions')

        # Find the results of these definitions
        results = self.XMLRoot.find('results')
        system = results.find('system')
        definition_results = system.find('definitions')

        # Definitions is now a list of the declaration of definitions
        # Iterate through, creating definition objects and appending
        # them to our list of definitions
        for definition in definitions:
            # Find the ID
            id = definition.get('id')
            # Move down into the metadata tag
            metadata = definition.find('metadata')
            # Find Title
            title = metadata.find('title').text
            # Find Description
            description = metadata.find('description').text

            # With the ID we can search the rest of the document for the result
            # Unfortunately ElementTree has no way of searching by attribute
            # and thus our algorithm blows out by a factor of n. Although really
            # any extension would be doing this anyway.

            for definition_result in definition_results:
                # Is this the result we want?
                if definition_result.get('definition_id') == id:
                    result = definition_result.get('result')
                    break

            # We have our information, lets compile it into a definition.
            definition_object = Definition.Definition(result, id, title, \
                                                      description)
            self.definitions.append(definition_object)
