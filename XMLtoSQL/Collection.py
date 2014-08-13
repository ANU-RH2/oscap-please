__author__ = 'sauski'

# 'Abstract' class from which all collection inherit and override


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