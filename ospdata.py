# OSP Data Analyzer
# ospdata.py
# Extracts data from the SQL Database
# By Elliot Osborne (u4670030)

import config
import sql
import json

# The most basic operation: fetch the collections as-is
# from the database.
# Will return [("machine_name", "date", "no_of_tests", "pass_rate")] as JSON.
# Will be filtered based on config.cfg
def get_collections():
    return json.dumps(sql.get_collections())

if __name__ == "__main__":
    print get_collections()
