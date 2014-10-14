#                           _____  _    _ _______
#                          |     |  \  /  |_____| |
#                          |_____|   \/   |     | |_____
#
#   _______  _____                _______ _______ _______ _____  _____  __   _
#   |       |     | |      |      |______ |          |      |   |     | | \  |
#   |_____  |_____| |_____ |_____ |______ |_____     |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This file contains the OVAL version of the collection object. This object
# contains the logic for extracting the required definition information from
# an XML file matching the Open Vulnerability and Assessment Language OVAL
# specifications. Results are found by performing a forward lookup from each
# of the defined definitions in the first part of the document. OVAL functions
# can be uniquely identified by containing oval-definition tags within the
# root tag. Unfortunately OVAL files have no concept of resolution within
# their definitions, and thus this field is always effectively empty.

__author__ = 'u5195918'
from XMLtoSQL import Definition, Collection, Test, Group, Machine
from Logging.LogEvents import *


class OVALCollection(Collection.Collection):

    name = 'OVAL'

    def __init__(self, xml_root, logger):
        Collection.Collection.__init__(self, xml_root, logger)

    def __str__(self):
        return "(Machine Name: " + self.machine_name + \
               " Date: " + str(self.date) + \
               " Number of Tests: " + str(self.no_of_tests) + \
               " Pass Percentage: " + str(self.pass_rate) + ")"

    def build_definitions(self):

        target_name = None

        # Find Hostname
        for host in self.xml_root.getiterator('primary_host_name'):
            target_name = host.text

        if target_name is None:
            self.logger.log(AttributeNotFound('target name'))
            return False

        # Machine name comes before the first dot
        self.machine_name = target_name.rsplit('.')[0]

        # Find Group
        # Group is everything after the first dot
        group_name = '.'.join(target_name.rsplit('.')[1:])

        # Create a machine and assign a group
        group_object = Group.Group(group_name)
        self.logger.log(CreatedObject('Group', group_object))

        self.machine = Machine.Machine(self.machine_name, group_object)
        self.logger.log(CreatedObject('Machine', self.machine))

        # Find Date
        generator = self.xml_root.find('generator')
        date = generator.find('timestamp')
        self.date = date.text
        # Build date
        # Dates in this format look something like 2014-07-21T02:46:46
        formatted_date = Collection.Collection.Date(self.date[17:19],
                                                    self.date[14:16],
                                                    self.date[11:13],
                                                    self.date[8:10],
                                                    self.date[5:7],
                                                    self.date[:4])

                # Was the date valid?
        if not formatted_date.valid:
            # If not, log an error and return
            self.logger.log(DateError(formatted_date))
            return False

        self.date = formatted_date

        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        oval_definitions = self.xml_root.find('oval_definitions')
        definitions = oval_definitions.find('definitions')

        if definitions is None:
            self.logger.log(AttributeNotFound('definitions'))
            return False

        # Find the results of these definitions
        results = self.xml_root.find('results')
        system = results.find('system')
        definition_results = system.find('definitions')

        if definition_results is None:
            self.logger.log(AttributeNotFound('definition results'))
            return False

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
            if title is None:
                self.logger.log(AttributeNotFound('definition title'))
                return False

            # Find Description
            description = metadata.find('description').text
            if description is None:
                self.logger.log(AttributeNotFound('definition description'))
                return False

            # OVAL definitions have no resolution
            resolution = "No resolution given"

            # With the ID we can search the rest of the document for the result
            # Unfortunately ElementTree has no way of searching by attribute
            # and thus our algorithm blows out by a factor of n. Although really
            # any extension would be doing this anyway.
            result = None
            for definition_result in definition_results:
                # Is this the result we want?
                if definition_result.get('definition_id') == unique_id:
                    result = definition_result.get('result')
                    break

            if result is None:
                self.logger.log(AttributeNotFound('definition result'))
                return False

            # We have our information, lets compile it into a definition.
            definition_object = Definition.Definition(unique_id,
                                                      title,
                                                      description,
                                                      resolution)

            self.logger.log(CreatedObject('Definition', definition_object))

            test_object = Test.Test(self.machine_name,
                                    definition_object,
                                    self.date,
                                    result)

            self.logger.log(CreatedObject('Test', test_object))

            # Is the test applicable and did we pass it?
            if test_object.result != "Not Applicable":
                # Applicable test
                self.no_of_tests += 1
                if test_object.result == "Pass":
                    self.number_of_tests_passed += 1

            self.tests.append(test_object)

        # What is our pass percentage (as an integer, 0-100)
        if self.no_of_tests > 0:
            self.pass_rate = self.number_of_tests_passed * 100 / \
                self.no_of_tests

        return True

    @staticmethod
    def is_of_type(xml_root):
        # Is this an OVAL file?
        oval_definitions = xml_root.find('oval_definitions')
        return oval_definitions is not None
