# This file has been depreciated, It was used for testing in the development
# of the logging module.

__author__ = 'sauski'

from Logger import Logger
from LogEvents import *

# Simple runner file.

logger = Logger('log', 5, 5, 20)

rel = RelationAlreadyExists('Collections', 'OSP')
dberror = DatabaseConnError('OSP', 'postgres')

logger.log(rel)
logger.log(dberror)
