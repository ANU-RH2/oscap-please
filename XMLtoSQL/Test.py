#                         _______ _______ _______ _______
#                            |    |______ |______    |
#                            |    |______ ______|    |
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This class is designed to encapsulate the idea of a "test", which is
# defined as a specific instance of a definition, and thus has a result and
# a machine attached to it. It is created by the collections after extracting
# the data. It is standardised across all collections, i.e. they must all
# extract the same data.

__author__ = 'u5195918'


class Test:

    # Tests table schema
    schema_name = "TESTS"
    schema = (('date', 'TIMESTAMP NOT NULL'),
              ('machine_name', 'VARCHAR(255) NOT NULL'),
              ('definition_id', 'VARCHAR(255) NOT NULL'),
              ('result', 'OUTCOME NOT NULL'),
              ('PRIMARY KEY', '(date, machine_name, definition_id)'),
              ('FOREIGN KEY', '(date, machine_name)\
              REFERENCES COLLECTIONS(date, machine_name)'))

    def __init__(self, machine_name, definition, date, result,):
        self.machine_name = machine_name
        self.definition = definition
        self.date = date

        # Extract definition_id from definition
        self.definition_id = definition.id

        # Format result into one of three possible options
        self.result = self.format_result(result)

    def __str__(self):
        return "(Date: " + str(self.date) + \
               " Machine Name: " + self.machine_name + \
               " Definition ID: " + str(self.definition_id) + \
               " Result: " + str(self.result) + ")"

    @staticmethod
    def format_result(result):

        if 'pass' in result.lower() or 'true' in result.lower():
            return 'Pass'
        elif 'fail' in result.lower() or \
             'false' in result.lower():
            return 'Fail'
        else:
            return 'Not Applicable'
