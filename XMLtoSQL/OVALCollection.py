#                           _____  _    _ _______
#                          |     |  \  /  |_____| |
#                          |_____|   \/   |     | |_____
#
#   _______  _____                _______ _______ _______ _____  _____  __   _
#   |       |     | |      |      |______ |          |      |   |     | | \  |
#   |_____  |_____| |_____ |_____ |______ |_____     |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: MVP
#
# This file contains the OVAL version of the collection object. This object
# contains the logic for extracting the required definition information from
# an XML file matching the Open Vulnerability and Assessment Language OVAL
# specifications. Results are found by performing a forward lookup from each
# of the defined definitions in the first part of the document.
# TODO Re-work the file identification function for more accurate identification

__author__ = 'u5195918'
from XMLtoSQL import Definition, Collection


class OVALCollection(Collection.Collection):

    def __init__(self, xml_root):
        Collection.Collection.__init__(self, xml_root)

    def __str__(self):
        return "(Machine Name: " + self.machine_name + \
               " Date: " + self.date.__str__() + ")"

    def build_definitions(self):

        # Find Hostname
        for host in self.xml_root.getiterator('primary_host_name'):
            self.machine_name = host.text

        # Find Date
        generator = self.xml_root.find('generator')
        date = generator.find('timestamp')
        self.date = date.text
        # Build date
        # Dates in this format look something like 2014-07-21T02:46:46
        formatted_date = Definition.Definition.Date(self.date[17:19],
                                                    self.date[14:16],
                                                    self.date[11:13],
                                                    self.date[8:10],
                                                    self.date[5:7],
                                                    self.date[:4])

        self.date = formatted_date

        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        oval_definitions = self.xml_root.find('oval_definitions')
        definitions = oval_definitions.find('definitions')

        # Find the results of these definitions
        results = self.xml_root.find('results')
        system = results.find('system')
        definition_results = system.find('definitions')

        # Definitions is now a list of the declaration of definitions
        # Iterate through, creating definition objects and appending
        # them to our list of definitions
        for definition in definitions:
            # Find the ID
            unique_id = definition.get('id')
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
            result = 'Result not found'
            for definition_result in definition_results:
                # Is this the result we want?
                if definition_result.get('definition_id') == unique_id:
                    result = definition_result.get('result')
                    break

            # We have our information, lets compile it into a definition.
            definition_object = Definition.Definition(self.machine_name,
                                                      unique_id,
                                                      title,
                                                      result,
                                                      self.date)
            self.definitions.append(definition_object)

    @staticmethod
    def is_of_type(xml_root):
        # Is this an OVAL file?
        # TODO Make this not just the opposite of XCCDF
        test_result = xml_root.find('TestResult')
        return test_result is None
