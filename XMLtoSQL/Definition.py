__author__ = 'Sauski'
# This may be the common layer for custom modules in the future.
class Definition:

    def __init__(self, result, id, title, description):
        self.result = result
        self.id = id
        self.title = title
        self.description = description

    def __str__(self):
        return "( ID: " + self.id + " Title: " + self.title + " Description: "+\
            self.description + " Result: " + self.result + " )"
