#   _______  _____                _______ _______ _______ _____  _____  __   _
#   |       |     | |      |      |______ |          |      |   |     | | \  |
#   |_____  |_____| |_____ |_____ |______ |_____     |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This object is the "abstract" collection object from which all current and
# future collection objects inherit. It skirts around the idea of abstract
# classes which aren't technically supported in Python by simply throwing
# exceptions should any of it's methods be called. It also controls the
# default values for collection wide properties, such as the machine name and
# date. It is also home to the standardised date input class, for which
# collection implementations must hand off to tests for insertion in the DB

__author__ = 'u5195918'


class Collection:

    schema_name = "COLLECTIONS"
    schema = (('date', 'TIMESTAMP NOT NULL'),
              ('machine_name', 'VARCHAR(255) NOT NULL'),
              ('no_of_tests', 'INTEGER NOT NULL'),
              ('pass_rate', 'FLOAT NOT NULL'),
              ('PRIMARY KEY', '(date, machine_name)'),
              ('FOREIGN KEY', '(machine_name) REFERENCES MACHINES(name)'))

    def __init__(self, xml_root, logger):
        self.xml_root = xml_root
        self.logger = logger
        self.name = 'unknown'
        self.tests = []
        self.date = 'unknown'
        self.machine_name = 'unknown'
        self.machine = 'not set'
        self.no_of_tests = 0
        self.number_of_tests_passed = 0
        self.pass_rate = 100

    def __str__(self):
        raise Exception('Abstract Class toString requested')

    @staticmethod
    def is_of_type(xml_tree):
        raise Exception('Method Not Implemented')

    def build_definitions(self):
        raise Exception('Method Not Implemented')

    class Date:
        # Normalised Date Object for Entry into PSQL
        def __init__(self, second, minute, hour, day, month, year):
            # Take input and format it so postgres will accept it
            self.second = second
            self.minute = minute
            self.hour = hour
            self.day = day
            self.month = month
            self.year = year

            self.valid = self.validate()

            self.timestamp = year + '-' + month + '-' + day + ' ' + hour\
                            + ':' + minute + ':' + second

        def __str__(self):
            return self.timestamp.decode('ascii', 'ignore')

        def validate(self):
            # Validate that stored values are in acceptable ranges
            if int(self.second) > 60         \
                    or int(self.second) < 0  \
                    or int(self.minute) < 0  \
                    or int(self.minute) > 60 \
                    or int(self.hour) < 0   \
                    or int(self.hour) > 24   \
                    or int(self.day) > 31    \
                    or int(self.day) < 0     \
                    or int(self.month) > 12  \
                    or int(self.month) < 0   \
                    or int(self.year) < 0:
                return False
            else:
                return True