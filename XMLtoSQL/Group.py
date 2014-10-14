#                      ______  ______  _____  _     _  _____
#                     |  ____ |_____/ |     | |     | |_____]
#                     |_____| |    \_ |_____| |_____| |
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: October 2014
#          Version: Extended Edition
#
# This class encapsulates the idea of a group, it is a simple idea but it
# enables more broader grouping of machines. Groups are generally defined as
# domains, though the exact interpretation remains up to the collection creating
# this object.

__author__ = 'u5195918'


class Group:

    schema_name = "GROUPS"
    schema = (('name', 'VARCHAR(255) NOT NULL'),
              ('PRIMARY KEY', '(name)'))

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "(Name: " + self.name + ")"