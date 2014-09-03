# OSP Data Analyzer
# ospdata.py
# Extracts data from the SQL Database
# By Elliot Osborne (u4670030)

import config
import sql

# This provides a basic list of machines, definitions,
# and the results on a given day.
# Also gives the configuration used to generate the output.
# The output is a a pair containing the configuration as a dict,
# and a list of dictionaries, where each corresponds to one test.

# Example test record:
# {'date': datetime.date(2014, 8, 4),
#   'machine_name': 'ejo-port',
#   'definition_name': 'Enterprise Quality Solution',
#   'result': 'Failed'}
def get_MVP():
    return sql.get_MVP()

if __name__ == "__main__":
    for r in get_MVP():
        print r
