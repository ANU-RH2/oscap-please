#   _______  _____                _______ _______ _______ _____  _____  __   _
#   |       |     | |      |      |______ |          |      |   |     | | \  |
#   |_____  |_____| |_____ |_____ |______ |_____     |    __|__ |_____| |  \_|
#

#
# This object is the "abstract" collection object from which all current and
# future collection objects inherit. It skirts around the idea of abstract
# classes which aren't technically supported in Python by simply throwing
# exceptions should any of it's methods be called. It also controls the
# default values for collection wide properties, such as the machine name and
# date.

__author__ = 'u5195918'


class Collection:
    def __init__(self, xml_root):
        self.xml_root = xml_root
        self.definitions = []
        self.machine_name = 'unknown'
        self.date = 'unknown'

    def __str__(self):
        raise Exception('Abstract Class toString requested')

    @staticmethod
    def is_of_type(xml_tree):
        raise Exception('Method Not Implemented')

    def build_definitions(self):
        raise Exception('Method Not Implemented')