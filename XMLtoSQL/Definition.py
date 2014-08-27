#     ______  _______ _______ _____ __   _ _____ _______ _____  _____  __   _
#     |     \ |______ |______   |   | \  |   |      |      |   |     | | \  |
#     |_____/ |______ |       __|__ |  \_| __|__    |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: MVP
#
# This file defines what a definition looks like, including the basic schema
# information for the MVP single relation database. The information that
# collections objects extract from their respective input files must match the
# types of information contained here. Some cleaning of inputs takes place, for
# example only Pass, Fail and NA results are permitted, any others are changed
# into these three types. Extending the information contained in the schema
# is as simple as adding to the classes schema object and adding the appropriate
# class variables.
#TODO Fix mismatches between database names

__author__ = 'u5195918'


class Definition:
    schema = (('machine_name', 'VARCHAR(255) NOT NULL'),
              ('unique_id', 'VARCHAR(255) NOT NULL'),
              ('definition_name', 'VARCHAR(255) NOT NULL'),
              ('result', 'VARCHAR(255) NOT NULL'),
              ('date', 'TIMESTAMP NOT NULL'),
              ('PRIMARY KEY', '(machine_name, unique_id, Date)')
    )

    def __init__(self, machine_name, unique_id, definition_name, result, date):
        self.machine_name = machine_name
        self.unique_id = unique_id
        self.definition_name = definition_name
        self.date = date
        self.result = result

        self.validate_definition()

    def __str__(self):
        return "(Machine Name: " + self.machine_name + \
               " Unique ID " + self.unique_id + \
               " Definition Name: " + self.definition_name +\
               " Result: " + self.result +\
               " Date: " + self.date + ")"

    def validate_definition(self):
        # Does this definition pass formatting tests?
        # TODO Add logging to the fixes
        if len(self.machine_name) > 255:
            self.machine_name = self.machine_name[:255]
        if len(self.definition_name) > 255:
            self.definition_name = self.definition_name[:255]

        # Ensure results is either Pass, Fail or Not Applicable

        if self.result != 'Pass' or self.result != 'Fail' \
                or self.result != 'Not Applicable':
            if 'pass' in self.result.lower() or 'true' in self.result.lower():
                # print 'Normalised ' + self.result + ' to Pass'
                self.result = 'Pass'
            elif 'fail' in self.result.lower() or \
                 'false' in self.result.lower():
                # print 'Normalised ' + self.result + ' to Fail'
                self.result = 'Fail'
            else:
                # print 'Normalised ' + self.result + ' to NA'
                self.result = 'Not Applicable'

    class Date:
        # Normalised Date Object for Entry into PSQL
        def __init__(self, second, minute, hour, day, month, year):
            # Take input and format it so postgres will accept it
            self.timestamp = year + '-' + month + '-' + day + ' ' + hour\
                            + ':' + minute + ':' + second

        def __str__(self):
            return self.timestamp.decode('ascii', 'ignore')



