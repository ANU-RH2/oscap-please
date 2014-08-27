__author__ = 'sauski'

from Logger import Logger
from LogEvents import *

# Simple runner file.

logger = Logger('log', 5, 5, 20)

rel = RelationAlreadyExists('Collections', 'OSP')
dberror = DatabaseConnError('OSP', 'postgres')

logger.log(rel)
logger.log(dberror)
