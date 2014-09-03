# Basic python script that runs OSP, basically just palms off arguments
# At the moment only works for the XMLtoSQL component
# No fancy heading, this is just a piece of glue to enable running the module
# independently

__author__ = 'u5195918'
import Parser
from XMLtoSQL import Controller
import sys


# Lets do some command line parsing!
options = Parser.parse(sys.argv)
print options
controller = Controller.Controller(options)

controller.extract_and_insert()



