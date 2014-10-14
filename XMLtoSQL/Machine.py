#              _______ _______ _______ _     _ _____ __   _ _______
#              |  |  | |_____| |       |_____|   |   | \  | |______
#              |  |  | |     | |_____  |     | __|__ |  \_| |______
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This class encapsulates the idea of a machine, machines own tests and belong
# to groups. This is a pretty sparse class, but it is important as to represent
# the eventual SQL data in Python. Any changes to the schema can be made here,
# and as with the other encapsulation classes the changes will automatically
# be picked up by the SQL interface. Machine objects are made by the different
# collections, and thus along with definitions, groups and tests form a
# standard interface for them.

__author__ = 'u5195918'


class Machine:

    schema_name = "MACHINES"
    schema = (('name', 'VARCHAR(255) NOT NULL'),
              ('group_name', 'VARCHAR(255) NOT NULL'),
              ('PRIMARY KEY', '(name)'),
              ('FOREIGN KEY', '(group_name)\
              REFERENCES GROUPS(name)'))

    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.group_name = group.name

    def __str__(self):
        return "(Machine Name: " + self.name + \
               " Group Name: " + self.group_name + ")"
