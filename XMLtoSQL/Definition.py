#     ______  _______ _______ _____ __   _ _____ _______ _____  _____  __   _
#     |     \ |______ |______   |   | \  |   |      |      |   |     | | \  |
#     |_____/ |______ |       __|__ |  \_| __|__    |    __|__ |_____| |  \_|
#
#       Written By: Theodore Olsauskas-Warren - u5195918
#               In: August 2014
#          Version: Extended Edition
#
# This class has has a significant reduction in size in the EE. It now forms
# a single part of a larger database, rather than the entire database. It is
# created by collections and populated with information extracted from the
# input files, it is then simply inserted into the DB. Changes to the
# information regarding definitions can be made by extending the schema
# in any way the developer desires, as long as the functions creating the
# definition are also updates. Definitions are also the only encapsulation to
# by default truncate the length of their attributes, as they are far and
# above the most likely to exceed them.

__author__ = 'u5195918'


class Definition:

    schema_name = "DEFINITIONS"
    schema = (('id', 'VARCHAR(255) NOT NULL'),
              ('title', 'VARCHAR(255) NOT NULL'),
              ('description', 'VARCHAR(255) NOT NULL'),
              ('resolution', 'VARCHAR(255) NOT NULL'),
              ('PRIMARY KEY', '(id)'))

    def __init__(self, unique_id, title, description, resolution):
        self.id = unique_id
        self.title = title
        self.description = description
        self.resolution = resolution
        self.validate()

    def validate(self):
        # Ensure entries meet database requirements
        self.resolution = self.truncate_string(self.resolution)
        self.description = self.truncate_string(self.description)

        # Strip excessive whitespace
        self.resolution = ' '.join(self.resolution.split())
        self.description = ' '.join(self.description.split())

    def __str__(self):
        return "(Id: " + self.id + \
               " Title: " + self.title + \
               " Description: " + self.description + \
               " Resolution: " + self.resolution + ")"

    @staticmethod
    def truncate_string(input_string):
        if input_string is not None:
            string_length = 255
            return input_string[:string_length]
        return input_string





