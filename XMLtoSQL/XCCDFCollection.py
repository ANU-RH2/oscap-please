#                    _     _ _______ _______ ______  _______
#                     \___/  |       |       |     \ |______
#                    _/   \_ |_____  |_____  |_____/ |
#
#   _______  _____                _______ _______ _______ _____  _____  __   _
#   |       |     | |      |      |______ |          |      |   |     | | \  |
#   |_____  |_____| |_____ |_____ |______ |_____     |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This file contains the XCCDF implementation of the collection class. It
# contains the logic for extracting the MVP definition information from a
# Extensible Configuration Checklist Description Format (XCCDF). It will also
# uniquely identify these types of files (at the moment this is achieved by
# checking for a TestResult child of the XML tree root).
# Definition titles and descriptions are found by performing a reverse lookup
# on their results.

__author__ = 'u5195918'
from XMLtoSQL import Definition, Collection, Test, Group, Machine
from Logging.LogEvents import *


class XCCDFCollection(Collection.Collection):

    name = 'XCCDF'

    def __init__(self, xml_root, logger):
        Collection.Collection.__init__(self, xml_root, logger)

    def __str__(self):
        return "(Machine Name: " + self.machine_name + \
               " Date: " + str(self.date) + \
               " Number of Tests: " + str(self.no_of_tests) + \
               " Pass Percentage: " + str(self.pass_rate) + ")"

    def build_definitions(self):
        # Get target name, then break it down
        # into host name and group
        # localhost.localdomain.local
        target_name = (self.xml_root.find('TestResult')).\
            find('target').text

        if target_name is None:
            self.logger.log(AttributeNotFound('target name'))
            return False

        # Machine name comes before the first dot
        self.machine_name = target_name.rsplit('.')[0]

        # Group is everything after the first dot
        group_name = '.'.join(target_name.rsplit('.')[1:])

        # Create a machine and assign a group
        group_object = Group.Group(group_name)
        self.logger.log(CreatedObject('Group', group_object))

        self.machine = Machine.Machine(self.machine_name, group_object)
        self.logger.log(CreatedObject('Machine', self.machine))

        # Look through our XML tree and find our definitions
        # First move through the tree to the correct position
        test_results = self.xml_root.find('TestResult')
        rule_results = test_results.findall('rule-result')

        if rule_results is None:
            self.logger.log(AttributeNotFound('rule results'))
            return False

        # Setup data to reverse lookup title and description info
        rules = self.xml_root.getiterator('Rule')
        if rules is None:
            self.logger.log(AttributeNotFound('rules'))
            return False

        # Grab the date, easiest from a test result
        try:
            self.date = rule_results[0].get('time')
        except IndexError, e:
            # If we get an index error we had no rule results,
            # which means something has gone wrong
            self.logger.log(NoResultsFound(self.machine))
            return False

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

        # We have a list of results, iterate over them
        for rule_result in rule_results:
            result = rule_result.find('result').text
            unique_id = rule_result.get('idref')

            if unique_id is None:
                self.logger.log(AttributeNotFound('definition id'))
                return False

            #Setup Defaults
            #XCCDF is odd in that these are not strictly required
            #therefore not finding them is not so bad
            title = 'No Title Found'
            description = 'No Description Found'
            resolution = 'No Resolution Found'

            # From the results, look back up the title and description
            for rule in rules:
                if rule.get('id') == unique_id:
                    # Found it
                    title = rule.find('title').text
                    # So often the description will have embedded
                    # The description tag sometimes has other tags inside it...
                    # Which is really, really dumb. So this only returns the
                    # text up to the first tag.
                    description = rule.find('description').text
                    potential_res = rule.find('fix')
                    if potential_res is not None:
                        resolution = potential_res.text
                    break

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
        # Is this an XCCDF file?
        test_result = xml_root.find('TestResult')
        return test_result is not None