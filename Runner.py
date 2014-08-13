__author__ = 'sauski'
from OSP import Parser
from OSP.XMLtoSQL import Controller
import sys

# Basic python script that runs OSP, basically just palms off arguments
# At the moment only works for the XMLtoSQL component

# Lets do some command line parsing!
options = Parser.parse(sys.argv)
print options
controller = Controller.Controller(options)

controller.extract_and_insert()



