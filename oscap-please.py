# Basic python script that runs OSP, basically just palms off arguments
# At the moment only works for the XMLtoSQL component
# No fancy heading, this is just a piece of glue to enable running the module
# independently

__author__ = 'u5195918'
import Parser
from Logging import Logger
from Logging.LogEvents import *
from XMLtoSQL import Controller
import ospdata
import sys

parser = Parser.Parser(sys.argv[1:])
options = parser.parse_arguments()

# Create Logger
logger = Logger.Logger(options.log_file_name,
                       options.file_verbosity,
                       options.verbosity,
                       options.log_file_width)

# Log input options
logger.log(InputOptionsReceived(options))

# Which path are we going down?
if options.insert_mode:
    controller = Controller.Controller(options, logger)
    controller.extract_and_insert()
else:
    ospdata.make_report(options, logger)




